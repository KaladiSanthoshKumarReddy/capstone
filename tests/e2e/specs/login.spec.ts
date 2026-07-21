import { test, expect } from '@playwright/test'
import { LoginPage } from '../pages/LoginPage'
import { DashboardPage } from '../pages/DashboardPage'

test.describe('Login Feature', () => {
  test('should display login form', async ({ page }) => {
    const loginPage = new LoginPage(page)
    await loginPage.goto()
    await expect(loginPage.emailInput).toBeVisible()
    await expect(loginPage.passwordInput).toBeVisible()
    await expect(loginPage.loginButton).toBeVisible()
  })

  test('should show error for invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page)
    await loginPage.goto()
    await loginPage.login('wrong@example.com', 'wrongpassword')
    await expect(loginPage.errorMessage).toBeVisible()
    await expect(loginPage.errorMessage).toContainText('Invalid credentials')
  })

  test('should redirect to dashboard on successful login', async ({ page }) => {
    // First register a test user via API
    await page.request.post('http://localhost:4000/api/auth/register', {
      data: { email: 'test@example.com', password: 'password123' },
    })

    const loginPage = new LoginPage(page)
    const dashboardPage = new DashboardPage(page)
    await loginPage.goto()
    await loginPage.login('test@example.com', 'password123')
    await expect(page).toHaveURL('/dashboard')
    await expect(dashboardPage.heading).toBeVisible()
  })
})
