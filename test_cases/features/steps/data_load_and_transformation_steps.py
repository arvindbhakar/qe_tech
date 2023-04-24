import os

from behave import *
import pandas as pd

from utils.csv_util import verify_csv_headers, check_primary_key


@given("the CSV file '{csv_file_path}'")
def step_impl(context, csv_file_path):
    file_path = os.path.abspath(csv_file_path)
    context.csv_file_path = file_path


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


@given('the instrument details are stored in "{filename}"')
def step_impl(context, filename):
    context.instrument_df = pd.read_csv(filename)


@given('the position details are stored in "{filename}"')
def step_impl(context, filename):
    context.position_df = pd.read_csv(filename)


@given('the position report is stored in "{filename}"')
def step_impl(context, filename):
    context.position_report_df = pd.read_csv(filename)


@when('I verify the content of the position report CSV file')
def step_impl(context):
    merged_df = pd.merge(context.instrument_df, context.position_df, left_on='ID', right_on='InstrumentID')
    merged_df = merged_df.rename(columns={'ID_y': 'PositionID'})
    print("merged pf")
    print(merged_df)
    #final_df = pd.merge(merged_df, context.position_report_df, left_on='InstrumentID', right_on='ISIN')
    final_df = pd.merge(merged_df, context.position_report_df, left_on='PositionID', right_on='PositionID')
    print("final_df pf")
    print(final_df)
    final_df['Calculated Total Price'] = merged_df['Quantity'] * merged_df['Unit Price']
    print("final_df['Calculated Total Price'")
    print(final_df['Calculated Total Price'])
    print("final_df['Total Price']")
    print(final_df['Total Price'])
    final_df['Total Price Matches'] = final_df['Total Price'] == final_df['Calculated Total Price']
    context.final_df = final_df


@then('the position report CSV file should match the instrument and position details')
def step_impl(context):
    assert context.final_df['Total Price Matches'].all()
