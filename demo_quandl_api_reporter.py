import argparse
from pprint import pprint

from config import QUANDL_API_KEY, DEFAULT_STOCK_CODES, START_DATE, END_DATE
from quandl_reports import ApiQuandlReport

# NOTE: This is a command line util for testing the live API reporting class interactively.
# Reporting tool should be interested with REST API or some other system to maximise usefulness

# Get command line argument
parser = argparse.ArgumentParser()
parser.add_argument("report_name", help="name of the report you want to run")
args = parser.parse_args()

# Valid report names
average_open_close = "average_open_close"
max_daily_profit = "max_daily_profit"
busy_day = "busy_day"
biggest_loser = "biggest_loser"

reports_names = [
    average_open_close,
    max_daily_profit,
    busy_day,
    biggest_loser
]

# Error codes
invalid_report_error = "{user_rpt} Is an invalid report name. Try: {reports}".format(
    user_rpt=args.report_name,
    reports=str(reports_names)
)

# Call the API reporting class
quandl_api = ApiQuandlReport(
    api_key=QUANDL_API_KEY,
    stock_codes=DEFAULT_STOCK_CODES,
    end_date=END_DATE,
    start_date=START_DATE
)

# Run the report selected by the user and pprint it.
# Otherwise, tell the user that they did not select a valid report.
if args.report_name == average_open_close:
    pprint(quandl_api.report_average_open_close())

elif args.report_name == max_daily_profit:
    pprint(quandl_api.report_max_daily_profit())

elif args.report_name == busy_day:
    pprint(quandl_api.report_busy_day())

elif args.report_name == biggest_loser:
    pprint(quandl_api.report_biggest_loser())

else:
    print(invalid_report_error)
