@login
Feature: User valid login. In order to verify the authentication is working. Use IBM credentials

    Scenario: Verify user validation authentication
      Given I am on ibm homepage
      When I wait for the page to load
      #And I fill in the following:
      #  | user-name | pass |
      #And I press "continue-button"
      #And I wait for the page to load
      #Then the response is success