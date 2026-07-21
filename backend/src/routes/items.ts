import { Router, Response } from 'express'
import { z } from 'zod'
import { getDb } from '../db/init'
import { authMiddleware, AuthRequest } from '../middleware/auth'

const router = Router()
router.use(authMiddleware)

const itemSchema = z.object({
  title: z.string().min(1),
  description: z.string().optional(),
})

router.get('/', async (_req: AuthRequest, res: Response) => {
  const db = getDb()
  const result = await db.execute('SELECT * FROM items ORDER BY created_at DESC')
  return res.json({ success: true, data: result.rows })
})

router.post('/', async (req: AuthRequest, res: Response) => {
  const parsed = itemSchema.safeParse(req.body)
  if (!parsed.success) {
    return res.status(400).json({ success: false, error: 'Invalid input' })
  }
  const { title, description } = parsed.data
  const db = getDb()
  const result = await db.execute({
    sql: 'INSERT INTO items (title, description, user_id) VALUES (?, ?, ?)',
    args: [title, description ?? null, req.userId ?? null],
  })
  return res.status(201).json({ success: true, data: { id: result.lastInsertRowid } })
})

router.delete('/:id', async (req: AuthRequest, res: Response) => {
  const db = getDb()
  await db.execute({ sql: 'DELETE FROM items WHERE id = ?', args: [req.params.id] })
  return res.json({ success: true, data: { deleted: true } })
})

export default router
