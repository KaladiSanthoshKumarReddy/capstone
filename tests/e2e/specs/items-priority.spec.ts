import { test, expect } from '@playwright/test'
import { LoginPage } from '../pages/LoginPage'

const USER = { email: 'priority_test@capstone.dev', password: 'Test1234!' }

test.describe('Item Priority (EPMCDMETST-58868)', () => {
  test.beforeEach(async ({ page }) => {
    // Register (no-op if already exists)
    await page.request.post('http://localhost:4000/api/auth/register', {
      data: { email: USER.email, password: USER.password },
    })

    const login = new LoginPage(page)
    await login.goto()
    await login.login(USER.email, USER.password)
    await page.waitForURL('**/dashboard')
  })

  test('Happy path: create item with priority and see badge', async ({ page }) => {
    // This test assumes the UI has a pri√ority selector with testid 'item-priority-select'
    // and item cards render a badge with testid 'item-priority-<id>'.
    // If testids differ, update this spec accordingly.

    const title = `Priority High ${Date.now()}`
    await page.getByTestId('item-title-input').fill(title)

    // Priority select
    const prioritySelector = page.getByTestId('item-priority-select')
    await expect(prioritySelector).toBeVisible()
    await prioritySelector.selectOption('high')

    await page.getByTestId('add-item-button').click()

    // assert item appears
    const titleEl = page.locator('[data-testid^="item-title-"]').filter({ hasText: title }).first()
    await expect(titleEl).toBeVisible()

    const testId = await titleEl.getAttribute('data-testid')
    const id = testId?.replace('item-title-', '')
    expect(id).toBeTruthy()

    await expect(page.locator(`[data-testid="item-priority-${id}"]`)).toHaveText(/high/i)
  })

  test('Error path: API rejects invalid priority (400)', async ({ page }) => {
    // Auth boundary is covered in existing specs; here we validate invalid priority is rejected.
    // Login via UI already sets token in localStorage, we can reuse it.
    const token = await page.evaluate(() => localStorage.getItem('token'))
    expect(token).toBeTruthy()

    const resp = await page.request.post('http://localhost:4000/api/items', {
      data: { title: 'Bad Priority Item', description: '', priority: 'CRITICAL' },
      headers: { Authorization: `Bearer ${token}` },
    })

    expect(resp.status()).toBe(400)
    const body = await resp.json()
    // The exact message can vary; assert general invalidation signal.
    expect(JSON.stringify(body).toLowerCase()).toMatch(/(priority|invalid)/)
  })
})
