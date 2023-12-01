""""
Tracking Plan from Google Sheet

Code sample: import your tracking plan from Google Sheet. Tracking plan can have several
tests cases (one tab each). See gspread documentation (https://gspread.readthedocs.io/) 
for authentication.
Demo spreadsheet is here: https://docs.google.com/spreadsheets/d/1Kd68s3vLrBqtMDW-PaALZF-5bTm-4J450YbJ3NTbZjQ
"""
import gaunit

import gspread
from os.path import join, dirname, realpath

# authentication. Method is up to you ; see gspread documentation.
gc = gspread.service_account(filename="service_account.json")

# open demo file and import tracking plan for our test case.
gsheet = gc.open_by_key("1Kd68s3vLrBqtMDW-PaALZF-5bTm-4J450YbJ3NTbZjQ")
tracking_plan = gaunit.TrackingPlan.from_spreadsheet(gsheet)
print(
    "expected events:\n%s"
    % tracking_plan.get_expected_events("ga_demo_store_add_to_cart")
)

# check GA events in a HAR file against tracking plan and print results
har_path = join(dirname(realpath(__file__)), "demo_store_add_to_cart.har")
r = gaunit.check_har("ga_demo_store_add_to_cart", tracking_plan, har_path=har_path)
print(r.was_successful())
# TODO fix numbers (param pr1pr)
