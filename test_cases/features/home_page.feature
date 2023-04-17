Feature: HomePage

Scenario Outline: Verify different  request types end points
Given Home page is open
When API request <requestType> is send with <endpoint>
Then Verify '<endpoint_url>' is displayed

  Examples:
    | requestType | endpoint     | endpoint_url          |
    | get         | users        | /api/users?page=2     |
    | get         | users-single | /api/users/2          |


Scenario: Verify API Response Code
Given Home page is open
When API request get is send with users
Then Verify status is '200'

