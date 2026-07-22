import { test, expect } from '@playwright/test'
import { DashboardPage } from '../pages/DashboardPage'
import { registerUser, loginViaApi } from '../helpers/auth'

const USER = { email: 'dash_e2e@capstone.dev', password: 'Test1234!' }

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
async function authenticate(page: Parameters<typeof loginViaApi>[0]) {
  await registerUser(page, USER.email, USER.password)
  await loginViaApi(page, USER.email, USER.password)
}

// ---------------------------------------------------------------------------
// Auth guard — no login required
// ---------------------------------------------------------------------------
test.describe('Dashboard — Auth Guard', () => {
  test('unauthenticated user is redirected to /login', async ({ page }) => {
    await page.goto('/login')
    await page.evaluate(() => localStorage.clear())
    await page.goto('/dashboard')
    await expect(page).toHaveURL('/login')
  })

  test('authenticated user can access /dashboard', async ({ page }) => {
    await authenticate(page)
    await page.goto('/dashboard')
    await expect(page).toHaveURL('/dashboard')
  })
})

// ---------------------------------------------------------------------------
// Layout — all visible elements after login
// ---------------------------------------------------------------------------
test.describe('Dashboard — Layout', () => {
  test.beforeEach(async ({ page }) => {
    await authenticate(page)
    await page.goto('/dashboard')
    const dash = new DashboardPage(page)
    await dash.waitForLoad()
  })

  test('shows "My Items" heading', async ({ page }) => {
    const dash = new DashboardPage(page)
    await expect(dash.heading).toHaveText('My Items')
  })

  test('shows item count subtitle', async ({ page }) => {
    await expect(page.locator('text=/\\d+ items? total/')).toBeVisible()
  })

  test('shows "Capstone App" navbar brand', async ({ page }) => {
    const dash = new DashboardPage(page)
    await expect(dash.navBrand).toBeVisible()
  })

  test('shows logged-in email in navbar', async ({ page }) => {
    const dash = new DashboardPage(page)
    await expect(dash.navEmail).toBeVisible()
    await expect(dash.navEmail).toHaveText(USER.email)
  })

  test('shows Logout button in navbar', async ({ page }) => {
    const dash = new DashboardPage(page)
    await expect(dash.logoutButton).toBeVisible()
    await expect(dash.logoutButton).toHaveText('Logout')
  })

  test('shows item title input', async ({ page }) => {
    const dash = new DashboardPage(page)
    await expect(dash.itemTitleInput).toBeVisible()
    await expect(dash.itemTitleInput).toHaveAttribute('placeholder', 'Title *')
  })

  test('shows optional description input', async ({ page }) => {
    const dash = new DashboardPage(page)
    await expect(dash.itemDescInput).toBeVisible()
  })

  test('add item button is disabled when title is empty', async ({ page }) => {
    const dash = new DashboardPage(page)
    await expect(dash.addItemButton).toBeDisabled()
  })

  test('add item button enables when title is filled', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.itemTitleInput.fill('Something')
    await expect(dash.addItemButton).toBeEnabled()
  })

  test('shows search input with correct placeholder', async ({ page }) => {
    const dash = new DashboardPage(page)
    await expect(dash.searchInput).toBeVisible()
    await expect(dash.searchInput).toHaveAttribute('placeholder', 'Search items…')
  })

  test('shows status filter dropdown', async ({ page }) => {
    const dash = new DashboardPage(page)
    await expect(dash.statusFilter).toBeVisible()
  })

  test('status filter has All / Active / Completed / Archived options', async ({ page }) => {
    const options = await page
      .getByTestId('status-filter')
      .locator('option')
      .allTextContents()
    expect(options).toEqual(['All Statuses', 'Active', 'Completed', 'Archived'])
  })

  test('shows empty state or item list — no perpetual loading', async ({ page }) => {
    const dash = new DashboardPage(page)
    await expect(dash.loadingState).not.toBeVisible({ timeout: 6000 })
    const hasItems = await dash.itemList.isVisible()
    const isEmpty  = await dash.emptyState.isVisible()
    expect(hasItems || isEmpty).toBe(true)
  })
})

// ---------------------------------------------------------------------------
// Logout flow
// ---------------------------------------------------------------------------
test.describe('Dashboard — Logout', () => {
  test.beforeEach(async ({ page }) => {
    await authenticate(page)
    await page.goto('/dashboard')
    await new DashboardPage(page).waitForLoad()
  })

  test('clicking Logout redirects to /login', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.logoutButton.click()
    await expect(page).toHaveURL('/login')
  })

  test('after logout, /dashboard redirects to /login', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.logoutButton.click()
    await page.waitForURL('/login')
    await page.goto('/dashboard')
    await expect(page).toHaveURL('/login')
  })

  test('token is removed from localStorage after logout', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.logoutButton.click()
    await page.waitForURL('/login')
    const token = await page.evaluate(() => localStorage.getItem('capstone_token'))
    expect(token).toBeNull()
  })

  test('email is removed from localStorage after logout', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.logoutButton.click()
    await page.waitForURL('/login')
    const email = await page.evaluate(() => localStorage.getItem('capstone_email'))
    expect(email).toBeNull()
  })
})

// ---------------------------------------------------------------------------
// Add / search / filter — functional interactions
// ---------------------------------------------------------------------------
test.describe('Dashboard — Item Interactions', () => {
  test.beforeEach(async ({ page }) => {
    await authenticate(page)
    await page.goto('/dashboard')
    await new DashboardPage(page).waitForLoad()
  })

  test('adds a new item and clears title input', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.itemTitleInput.fill('E2E Dashboard Item')
    await dash.addItemButton.click()
    await expect(page.getByText('E2E Dashboard Item')).toBeVisible()
    await expect(dash.itemTitleInput).toHaveValue('')
  })

  test('newly added item has "active" status badge', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.itemTitleInput.fill('Status Badge Test')
    await dash.addItemButton.click()
    // Find the card and check its status badge
    const badge = page
      .locator('[data-testid^="item-status-"]')
      .filter({ hasText: 'active' })
      .first()
    await expect(badge).toBeVisible()
  })

  test('search input syncs to URL ?search= param after debounce', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.searchInput.fill('uniquequery')
    await page.waitForURL(/search=uniquequery/, { timeout: 1500 })
    await expect(page).toHaveURL(/search=uniquequery/)
  })

  test('status filter syncs to URL ?status= param', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.statusFilter.selectOption('completed')
    await expect(page).toHaveURL(/status=completed/)
  })

  test('changing status filter resets page to 1', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.statusFilter.selectOption('active')
    const url = new URL(page.url())
    const pageParam = url.searchParams.get('page')
    expect(pageParam === null || pageParam === '1').toBe(true)
  })

  test('empty state appears when search matches nothing', async ({ page }) => {
    const dash = new DashboardPage(page)
    await dash.searchInput.fill('xzxzxz-no-match-at-all')
    await page.waitForURL(/search=xzxzxz/, { timeout: 1500 })
    await expect(dash.emptyState).toBeVisible()
    await expect(dash.emptyState).toContainText('No items found')
  })

  test('can delete an item', async ({ page }) => {
    const dash = new DashboardPage(page)
    const title = `Delete Me ${Date.now()}`
    await dash.itemTitleInput.fill(title)
    await dash.addItemButton.click()
    await expect(page.getByText(title)).toBeVisible()

    const deleteBtn = page.locator('[data-testid^="item-delete-"]').first()
    page.once('dialog', d => d.accept())
    await deleteBtn.click()
    await expect(page.getByText(title)).not.toBeVisible()
  })

  test('can toggle item status to completed', async ({ page }) => {
    const dash = new DashboardPage(page)
    const title = `Toggle Status Test ${Date.now()}`
    await dash.itemTitleInput.fill(title)
    await dash.addItemButton.click()
    await expect(page.getByText(title)).toBeVisible()

    const titleEl = page.locator('[data-testid^="item-title-"]').filter({ hasText: title }).first()
    const titleTestId = await titleEl.getAttribute('data-testid')
    const id = titleTestId?.replace('item-title-', '')
    expect(id).toBeTruthy()

    const toggle = page.locator(`[data-testid="item-toggle-${id}"]`)
    await toggle.click()
    const badge = page.locator(`[data-testid="item-status-${id}"]`)
    await expect(badge).toHaveText('completed')
  })

  test('can inline-edit item title', async ({ page }) => {
    const dash = new DashboardPage(page)
    const title = `Original Title ${Date.now()}`
    const nextTitle = `Updated Title ${Date.now()}`
    await dash.itemTitleInput.fill(title)
    await dash.addItemButton.click()
    await expect(page.getByText(title)).toBeVisible()

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

  test('pressing Escape cancels inline edit without saving', async ({ page }) => {
    const dash = new DashboardPage(page)
    const title = `No Change Title ${Date.now()}`
    await dash.itemTitleInput.fill(title)
    await dash.addItemButton.click()
    await expect(page.getByText(title)).toBeVisible()

    const titleEl = page.locator('[data-testid^="item-title-"]').filter({ hasText: title }).first()
    const titleTestId = await titleEl.getAttribute('data-testid')
    const id = titleTestId?.replace('item-title-', '')
    expect(id).toBeTruthy()

    await titleEl.click()
    const editInput = page.locator(`[data-testid="item-edit-input-${id}"]`)
    await expect(editInput).toBeVisible()
    await editInput.fill('Abandoned Edit')
    await editInput.press('Escape')

    await expect(page.getByText(title)).toBeVisible()
    await expect(page.getByText('Abandoned Edit')).not.toBeVisible()
  })
})
