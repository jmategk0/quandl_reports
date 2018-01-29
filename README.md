Introduction

This is a toolkit for reporting on quandl stocks data using pandas. Data may be ingested via rest api calls or by
bulk operations on csv file exports. The core reporting is done by importing the raw data into dataframes and using
pandas query tools to produce reports in a json serializable format. These report results can be easily plugged into
another other desired system, such as a rest api or a data visualization tool.

Four reports are supported
1. average_open_close: average open and closing price for stocks
2. max_daily_profit: max daily profit base on daily high/low for stocks
3. busy_day: number of days where the stocks volume was 10% above average 
4. biggest_loser: number of days where a stocks close price was lower than its open price

Setup
1. create a new virtualenv
2. pip install requirements.txt
3. plug in your api key in config.py

NOTE: Only supported on python 3.6+ and Ubuntu 14.04+

Run Reports & Tests
1. demo cli: python36 demo_quandl_api_reporter.py average_open_close
2. Tests: python36 test_reports.py

NOTE: You can pass in any of the four report names into the cli tool. 

TODO and Future Work
1. Improve tests
2. resolve pandas warning
3. optimize pandas code (sorry this is my first pandas projects in a while)
4. Add rest api
5. Add data visualizations with pygal or D3
6. Add real UI with ReactJS
7. Cleanup file structure

Notes on Performance:

Reporting Code was tested on full quandl data export totally ~1.8 GB CSV file with 15,289,353 rows of stock price data.
It takes an average of 42 seconds and ~3.2 GB of RAM to process the average_open_close report. This is code is MVP
stage so this is adequate performance for now pandas and numpy are optimized using python and c-extensions.
This means the code is pretty fast out of the box but my uses of the pandas library can probably be improved.
(again this was my first pandas project in years) That being said this code is optimized more for readability and long
term maintainability rather then keeping cpu cycles to the lowest possible level.

Datasets in the 10,000 rows range or less should process less than a second.

Links & Docs

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
 
