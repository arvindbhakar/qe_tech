Feature: UserAPI

Scenario: Get user by id
Given Home page is open
When API request get is send with users-single
Then Verify '/api/users/2' is displayed
And Verify status is '200'
And Response contains user id '2'


Scenario: Create new user
Given Home page is open
When API request post is send with post
Then Verify status is '201'
And Response contains user name as 'morpheus'
