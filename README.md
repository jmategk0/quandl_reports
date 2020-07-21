###Introduction: Quandl API Demo

Quandl is a market place for financial and economic data, and has very robust API offerings.
For python developers this is convenient because the pip package pulls the rest api and converts 
it to pandas dataframes, so its very easy to use. You can also download whole datasets in csv
format.

This project is a demo for reporting on stock price data from quandl using pandas. 
Data may be ingested via rest api calls or by bulk operations on csv file exports. The core 
reporting is done by importing the raw data into pandas dataframes tooling to 
produce reports in a json serializable format. These report results can be easily plugged into
another system, such as a rest api or a data visualization tool.

##Four reports are supported
1. average_open_close: average open and closing price for stocks
2. max_daily_profit: max daily profit base on daily high/low for stocks
3. busy_day: number of days where the stocks volume was 10% above average 
4. biggest_loser: number of days where a stocks close price was lower than its open price

## Setup the config file
A config file is needed to run this code. Most critical is that you
must populate `QUANDL_API_KEY` with a valid API key. You will need
to make a free account https://www.quandl.com/ to get a API key.

You can also update the list of stocks used for reporting 
`DEFAULT_STOCK_CODES` and the date ranges.

##Setup Local
1. create a new virtualenv
2. pip install requirements.txt
3. plug in your api key in config.py

NOTE: Only supported on python 3.6+ and Ubuntu 18.04+

##Setup with Docker
Run one of the following commands and the image will build

Run Reports & Tests
1. Run Reports Live (four reports supported)

`docker-compose run --rm quandl python demo_quandl_api_reporter.py average_open_close`

`docker-compose run --rm quandl python demo_quandl_api_reporter.py max_daily_profit`

`docker-compose run --rm quandl python demo_quandl_api_reporter.py busy_day`

`docker-compose run --rm quandl python demo_quandl_api_reporter.py biggest_loser`

2. Run Tests

`docker-compose run --rm quandl python test_reports.py` 

## TODO and Future Work
1. Improve tests
2. resolve pandas warning
3. optimize pandas code
4. Add rest api
5. Add data visualizations with pygal or D3
6. Add real UI with ReactJS

###Notes on Performance:

Reporting Code was tested on full quandl data export totaling ~1.8 GB CSV file with 15,289,353 rows of stock price data.
It takes an average of 42 seconds and ~3.2 GB of RAM to process the average_open_close report. This code is MVP
stage, so for now this is adequate performance. Pandas and numpy are optimized using python c-extensions, so while
its pretty faster out of the box i'm sure my pandas code can be improved. That being said this code is optimized more 
for readability and long term maintainability rather then keeping cpu cycles to the lowest possible level.

Datasets in the 10,000 rows range or less should process less than a second.

###Links & Docs

https://www.quandl.com/tools/python

https://github.com/quandl/quandl-python

https://www.quandl.com/databases/WIKIP

https://www.quandl.com/databases/WIKIP/documentation/about

https://docs.quandl.com/docs/python-installation

https://docs.quandl.com/docs/python-tables

https://docs.quandl.com/docs/python-time-series

https://docs.quandl.com/docs#section-authentication

https://docs.quandl.com/docs/data-organization

https://docs.quandl.com/docs/parameters-1

https://blog.quandl.com/getting-started-with-the-quandl-api

https://pypi.python.org/pypi/Quandl

https://pypi.python.org/pypi/pandas/0.22.0
 
