import { Page, Locator } from '@playwright/test'

export class DashboardPage {
  readonly page: Page
  readonly heading: Locator

  constructor(page: Page) {
    this.page = page
    this.heading = page.getByTestId('dashboard-heading')
  }

  async goto() {
    await this.page.goto('/dashboard')
  }
}
