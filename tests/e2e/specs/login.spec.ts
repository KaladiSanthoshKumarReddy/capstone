import { test, expect } from '@playwright/test'
import { LoginPage } from '../pages/LoginPage'
import { registerUser } from '../helpers/auth'

const USER = { email: 'login_e2e@capstone.dev', password: 'Test1234!' }

// ---------------------------------------------------------------------------
// UI — static checks, no auth needed
// ---------------------------------------------------------------------------
test.describe('Login Page — UI', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login')
  })

  test('renders Sign In heading', async ({ page }) => {
    const lp = new LoginPage(page)
    await expect(lp.heading).toBeVisible()
  })

  test('shows email input, password input, and login button', async ({ page }) => {
    const lp = new LoginPage(page)
    await expect(lp.emailInput).toBeVisible()
    await expect(lp.passwordInput).toBeVisible()
    await expect(lp.loginButton).toBeVisible()
  })

  test('email input has type=email', async ({ page }) => {
    await expect(page.getByTestId('email-input')).toHaveAttribute('type', 'email')
  })

  test('password input has type=password', async ({ page }) => {
    await expect(page.getByTestId('password-input')).toHaveAttribute('type', 'password')
  })

  test('email and password inputs have required attribute', async ({ page }) => {
    await expect(page.getByTestId('email-input')).toHaveAttribute('required', '')
    await expect(page.getByTestId('password-input')).toHaveAttribute('required', '')
  })

  test('login button label is "Login" initially', async ({ page }) => {
    await expect(page.getByTestId('login-button')).toHaveText('Login')
  })

  test('login button is enabled on initial load', async ({ page }) => {
    await expect(page.getByTestId('login-button')).toBeEnabled()
  })

  test('no error message visible on initial load', async ({ page }) => {
    await expect(page.getByTestId('login-error')).not.toBeVisible()
  })
})

// ---------------------------------------------------------------------------
// Validation — HTML5 constraints prevent submission
// ---------------------------------------------------------------------------
test.describe('Login — Validation', () => {
  test('does not submit with empty email', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    await lp.passwordInput.fill('password123')
    await lp.loginButton.click()
    await expect(page).toHaveURL('/login')
    await expect(lp.errorMessage).not.toBeVisible()
  })

  test('does not submit with empty password', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    await lp.emailInput.fill('test@example.com')
    await lp.loginButton.click()
    await expect(page).toHaveURL('/login')
    await expect(lp.errorMessage).not.toBeVisible()
  })

  test('does not submit with invalid email format', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    await lp.emailInput.fill('not-an-email')
    await lp.passwordInput.fill('password123')
    await lp.loginButton.click()
    await expect(page).toHaveURL('/login')
  })
})

// ---------------------------------------------------------------------------
// Authentication — wrong / correct credentials
// ---------------------------------------------------------------------------
test.describe('Login — Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await registerUser(page, USER.email, USER.password)
  })

  test('shows "Invalid credentials" for unregistered email', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    await lp.login('nobody@capstone.dev', 'Test1234!')
    await expect(lp.errorMessage).toBeVisible()
    await expect(lp.errorMessage).toHaveText('Invalid credentials')
  })

  test('shows "Invalid credentials" for wrong password', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    await lp.login(USER.email, 'WrongPassword!')
    await expect(lp.errorMessage).toBeVisible()
    await expect(lp.errorMessage).toHaveText('Invalid credentials')
  })

  test('error message has red text styling', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    await lp.login('bad@capstone.dev', 'WrongPass99')
    await expect(lp.errorMessage).toHaveClass(/text-red/)
  })

  test('login button shows "Signing in…" and is disabled while submitting', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    await lp.emailInput.fill(USER.email)
    await lp.passwordInput.fill(USER.password)

    // Hold the API response so we can observe the loading state
    await page.route('**/api/auth/login', route =>
      new Promise<void>(resolve => setTimeout(() => resolve(route.continue() as unknown as void), 600)),
    )
    void lp.loginButton.click()
    await expect(lp.loginButton).toBeDisabled()
    await expect(lp.loginButton).toHaveText('Signing in…')
    await page.unrouteAll()
  })

  test('redirects to /dashboard on valid credentials', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    await lp.login(USER.email, USER.password)
    await expect(page).toHaveURL('/dashboard')
  })

  test('stores token in localStorage after login', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    await lp.login(USER.email, USER.password)
    await page.waitForURL('/dashboard')
    const token = await page.evaluate(() => localStorage.getItem('capstone_token'))
    expect(token).toBeTruthy()
  })

  test('stores email in localStorage after login', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    await lp.login(USER.email, USER.password)
    await page.waitForURL('/dashboard')
    const email = await page.evaluate(() => localStorage.getItem('capstone_email'))
    expect(email).toBe(USER.email)
  })

  test('error clears and redirects on successful retry after failure', async ({ page }) => {
    const lp = new LoginPage(page)
    await lp.goto()
    // First attempt — wrong password
    await lp.login(USER.email, 'WrongPass!')
    await expect(lp.errorMessage).toBeVisible()
    // Second attempt — correct
    await lp.emailInput.fill(USER.email)
    await lp.passwordInput.fill(USER.password)
    await lp.loginButton.click()
    await expect(page).toHaveURL('/dashboard')
  })
})

// ---------------------------------------------------------------------------
// Route guards
// ---------------------------------------------------------------------------
test.describe('Login — Route Guards', () => {
  test('visiting /dashboard without token redirects to /login', async ({ page }) => {
    await page.goto('/login')
    await page.evaluate(() => localStorage.clear())
    await page.goto('/dashboard')
    await expect(page).toHaveURL('/login')
  })

  test('visiting / without token redirects to /login via /dashboard', async ({ page }) => {
    await page.goto('/login')
    await page.evaluate(() => localStorage.clear())
    await page.goto('/')
    await expect(page).toHaveURL('/login')
  })

  test('404 route shows NotFound page', async ({ page }) => {
    await page.goto('/this-does-not-exist')
    await expect(page.getByText('404')).toBeVisible()
    await expect(page.getByText('Page not found')).toBeVisible()
  })
})
