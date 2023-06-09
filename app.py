# -*- coding: utf-8 -*-
#Imports
import sys
import fire
import questionary
from pathlib import Path
import csv
import os

from qualifier.utils.fileio import load_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

from qualifier.utils.fileio import save_csv


def load_bank_data():
    csvpath = questionary.text(
        "Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)


def get_applicant_info():
    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text(
        "What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(
        monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(
        loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered


def save_qualifying_loans(qualifying_loans):
    # if no loans were found there is nothing to save so we exit the application
    if len(qualifying_loans) == 0:
        print("No qualifying loans to save, exiting application.")
        return
    # if loans were found provide the option to save them to a csv, asking user for the
    # filepath and filename unless the default location is desired

    # confirm user's desire to save file
    if questionary.confirm("Would you like to save the list of qualifying loans to a csv file?", default=True).ask():
        # confirm if user wants to save file in default location
        if questionary.confirm("Would you like to save the file in the default location? (./qualifying_loans.csv)", default=True).ask():
            result = save_csv(qualifying_loans)
        else:
            # verify desired file location if not the default
            filepath = questionary.text(
                "Please enter the filepath, including both directory path and file name, \n   where you would like to save the loan information. \n   Either absolute or relative filepaths may be used.").ask()
            result = save_csv(qualifying_loans, filepath)
    # if user chooses not to save the file, print a confirmation that no file was saved
    else:
        print(
            "File not saved. Please rerun application if a new file needs to be generated.")

    # print success message if no errors with saving file
    if result:
        print("File successfully saved")
    # print warning message if there was an error when trying to save the file
    else:
        print("Error saving file, please rerun application.")

    print("\n\nThank you for using the application.")


def run():
    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)