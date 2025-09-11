from dash import dcc, html




title_container= html.Div(
    id= "results-title-container",
    className= "title-container",
    children= [html.H1("Cycling DB Loader", className="h1-title")]
)
results_title_container= html.Div(
    id= "results-title",
    className= "results-title-container",
    children= [html.H1("Data Load Results", className="results-h1-title")]
)

results_header_container= html.Div(
    id= "results_header-container",
    className= "header-container",
    children= [
        title_container
    ]
)

logout_button= html.Button(
    "Log Out",
    id= "results-logout-button",
    className="logout-button",
    style= {"textDecoration":"none"}
)

return_button = html.A(
    "← Return",
    href="/dash/database-loader/",  # o la ruta que necesites
    id="results-return-button",
    className="return-button",
    style={"textDecoration": "none"}
)

results_chart_container= html.Div(
    id="results-chart-container",
    className="results-chart-container",
    children= [
        dcc.Graph(
            id="results-chart",
            className="results-chart",
            config={
                "modeBarButtonsToRemove": [
                    'pan2d',
                    'select2d',
                    'lasso2d',
                    
                    'zoomOut2d',
                    "autoscale",
                    'zoomIn2d',
                    'zoom2d'
                ],
                "displaylogo": False
            }
        )
    ]
)



main_container= html.Div(
    id="results-main-content-area",
    className= "results-main-container",
    children=[
        results_title_container,
        results_chart_container]
)

results_store= dcc.Store(id="results-store", storage_type="session", clear_data= False) 

results_layout= html.Div(
    id="results-main-container",
    className="dash-main-container",
    children=[
        return_button,
        logout_button,
        results_header_container,
        main_container,
        results_store
              ]
)
