from unittest import (
    TestCase,
    TestLoader,
    TextTestRunner,
    skip
)

from config import (
    DEFAULT_STOCK_CODES,
    START_DATE,
    END_DATE,
    QUANDL_API_KEY
)

from quandl_reports import CsvQuandlReport, ApiQuandlReport

from test_results_fixtures import (
    default_open_close_report,
    default_max_daily_profit_report,
    default_busy_day_report,
    default_biggest_loser_report
)

# NOTE: CSV and API reports both return the same expected_results.
# TestCases run all four top level reporting methods for both quandl child classes.
# Both TestCase use the same expected result fixtures, showing the both reporting methods (API & CSV) produce the
# same result.


class DefaultStockCodeCsvReportsTestCase(TestCase):

    def setUp(self):
        self.default_prices_data_file = "default_stock_codes_data.csv"

    def test_average_open_close_report(self):
        expected_results = default_open_close_report
        report = CsvQuandlReport(
            filename=self.default_prices_data_file,
            stock_codes=DEFAULT_STOCK_CODES,
            end_date=END_DATE,
            start_date=START_DATE
        )
        report_results = report.report_average_open_close()
        self.assertEqual(report_results, expected_results)

    def test_max_daily_profit_report(self):
        expected_results = default_max_daily_profit_report
        report = CsvQuandlReport(
            filename=self.default_prices_data_file,
            stock_codes=DEFAULT_STOCK_CODES,
            end_date=END_DATE,
            start_date=START_DATE
        )
        report_results = report.report_max_daily_profit()
        self.assertEqual(report_results, expected_results)

    def test_busy_day_report(self):
        expected_results = default_busy_day_report
        report = CsvQuandlReport(
            filename=self.default_prices_data_file,
            stock_codes=DEFAULT_STOCK_CODES,
            end_date=END_DATE,
            start_date=START_DATE
        )
        report_results = report.report_busy_day()
        self.assertEqual(report_results, expected_results)

    def test_biggest_loser_report(self):
        expected_results = default_biggest_loser_report
        report = CsvQuandlReport(
            filename=self.default_prices_data_file,
            stock_codes=DEFAULT_STOCK_CODES,
            end_date=END_DATE,
            start_date=START_DATE
        )
        report_results = report.report_biggest_loser()
        self.assertEqual(report_results, expected_results)


class DefaultStockCodeApiReportsTestCase(TestCase):

    def setUp(self):
        self.api_key = QUANDL_API_KEY
        # TODO: Setup mocks with unittest.mock; ensures code handles expected api calls without calling live api.

    @skip("passed last time with live call")
    def test_average_open_close_report(self):
        expected_results = default_open_close_report
        report = ApiQuandlReport(
            api_key=self.api_key,
            stock_codes=DEFAULT_STOCK_CODES,
            end_date=END_DATE,
            start_date=START_DATE
        )
        report_results = report.report_average_open_close()
        self.assertEqual(report_results, expected_results)

    @skip("passed last time with live call")
    def test_max_daily_profit_report(self):
        expected_results = default_max_daily_profit_report
        report = ApiQuandlReport(
            api_key=self.api_key,
            stock_codes=DEFAULT_STOCK_CODES,
            end_date=END_DATE,
            start_date=START_DATE
        )
        report_results = report.report_max_daily_profit()
        self.assertEqual(report_results, expected_results)

    @skip("passed last time with live call")
    def test_busy_day_report(self):
        expected_results = default_busy_day_report
        report = ApiQuandlReport(
            api_key=self.api_key,
            stock_codes=DEFAULT_STOCK_CODES,
            end_date=END_DATE,
            start_date=START_DATE
        )
        report_results = report.report_busy_day()
        self.assertEqual(report_results, expected_results)

    @skip("passed last time with live call")
    def test_biggest_loser_report(self):
        expected_results = default_biggest_loser_report
        report = ApiQuandlReport(
            api_key=self.api_key,
            stock_codes=DEFAULT_STOCK_CODES,
            end_date=END_DATE,
            start_date=START_DATE
        )
        report_results = report.report_biggest_loser()
        self.assertEqual(report_results, expected_results)


default_csv_test_suite = TestLoader().loadTestsFromTestCase(DefaultStockCodeCsvReportsTestCase)
TextTestRunner(verbosity=2).run(default_csv_test_suite)

default_api_test_suite = TestLoader().loadTestsFromTestCase(DefaultStockCodeApiReportsTestCase)
TextTestRunner(verbosity=2).run(default_api_test_suite)
