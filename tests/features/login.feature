Feature: User Login
  As a registered user
  I want to log into the application
  So that I can access my dashboard

  Background:
    Given the application is running on "http://localhost:3000"

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter email "test@example.com" and password "password123"
    And I click the Login button
    Then I should be redirected to "/dashboard"
    And I should see the dashboard heading

  Scenario: Failed login with invalid credentials
    Given I am on the login page
    When I enter email "wrong@example.com" and password "wrongpass"
    And I click the Login button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page

  Scenario: Login form validation — empty fields
    Given I am on the login page
    When I click the Login button without filling in any fields
    Then the form should not be submitted
