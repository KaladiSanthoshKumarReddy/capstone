import { Router, Response } from 'express'
import { z } from 'zod'
import { getDb } from '../db/init'
import { authMiddleware, AuthRequest } from '../middleware/auth'

const router = Router()
router.use(authMiddleware)

const createSchema = z.object({
  title: z.string().min(1),
  description: z.string().optional(),
})

const patchSchema = z.object({
  title: z.string().min(1).optional(),
  description: z.string().optional(),
  status: z.enum(['active', 'completed', 'archived']).optional(),
})

// GET /api/items?page=1&limit=10&search=text&status=active
router.get('/', async (req: AuthRequest, res: Response) => {
  const page  = Math.max(1, parseInt(req.query.page  as string) || 1)
  const limit = Math.min(100, Math.max(1, parseInt(req.query.limit as string) || 10))
  const search = (req.query.search as string | undefined)?.trim() || null
  const status = (req.query.status as string | undefined) || null
  const offset = (page - 1) * limit

  const db = getDb()

  const whereClauses: string[] = ['user_id = ?']
  const args: (string | number | null)[] = [req.userId ?? null]

  if (search) {
    whereClauses.push("(title LIKE ? OR description LIKE ?)")
    args.push(`%${search}%`, `%${search}%`)
  }
  if (status && status !== 'all') {
    whereClauses.push("status = ?")
    args.push(status)
  }

  const where = whereClauses.length ? `WHERE ${whereClauses.join(' AND ')}` : ''

  const countResult = await db.execute({ sql: `SELECT COUNT(*) as total FROM items ${where}`, args })
  const total = Number((countResult.rows[0] as unknown as { total: number }).total)

  const itemsResult = await db.execute({
    sql: `SELECT * FROM items ${where} ORDER BY created_at DESC LIMIT ? OFFSET ?`,
    args: [...args, limit, offset],
  })

  return res.json({
    success: true,
    data: itemsResult.rows,
    meta: { total, page, limit, totalPages: Math.ceil(total / limit) },
  })
})

// POST /api/items
router.post('/', async (req: AuthRequest, res: Response) => {
  const parsed = createSchema.safeParse(req.body)
  if (!parsed.success) {
    return res.status(400).json({ success: false, error: 'Invalid input' })
  }
  const { title, description } = parsed.data
  const db = getDb()
  const result = await db.execute({
    sql: 'INSERT INTO items (title, description, user_id) VALUES (?, ?, ?)',
    args: [title, description ?? null, req.userId ?? null],
  })
  return res.status(201).json({ success: true, data: { id: Number(result.lastInsertRowid) } })
})

// PATCH /api/items/:id  [55187]
router.patch('/:id', async (req: AuthRequest, res: Response) => {
  const parsed = patchSchema.safeParse(req.body)
  if (!parsed.success) {
    return res.status(400).json({ success: false, error: 'Invalid input' })
  }
  const { title, description, status } = parsed.data
  if (!title && description === undefined && !status) {
    return res.status(400).json({ success: false, error: 'Nothing to update' })
  }
  const db = getDb()

  const setClauses: string[] = ['updated_at = CURRENT_TIMESTAMP']
  const args: (string | number | null)[] = []
  if (title)                { setClauses.push('title = ?');       args.push(title) }
  if (description !== undefined) { setClauses.push('description = ?'); args.push(description) }
  if (status)               { setClauses.push('status = ?');      args.push(status) }
  args.push(req.params.id, req.userId ?? null)

  const result = await db.execute({
    sql: `UPDATE items SET ${setClauses.join(', ')} WHERE id = ? AND user_id = ?`,
    args,
  })

  if (result.rowsAffected === 0) {
    return res.status(404).json({ success: false, error: 'Item not found' })
  }

  const updated = await db.execute({
    sql: 'SELECT * FROM items WHERE id = ? AND user_id = ?',
    args: [req.params.id, req.userId ?? null],
  })
  return res.json({ success: true, data: updated.rows[0] })
})

// DELETE /api/items/:id
router.delete('/:id', async (req: AuthRequest, res: Response) => {
  const db = getDb()
  const result = await db.execute({
    sql: 'DELETE FROM items WHERE id = ? AND user_id = ?',
    args: [req.params.id, req.userId ?? null],
  })
  if (result.rowsAffected === 0) {
    return res.status(404).json({ success: false, error: 'Item not found' })
  }
  return res.json({ success: true, data: { deleted: true } })
})

export default router
