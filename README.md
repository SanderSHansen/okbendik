# Assignment 5

## Dependencies
- altair
- altair-viewer
- beautifulsoup4
- fastapi[all]
- pandas
- pytest
- requests
- requests-cache
- uvicorn

## How to install
The requirements can be installed by running:
```
pip install -r requirements.txt
```

## How to run
The app can be run by running this command and typing "http://localhost:5000/" in your browser.
```
python3 app.py
```
The tests can be run by running these commands:
```
pytest -v tests/test_strompris.py
pytest -v tests/test_app.py
```


## Tasks done
- 5.1
- 5.2
- 5.3



## Files

### Task 5.1: strompris.py
- fetch_day_prices(): Fetch one day of data and return a DataFrame.
- fetch_prices(): Fetch prices for multiple days and locations and return a DataFrame.

- plot_prices(): Plots prices from a given DataFrame.

### Task 5.2 & 5.3: app.py
- render_html(): Renders the "strompris.html" with given inputs.
- render_json(): Takes given inputs and returns it as chart to dictionary.

The code was implemented and run on macOS Ventura 13.0