Feature: Data load and transformation

Scenario: Verify PositionReport file headers
  Given the CSV file 'test_cases/data/out/PositionReport.csv'
  When I verify the headers:
    | ExpectedHeaders|
    | ID          |
    | PositionID  |
    | ISIN        |
    | Quantity    |
    | Total Price |
  Then the headers should be correct

Scenario: Check the primary key constraint in the PositionReport file
    Given the CSV file 'test_cases/data/out/PositionReport.csv'
    When I check the primary key constraint for column 'ID'
    Then the primary key constraint should be satisfied

Scenario: Verify the content of the position report CSV file
    Given the instrument details are stored in "test_cases/data/in/InstrumentDetails.csv"
    And the position details are stored in "test_cases/data/in/PositionDetails.csv"
    And the position report is stored in "test_cases/data/out/PositionReport.csv"
    When I verify the content of the position report CSV file
    Then the position report CSV file should match the instrument and position details
