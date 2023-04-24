from behave import *
import pandas as pd

from utils.csv_util import verify_csv_headers, check_primary_key


@given("the CSV file '{csv_file_path}'")
def step_impl(context, csv_file_path):
    context.csv_file_path = csv_file_path


@when("I verify the headers")
def step_impl(context):
    expected_headers = [row[0] for row in context.table]
    headers_are_correct = verify_csv_headers(context.csv_file_path, expected_headers)
    context.headers_are_correct = headers_are_correct


@then("the headers should be correct")
def step_impl(context):
    assert context.headers_are_correct, "CSV file headers are incorrect."


@when("I check the primary key constraint for column '{col}'")
def step_impl(context, col):
    context.is_primary_key = check_primary_key(context.csv_file_path, col)


@then("the primary key constraint should be satisfied")
def verify_primary_key_constraint(context):
    assert context.is_primary_key, "The column is not a primary key"


@given('the primary key column "{column}" in the CSV file "{file}"')
def step_impl(context, column, file):
    context.primary_key = column
    context.df1 = pd.read_csv(file)


@given('the secondary key column "{column}" in the CSV file "{file}"')
def step_impl(context, column, file):
    context.secondary_key = column
    context.df2 = pd.read_csv(file)


@when('I verify the primary and secondary key constraints')
def step_impl(context):
    assert context.primary_key in context.df1.columns, f"{context.primary_key} is not in {context.df1.columns}"
    # Check if the secondary key column exists in the DataFrame
    assert context.secondary_key in context.df2.columns, f"{context.secondary_key} is not in {context.df2.columns}"
    # Check if there are any duplicate primary key values in the DataFrame
    assert not context.df1.duplicated(
        subset=context.primary_key).any(), f"Duplicate {context.primary_key} values found in file1.csv"
    # Check if there are any duplicate secondary key values in the DataFrame
    assert not context.df2.duplicated(
        subset=context.secondary_key).any(), f"Duplicate {context.secondary_key} values found in file2.csv"


@then('the data in the CSV files should be consistent')
def step_impl(context):
    # Merge the two DataFrames on the primary and secondary key columns
    merged_df = pd.merge(context.df1, context.df2, on=[context.primary_key, context.secondary_key], how='outer')
    # Check if any rows are missing from the merged DataFrame
    assert merged_df.notnull().all().all(), "Data is inconsistent between the CSV files"
