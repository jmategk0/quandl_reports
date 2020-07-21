import pandas as pd
import quandl

from config import PRICES_DATATABLE_CODE, QUANDL_API_KEY
from price_table_columns import (
    PRICES_COLUMNS_TO_KEEP,
    PRICES_COLUMNS_TO_DROP,
    OPEN_COL,
    CLOSE_COL,
    HIGH_COL,
    LOW_COL,
    VOLUME_COL,
    TICKER_COL,
    DATE_COL,
)

quandl.ApiConfig.api_key = QUANDL_API_KEY

# We define one base call with all the pandas reporting logic
# Each child class implements a method to populate the dataframe
# from a csv file or a live api call


class BaseQuandlReport(object):
    def __init__(self, stock_codes, start_date, end_date):
        """
        This is the Base Class for all Quandl reporting tools.

        All child classes must implement the populate_dataframe method
        to populate the self.df property. self.df is used as the raw dataset
        for all reporting methods.

        All reporting is implemented in the baseclass and works under
        the assumption that child classes are successfully populated 
        self.df with a valid dataframe.
        
        pandas dataframe processing in central to all reporting workflows.

        :param stock_codes: A list of stock ticker codes (strings)
        :param start_date: A string formatted date, at the start of a range
        :param end_date: A string formatted date, at the end of a range
        """

        self.stock_codes = stock_codes
        self.start_date = start_date
        self.end_date = end_date
        self.df = pd.DataFrame()  # Used to store raw data from source

    def populate_dataframe(self):
        # Child classes must implement this method
        # Result must populate self.df otherwise reporting code will fail.
        raise NotImplementedError

    def get_stock_open_close(self, stock_code, time_period="M", round_precision=2):
        """
        This report will filter self.df by stock code, 
        then calculate the average open price and close price for each month in a year.
        
        :param stock_code: a single stock ticker code, string 
        :param time_period: a pandas dataframe time_period to group by.
        :param round_precision: round digits
        :return: A json serializable list of dicts with report values
        """
        stock_results = []

        # Filter the dataframe on stock code
        stock_df = self.df[self.df.ticker == stock_code]

        # group by open and close prices for time period
        group_by_period_and_open = stock_df[OPEN_COL].groupby(
            by=stock_df.date.dt.to_period(time_period)
        )
        group_by_period_and_close = stock_df[CLOSE_COL].groupby(
            by=stock_df.date.dt.to_period(time_period)
        )

        # get the mean open and close
        open_means = dict(group_by_period_and_open.mean())
        close_means = dict(group_by_period_and_close.mean())

        # load up reporting format
        for year_mo_key in open_means:
            row = {
                "month": str(year_mo_key),
                "average_open": round(open_means[year_mo_key], round_precision),
                "average_close": round(close_means[year_mo_key], round_precision),
            }
            stock_results.append(row)

        return stock_results

    def get_max_daily_profit(self, stock_code, round_precision=2):
        """
        This method returns max daily profit for a stock. Calculation is based 
        on the difference between daily high and low.
        
        Known Issues: Pandas warning =
        'A value is trying to be set on a copy of a slice from a DataFrame.
        Try using .loc[row_indexer,col_indexer] = value instead'


        :param stock_code: a single stock ticker code, string
        :param round_precision: round digits
        :return: A json serializable list of dicts with report values
        """

        # step1: filter the df
        df_for_profit = self.df[self.df.ticker == stock_code]

        # step2: modify the df
        df_for_profit["daily_profit"] = df_for_profit[HIGH_COL] - df_for_profit[LOW_COL]

        # step3: profit
        # TODO: resolve pandas warning from this line
        max_daily_profit = df_for_profit.loc[df_for_profit["daily_profit"].idxmax()]

        # load report format
        results = {
            "ticker": max_daily_profit.ticker,
            "date": str(max_daily_profit.date.date()),
            "daily_profit": round(max_daily_profit.daily_profit, round_precision),
        }
        return results

    def get_busy_day(self, stock_code, report_limit=0.1, round_precision=2):
        """
        This method finds all the days where daily volume was X% above average volume.
        In our case we define X as 10% by default.
        
        Note: These results can be large. 
        
        :param stock_code: a single stock ticker code, string
        :param report_limit: reporting limit for defining a busy day.
        :param round_precision: round digits
        :return: A json serializable list of dicts with report values
        """

        results = []

        # filter the dataframe
        stock_df = self.df[self.df.ticker == stock_code]

        # Calculate mean volume and reporting limit
        mean_volume = stock_df[VOLUME_COL].mean()
        rate_amount = mean_volume * report_limit
        limit = mean_volume + rate_amount

        # filter only the busy days from the stock dataframe
        df_busy = stock_df[stock_df.volume > limit]

        # loop over dataframe and prep the report format.
        for index, row in df_busy.iterrows():
            result = {
                "ticker": row[TICKER_COL],
                "date": str(row[DATE_COL].date()),
                "average_volume": round(mean_volume, round_precision),
                "volume": round(row[VOLUME_COL], round_precision),
            }
            results.append(result)

        return results

    def get_biggest_loser(self, stock_code):
        """
        This method count the number of days a stocks close was lower than its open price.

        :param stock_code: a single stock ticker code, string
        :return: A json serializable list of dicts with report values
        """
        # Filter dataframe
        stock_df = self.df[self.df.ticker == stock_code]
        df_loser = stock_df[stock_df.close < stock_df.open]
        # report results, df.shape is the quickest way to get a row count
        results = {"ticker": stock_code, "number_of_days": df_loser.shape[0]}
        return results

    def report_average_open_close(self):
        """
        Report average_open_close for each stock ticker code in the
        objects stock code list.

        :return: A json serializable dicts with report values for each stock code
        """
        report_results = {}

        for stock in self.stock_codes:
            report_results[stock] = self.get_stock_open_close(stock_code=stock)
        return report_results

    def report_max_daily_profit(self):
        """
        Report max_daily_profit for each stock ticker code in the
        objects stock code list.

        :return: A json serializable dicts with report values for each stock code
        """
        report_results = {}

        for stock in self.stock_codes:
            report_results[stock] = self.get_max_daily_profit(stock_code=stock)
        return report_results

    def report_busy_day(self):
        """
        Report busy_day for each stock ticker code in the
        objects stock code list.

        :return: A json serializable dicts with report values for each stock code
        """
        report_results = {}

        for stock in self.stock_codes:
            report_results[stock] = self.get_busy_day(stock_code=stock)
        return report_results

    def report_biggest_loser(self):
        """
        Report biggest_loser for each stock ticker code in the
        objects stock code list.

        This method loads results into another dataframe to find the max days between all 
        stock codes.

        :return: A json serializable dict with report values for each stock code
        """
        report_results = []

        for stock in self.stock_codes:
            report_results.append(self.get_biggest_loser(stock_code=stock))
        df_results = pd.DataFrame(report_results)
        biggest_loser = df_results.loc[df_results["number_of_days"].idxmax()]
        return dict(biggest_loser)


class ApiQuandlReport(BaseQuandlReport):
    def __init__(self, api_key, stock_codes, start_date, end_date):
        """
        This child reporting class is used for populating a dataframe from
        the official python wrapper for the quandl rest api.

        All results are returned as pandas daraframes.

        :param api_key: quandl api key value
        :param stock_codes: A list of stock ticker codes (strings)
        :param start_date: A string formatted date, at the start of a range
        :param end_date: A string formatted date, at the end of a range
        """

        super().__init__(stock_codes, start_date, end_date)
        self.api_key = api_key
        self.PRICES_DATATABLE_CODE = PRICES_DATATABLE_CODE  # database name
        self.populate_dataframe()

    def populate_dataframe(self):
        """
        populate dataframe using quandl rest api wrapper.
        api qry filters on stock code list, date range, and columns to include.
        
        :return: dataframe for self.df
        """

        self.df = quandl.get_table(
            datatable_code=self.PRICES_DATATABLE_CODE,
            ticker=self.stock_codes,
            date={"gte": self.start_date, "lte": self.end_date},
            qopts={"columns": PRICES_COLUMNS_TO_KEEP},
        )


class CsvQuandlReport(BaseQuandlReport):
    def __init__(self, filename, stock_codes, start_date, end_date):
        """
        This child reporting class is used for populating a dataframe from
        csv output from quandl.

        All results are returned as pandas daraframes.
        
        :param filename: full filepath to a csv file with quandl data export
        :param stock_codes: A list of stock ticker codes (strings)
        :param start_date: A string formatted data, at the start of a range
        :param end_date: A string formatted date, at the end of a range
        """

        super().__init__(stock_codes, start_date, end_date)
        self.filename = filename
        self.populate_dataframe()

    def populate_dataframe(self):
        """
        populate dataframe using quandl csv export. 
        dataframe filters on stock code list, date range, and columns to include.

        :return: dataframe for self.df
        """
        raw_df = pd.read_csv(filepath_or_buffer=self.filename, parse_dates=["date"])
        df_filtered_by_code = raw_df[raw_df.ticker.isin(self.stock_codes)]
        df_filtered_by_date = df_filtered_by_code[
            (df_filtered_by_code.date >= self.start_date)
            & (df_filtered_by_code.date <= self.end_date)
        ]
        self.df = df_filtered_by_date.drop(PRICES_COLUMNS_TO_DROP, axis=1)
