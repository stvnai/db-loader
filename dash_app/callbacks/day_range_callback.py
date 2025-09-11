from dash import Input, Output, dcc, callback
import calendar

def day_range(app):
    @app.callback(
        Output("day-input", "options"),
        Input("year-input", "value"),
        Input("month-input", "value"),
    )

    def date_options(year, month):
        if year is not None and month is not None:

            month_days= calendar.monthrange(year,month)[1]

            options= [{"label": str(day), "value": day} for day in range(1,month_days+1)]
            return options
        else:
            options= [{"label": str(day), "value": day} for day in range(1,32)]
            return options
        




