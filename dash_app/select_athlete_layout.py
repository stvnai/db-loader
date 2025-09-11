from dash import dcc, html

title_container= html.Div(
    id= "title-container",
    className= "title-container",
    children= [html.H1("Cycling DB Loader", className="h1-title")]
)
select_title_container= html.Div(
    id= "select-title-container",
    className= "title-container",
    children= [html.H2("Select athlete to start uploading", className="h2-title")]
)

header_container= html.Div(
    id= "header-container",
    className= "header-container",
    children= [
        title_container
    ]
)

athlete_list= dcc.Dropdown(
    id= "athlete-list",
    placeholder= "Select athlete",
    className="dropdown-list", 
    multi=False
)

athlete_list_container= html.Div(
    id= "athlete-list-container",
    className= "athlete-list-container",
    children= [athlete_list]

)

confirm_load_data_container= html.Div(
    id="confirm-load-data-container",
    className="confirm-load-data-container",
    children=[
        dcc.ConfirmDialogProvider(
            id="confirm-load-data-dialog",
            children= [
                html.Button(
                    "Load Data",
                    id= "load-button",
                    className= "load-button",
                    disabled=True
                )

            ]
        )
    ]
)


uploader_component= dcc.Upload(
    id= "file-uploader",
    className= "dash-uploader-area",
    multiple= True,
    accept= ".FIT, .fit",
    children= [
        html.Img(
            src="assets/db-icon-01.png",
            alt="db-icon",
            height=60,
            width=60,
            style={"opacity":"0.2", "marginBottom":"2rem"}),
        html.P("Drag and drop or"),
        html.A("click to select .fit files to upload", style= {"font-weight":"bold"}),
    ],

    style_reject= {
        "borderStyle":"dashed",
        "borderColor":'#1b5f8d',
        'backgroundColor': 'rgba(27, 95, 141, 0.05)',
        'color': '#a4a8bb',
        'opacity': '0.8'

    },
    disabled= True
)

uploader_container= html.Div(
    id= "uploader-container",
    className= "uploader-container",
    children= [uploader_component]
)


loading_data_container= html.Div(
    className= "loading-container",
    children= dcc.Loading(
        id= "loading-data",
        className="loading-data",
        type= "default",
        overlay_style= {"visibility":"visible", "filter": "blur(5px)"},
        children= [
            html.Div(
                id= "loading-container",
                style= {"display":"flex"}
            )
        ]
    )
)



logout_button= html.Button(
    "Log Out",
    id= "logout-button",
    className="logout-button",
    style= {"textDecoration":"none"}
)

register_link_container= html.Div(
    id= "register-link-container",
    className= "link-container",
    children= [
        html.P(
            "Athlete not in list?",
            className= "p-register-athlete"
            ),
        html.A(
            "Register a New Athlete",
            id="register-link",
            className="link-register-athlete",
            style={"font-weight":"bold"},
            href="/dash/register-athlete")
    ]

)

select_athlete_loader_container= html.Div(
    id= "select-athlete-loader-container",
    className= "select-athlete-loader-container",
    children= [
        
        athlete_list_container,
        uploader_container
        
    ]
)
data_loader_container= html.Div(
    id= "data-loader-container",
    className= "data-loader-container",
    children= [
        select_title_container,
        select_athlete_loader_container,
        loading_data_container

    ]
)

main_area_container= html.Div(
    id= "main-content-area",
    className= "main-content-area",
    children=[data_loader_container]
)

raw_data_store= dcc.Store(id="athlete-raw-data") 
selected_athlete_store= dcc.Store(id="selected-athlete-data")
results_store= dcc.Store(id="results-store", storage_type="session", clear_data= False) 

# location= html.Div(dcc.Location(id='url', refresh=False))

db_loader_layout= html.Div(
    id= "dash-main-container",
    className= "dash-main-container",
    children= [
        logout_button,
        header_container,
        main_area_container,
        confirm_load_data_container,
        register_link_container,
        raw_data_store,
        selected_athlete_store,
        results_store
    ]
)



