import { test, expect } from '@playwright/test'
import { DashboardPage } from '../pages/DashboardPage'

test.describe('Dashboard Feature', () => {
  test('should display dashboard heading', async ({ page }) => {
    const dashboardPage = new DashboardPage(page)
    await dashboardPage.goto()
    await expect(dashboardPage.heading).toBeVisible()
    await expect(dashboardPage.heading).toContainText('Dashboard')
  })

  test('should have correct page title', async ({ page }) => {
    await page.goto('/dashboard')
    await expect(page).toHaveTitle(/Capstone/)
  })
})
