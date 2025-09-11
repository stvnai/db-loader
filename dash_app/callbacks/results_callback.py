from dash import Input, Output, dcc, State, callback
import plotly.express as px
import plotly.graph_objects as go


def show_results(app):

    @app.callback(
        Output("results-chart", "figure"),
        State("results-store", "data"),
        Input("results-chart-container","id")
    )

    def generate_chart_results(results,_):

        data= {"batch_size":85, "success":50, "failures":35}

        if results:
            data= results

            
        labels= ["Processed", "Not Processed"]
        values=[data.get("success",0), data.get("failures",0)]


        fig= go.Figure()

        fig.add_trace(
            go.Pie(
                labels= labels,
                values= values,
                pull= [0.0,0.03],
                name="",
                marker_colors= ["#113C58", "#E35936"],
                hole= 0.7, 
                textinfo="value",
                hoverinfo="label+percent",
                textfont={'size': 30, 'color': "#A1A8B4"}
                

            )
        )

        fig.add_annotation(
            text="<b>Files in Batch:</b>",
            showarrow=False,
            font= dict(
                size=27,
                color="#1B5F8D"
            ),

            xref="paper",
            yref="paper",
            x=0.5,
            y=0.41
        )

        fig.add_annotation(
            text=f"{data["batch_size"]}",
            showarrow=False,
            font= dict(
                size=80,
                color="#A1A8B4"
            ),

            xref="paper",
            yref="paper",
            x=0.5,
            y=0.55

            
        )

        fig.update_layout(
            # title="<b>Data Load Results</b>",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        return fig