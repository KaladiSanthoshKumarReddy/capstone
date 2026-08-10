Feature: Item Priority
  As a logged-in user
  I want to set a priority on an item
  So that I can triage work effectively

  Background:
    Given the application is running on "http://localhost:3000"
    And I am logged in as "priority_test@capstone.dev"

  Scenario: Happy path — create an item with priority
    When I enter title "Urgent Task"
    And I select priority "High"
    And I click "Add Item"
    Then I should see an item "Urgent Task" with priority "High"

  Scenario: Error path — reject invalid priority
    When I create an item with title "Bad priority Item" and priority "CRITICAL"
    Then I should see an error message "Invalid priority"
