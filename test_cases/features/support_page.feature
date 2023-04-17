Feature: SupportPage

Scenario: Verify support page is displayed
Given Home page is open
When Click on support button
Then Verify support page is displayed

Scenario: Verify support options
  Given Home page is open
  When Click on support button
  Then Verify support page is displayed
  And Verify One time support option is displayed
  And Verify monthly support option is displayed

