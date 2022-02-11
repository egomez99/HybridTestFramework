@web @search
Feature: User valid search. In order to verify the user is able to search.
    As a web user,
    I want to find information online.

  Scenario: Verify user search in google
    Given I am on Google Homepage
    When I search for "python"
    Then I check results for "python"

