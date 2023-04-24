import pandas as pd


def verify_csv_headers(csv_file_path, expected_headers):
    """
    Verifies that the CSV file at the given path has the expected headers.
    """
    df = pd.read_csv(csv_file_path)
    actual_headers = list(df.columns)
    if actual_headers != expected_headers:
        return False
    return True


def check_primary_key(csv_file_path, primary_key):
    """
    Checks if the specified column in a CSV file contains unique values (i.e., is a primary key).
    """
    df = pd.read_csv(csv_file_path)
    if df[primary_key].duplicated().any():
        return False
    return True


def check_constraints(primary_file_path, primary_key, secondary_file_path, secondary_key):
    """
    Checks the primary and secondary key constraints between two CSV files.
    """
    primary_df = pd.read_csv(primary_file_path)
    secondary_df = pd.read_csv(secondary_file_path)

    # Check primary key constraint
    if primary_df[primary_key].duplicated().any():
        return False

    # Check secondary key constraint
    if not secondary_df[secondary_key].isin(primary_df[primary_key]).all() or secondary_df[
        secondary_key].duplicated().any():
        return False

    return True


def get_column_values(csv_file_path, column_name):
    """
    Reads a specific column from a CSV file and returns its values as a list.
    """
    df = pd.read_csv(csv_file_path, usecols=[column_name])
    return df[column_name].tolist()

