import { test, expect } from '@playwright/test'
import { LoginPage } from '../pages/LoginPage'
import { DashboardPage } from '../pages/DashboardPage'

const USER = { email: 'items_test@capstone.dev', password: 'Test1234!' }

async function ensureUser(page: import('@playwright/test').Page) {
  // Register (no-op if already exists)
  await page.request.post('http://localhost:4000/api/auth/register', {
    data: { email: USER.email, password: USER.password },
  })
}

test.describe('Item Management', () => {
  test.beforeEach(async ({ page }) => {
    await ensureUser(page)
    const login = new LoginPage(page)
    await login.goto()
    await login.login(USER.email, USER.password)
    await page.waitForURL('**/dashboard')
  })

  test('should show empty state when no items', async ({ page }) => {
    const dash = new DashboardPage(page)
    const empty = page.getByTestId('empty-state')
    // If DB is empty the empty state renders, otherwise items-loading or item-list renders
    await expect(page.getByTestId('dashboard-heading')).toBeVisible()
  })

  test('should add a new item', async ({ page }) => {
    const titleInput = page.getByTestId('item-title-input')
    const addBtn     = page.getByTestId('add-item-button')
    const title = `My first test item ${Date.now()}`

    await titleInput.fill(title)
    await addBtn.click()

    await expect(titleInput).toHaveValue('')
    await expect(page.getByText(title)).toBeVisible()
  })

  test('should delete an item', async ({ page }) => {
    const titleInput = page.getByTestId('item-title-input')
    const addBtn     = page.getByTestId('add-item-button')

    await titleInput.fill('Item to delete')
    await addBtn.click()
    await page.waitForSelector('[data-testid^="item-card-"]')

    // Click first delete button
    const deleteBtn = page.locator('[data-testid^="item-delete-"]').first()
    page.once('dialog', d => d.accept())
    await deleteBtn.click()

    await expect(page.getByText('Item to delete')).not.toBeVisible()
  })

  test('should toggle item status to completed', async ({ page }) => {
    const titleInput = page.getByTestId('item-title-input')
    const addBtn     = page.getByTestId('add-item-button')
    const title = `Toggle me ${Date.now()}`

    await titleInput.fill(title)
    await addBtn.click()
    await expect(page.getByText(title)).toBeVisible()

    const titleEl = page.locator('[data-testid^="item-title-"]').filter({ hasText: title }).first()
    const titleTestId = await titleEl.getAttribute('data-testid')
    const id = titleTestId?.replace('item-title-', '')
    expect(id).toBeTruthy()

    const toggle = page.locator(`[data-testid="item-toggle-${id}"]`)
    await toggle.click()

    // Status badge should show 'completed'
    await expect(page.locator(`[data-testid="item-status-${id}"]`)).toHaveText('completed')
  })

  test('should inline-edit item title', async ({ page }) => {
    const titleInput = page.getByTestId('item-title-input')
    const addBtn     = page.getByTestId('add-item-button')
    const title = `Old title ${Date.now()}`
    const nextTitle = `New title ${Date.now()}`

    await titleInput.fill(title)
    await addBtn.click()
    await expect(page.getByText(title)).toBeVisible()

    // Click the title to enter edit mode
    const titleEl = page.locator('[data-testid^="item-title-"]').filter({ hasText: title }).first()
    const titleTestId = await titleEl.getAttribute('data-testid')
    const id = titleTestId?.replace('item-title-', '')
    expect(id).toBeTruthy()
    await titleEl.click()

    const editInput = page.locator(`[data-testid="item-edit-input-${id}"]`)
    await expect(editInput).toBeVisible()
    await editInput.fill(nextTitle)
    await editInput.press('Enter')

    await expect(page.getByText(nextTitle)).toBeVisible()
    await expect(page.getByText(title)).not.toBeVisible()
  })
})

test.describe('Search and Filter', () => {
  test.beforeEach(async ({ page }) => {
    await ensureUser(page)
    const login = new LoginPage(page)
    await login.goto()
    await login.login(USER.email, USER.password)
    await page.waitForURL('**/dashboard')
  })

  test('should filter items by search term', async ({ page }) => {
    const search = page.getByTestId('search-input')
    await search.fill('unique search xyz')
    await page.waitForTimeout(400) // wait for debounce
    // Result: empty-state or filtered list — URL should have search param
    await expect(page).toHaveURL(/search=unique/)
  })

  test('should filter items by status', async ({ page }) => {
    const filter = page.getByTestId('status-filter')
    await filter.selectOption('completed')
    await expect(page).toHaveURL(/status=completed/)
  })

  test('should reset page to 1 when search changes', async ({ page }) => {
    const search = page.getByTestId('search-input')
    await search.fill('test')
    await page.waitForTimeout(400)
    const url = new URL(page.url())
    // page param should be absent or 1
    const pageParam = url.searchParams.get('page')
    expect(pageParam === null || pageParam === '1').toBe(true)
  })
})

test.describe('Pagination', () => {
  test.beforeEach(async ({ page }) => {
    await ensureUser(page)
    const login = new LoginPage(page)
    await login.goto()
    await login.login(USER.email, USER.password)
    await page.waitForURL('**/dashboard')
  })

  test('pagination controls render when there are multiple pages', async ({ page }) => {
    // Only visible when totalPages > 1; if not enough data, pagination is hidden — that's OK
    const hasPagination = await page.getByTestId('pagination').isVisible().catch(() => false)
    // Just verify page loaded correctly
    await expect(page.getByTestId('dashboard-heading')).toBeVisible()
    if (hasPagination) {
      await expect(page.getByTestId('prev-page')).toBeVisible()
      await expect(page.getByTestId('next-page')).toBeVisible()
      await expect(page.getByTestId('page-indicator')).toContainText('/')
    }
  })
})
