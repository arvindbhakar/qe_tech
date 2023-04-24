Feature: Data load and transformation

Scenario: Verify PositionReport file headers
  Given the CSV file '../data/out/PositionReport.csv'
  When I verify the headers:
    | ID          |
    | PositionID  |
    | ISIN        |
    | Quantity    |
    | Total Price |
  Then the headers should be correct

Scenario: Check the primary key constraint in the PositionReport file
    Given the CSV file 'PositionReport.csv'
    When I check the primary key constraint for column 'ID'
    Then the primary key constraint should be satisfied

Scenario: Verify primary and secondary key constraints across two CSV files
    Given the CSV file 'PositionReport.csv'
    Given the primary key column 'ID' in the CSV file '../data/in/InstrumentDetails.csv'
    And the secondary key column "Id2" in the CSV file '../data/out/PositionReport.csv'
    When I verify the primary and secondary key constraints
    Then the data in the CSV files should be consistent

Scenario: Verify data in a CSV file
    Given the CSV file '../data/out/PositionReport.csv'
    When I load the data from the CSV file
    Then the data should contain the following:
    |ID	    |PositionID	  |ISIN	    |Quantity	|Total Price|
    |PR001	|P001	      |IS001	|10	        |80         |
    |PR002	|P002	      |IS002	|6	        |60         |
    |PR003	|P003	      |IS003	|4	        |60         |
    |PR004	|P004	      |IS004	|5	        |40         |
    |PR005	|P005	      |IS001	|2	        |20         |
