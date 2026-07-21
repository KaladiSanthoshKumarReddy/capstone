Feature: Item Management
  As a logged-in user
  I want to manage items
  So that I can track work across the application

  Background:
    Given I am logged in as "test@example.com"
    And I am on the dashboard

  Scenario: Create a new item
    When I click "Add Item"
    And I fill in title "My First Item"
    And I submit the form
    Then the item "My First Item" should appear in the list

  Scenario: Delete an item
    Given an item "Test Item" exists
    When I click delete on "Test Item"
    Then "Test Item" should be removed from the list

  Scenario: View empty state
    Given no items exist
    Then I should see the empty state message
