from config import DEFAULT_STOCK_CODES, START_DATE, END_DATE
from quandl_reports import CsvQuandlReport
from pprint import pprint

filename = "default_stock_codes_data.csv"
report = CsvQuandlReport(
    filename=filename,
    stock_codes=DEFAULT_STOCK_CODES,
    end_date=END_DATE,
    start_date=START_DATE
)
report_results = report.report_average_open_close()
pprint(report_results)
# ~47 secs with full data 3/3/2018
