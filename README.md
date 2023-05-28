# Financial-Applications-with-Python
Challenge 2 - University of Berkeley Financial Technology Boot Camp
## Loan Qualifier Application
The Loan Qualifier Application is a Python-based software that automates the process of comparing the attributes of a potential borrower to the loan offerings of a set of banks. By providing certain financial information, the application determines the borrower's monthly debt to income ratio and loan to value ratio. It then notifies the user of the number of qualifying loans available from the provided list of banks. Additionally, the user has the option to save the list of qualifying loans to a CSV file at a location of their choice.

### Technologies
The Loan Qualifier Application is built using the following technologies:

- Python programming language (version 3.9.15)
- Python libraries:
  - questionary
  - fire
 The required directory structure should be as follows:
```
|-- app.py
|
|-- qualifier
		|
		|-- filters
		|	 |-- credit_score.py
		|	 |-- debt_to_income.py
		|	 |-- loan_to_value.py
		|	 |-- max_loan_size.py
		|
		|-- utils
			 |-- calculators.py
			 |-- fileio.py
```
To run the application, open a terminal and navigate to the root directory of the application. Then execute the following command:
```
python app.py
```
Here is an example of a sample run showing all the prompts and requesting the saving of the lender information to a CSV file:
```
> python app.py
? Enter a file path to a rate-sheet (.csv): ./data/daily_rate_sheet.csv
? What's your credit score? 750
? What's your current amount of monthly debt? 5000
? What's your total monthly income? 35000
? What's your desired loan amount? 5000
? What's your home value? 800000
The monthly debt to income ratio is 0.14
The loan to value ratio is 0.01.
Found 15 qualifying loans
? Would you like to save the list of qualifying loans to a CSV file? Yes
? Would you like to save the file in the default location? (./qualifying_loans.csv) No
? Please enter the filepath, including both directory path and file name,
   where you would like to save the loan information.
   Either absolute or relative filepaths may be used. ./qualifying_loans.csv
File successfully saved

Thank you for using the application.
```
## Files
- The necessary file for this the found in /Data
