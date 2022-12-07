import datetime
from typing import List, Optional

import altair as alt
from fastapi import FastAPI, Query, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from strompris import (
    ACTIVITIES,
    LOCATION_CODES,
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

from fastapi.responses import HTMLResponse


app = FastAPI()
templates = Jinja2Templates(directory="templates")



# `GET /` should render the `strompris.html` template
# with inputs:
# - request
# - location_codes: location code dict
# - today: current date

@app.get("/")
def render_html(request: Request):
    """Render html
    arguments:
        request (Request)

    return:
        template of request, location_codes and datetime today
    """
    return templates.TemplateResponse("strompris.html", {
        "request": request,
        "location_codes": LOCATION_CODES.keys(),
        "today": str(datetime.date.today())
    })

# GET /plot_prices.json should take inputs:
# - locations (list from Query)
# - end (date)
# - days (int, default=7)
# all inputs should be optional
# return should be a vega-lite JSON chart (alt.Chart.to_dict())
# produced by `plot_prices`
# (task 5.6: return chart stacked with plot_daily_prices)

@app.get("/plot_prices.json")
def render_json(
    locations: Optional[List[str]] = Query(default=list(LOCATION_CODES.keys())),
    end: Optional[datetime.date] = None,
    days: Optional[int] = 7
    ):
    """Render json
    arguments:
        locations (List) : optional list of locations
        end (datetime.date) : optional date object
        days (int) : optional Integer to choose timespan

    return:
        dictionary of chart from plot_prices()
    """
    df = fetch_prices(end_date=end, days=days, locations=locations)
    chart = plot_prices(df)
    return chart.to_dict()

# Task 5.6:
# `GET /activity` should render the `activity.html` template
# activity.html template must be adapted from `strompris.html`
# with inputs:
# - request
# - location_codes: location code dict
# - activities: activity energy dict
# - today: current date

...

# Task 5.6:
# `GET /plot_activity.json` should return vega-lite chart JSON (alt.Chart.to_dict())
# from `plot_activity_prices`
# with inputs:
# - location (single, default=NO1)
# - activity (str, default=shower)
# - minutes (int, default=10)

...


# mount your docs directory as static files at `/help`

...

if __name__ == "__main__":
    # use uvicorn to launch your application on port 5000
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)
