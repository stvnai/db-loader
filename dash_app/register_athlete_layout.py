from dash import dcc, html
from datetime import date



title_container= html.Div(
    id= "register-title-container",
    className= "title-container",
    children= [html.H1("Cycling DB Loader", className="h1-title")]
)
register_title_container= html.Div(
    id= "register-title",
    className= "title-container",
    children= [html.H2("Register New Athlete", className="h2-title")]
)
date_of_birth_container= html.Div(
    id= "date_of_birth",
    className= "title-container",
    children= [html.H3("Date of birth", className="h3-title")]
)

header_container= html.Div(
    id= "header-container",
    className= "header-container",
    children= [
        title_container
    ]
)

logout_button= html.Button(
    "Log Out",
    id= "register-logout-button",
    className="logout-button",
    style= {"textDecoration":"none"}
)

select_link_container= html.Div(
    id= "select-link-container",
    className= "link-container",
    children= [
        html.P(
            "Athlete already registered?",
            className= "p-register-athlete"
            ),
        html.A(
            "Select Athlete and Upload",
            id="register-link",
            className="link-register-athlete",
            style={"font-weight":"bold"},
            href="/dash/database-loader/")
    ]

)

name_input= html.Div(
    id="name-input-container",
    className="input-container",
    children= [
        dcc.Input(
            id="name-input",
            className="text-input",
            type="text",
            placeholder="Name",
            multiple= False,
            maxLength=75,
            minLength=3,
            pattern="[A-Za-z]{3,}"
        )
    ]
)

lastname_input= html.Div(
    id="lastname-input-container",
    className="input-container",
    children= [
        dcc.Input(
            id="lastname-input",
            className="text-input",
            type="text",
            placeholder="Last Name",
            multiple= False,
            maxLength=75,
            minLength=3,
            pattern="[A-Za-z]{3,}"
        )
    ]
)

gender_input= html.Div(
    id="gender-input-container",
    className="input-container",
    children= [
        dcc.Input(
            id="gender-input",
            className="text-input",
            type="text",
            placeholder="Gender",
            multiple= False,
            maxLength=20,
            minLength=3,
            pattern="[A-Za-z]{3,}"
        )
    ]
)

today= date.today()
max_year= today.year - 12
min_year= today.year - 80
month= today.month
day= today.day


months= [
    {"label": "JAN", "value": 1},
    {"label": "FEB", "value": 2},
    {"label": "MAR", "value": 3},
    {"label": "APR", "value": 4},
    {"label": "MAY", "value": 5},
    {"label": "JUN", "value": 6},
    {"label": "JUL", "value": 7},
    {"label": "AUG", "value": 8},
    {"label": "SEP", "value": 9},
    {"label": "OCT", "value": 10},
    {"label": "NOV", "value": 11},
    {"label": "DEC", "value": 12}
]

year_range= [i for i in range(min_year, (max_year + 1))]


year_input= html.Div(
    id="year-input-container",
    className="date-input-container",
    children= [
        dcc.Dropdown(
            id="year-input",
            className="date-input",
            placeholder="YYYY",
            multi= False,
            options= [{"label": str(year_value), "value":year_value} for year_value in year_range]   
        )
    ]
)

month_input= html.Div(
    id="month-input-container",
    className="date-input-container",
    children= [
        dcc.Dropdown(
            id="month-input",
            className="date-input",
            placeholder="MM",
            multi=False,
            options= months   
        )
    ]
)
day_input= html.Div(
    id="day-input-container",
    className="date-input-container",
    children= [
        dcc.Dropdown(
            id="day-input",
            className="date-input",
            placeholder="DD",
            multi= False,
        )
    ]
)

date_input= html.Div(
    id= "date-input-container",
    className= "dates-input-container",
    children= [
        year_input,
        month_input,
        day_input
    ]
)

input_fields_container= html.Div(
    id= "all-inputs-container",
    className= "register-all-inputs-container",
    children= [
        name_input,
        lastname_input,
        gender_input,
        date_of_birth_container,
        date_input
    ]
)

register_button_container= html.Div(
    id= "register-button-container",
    className= "load-button-container",
    children= [
        html.Button(
            "Register Athlete",
            id= "register-button",
            className= "load-button",
            disabled= True,

        )
    ]
)

register_data_container= html.Div(
    id= "register-data-container",
    className= "register-data-container",
    children= [
        register_title_container,
        input_fields_container,
        register_button_container
    ]
)

confirm_registry_container= html.Div(
    id="confirm-registry-container",
    className="confirm-registry-container",
    children= [
        dcc.ConfirmDialog(
            id="check-athlete-exist"
        )
    ]

)

check_athlete_store= dcc.Store(id="athlete-exist-store")

register_athlete_layout= html.Div(
    id= "dash-register-main-container",
    className="dash-main-container",
    children=[
        logout_button,
        header_container,
        register_data_container,
        select_link_container,
        confirm_registry_container
        ]
)