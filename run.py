from app import create_flask_app, create_dash_load_data, create_dash_register_athlete, create_dash_load_results
from app.set_logging import set_logging

set_logging()

app= create_flask_app()
load_data_app= create_dash_load_data(app)
dash_register_athlete= create_dash_register_athlete(app)
dash_results= create_dash_load_results(app)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug= True)
 