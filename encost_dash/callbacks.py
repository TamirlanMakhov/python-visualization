from dash import html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from .data import get_data_from_db

import dash_table
import plotly.express as px


def create_pie_chart(df):
    return px.pie(df, names='reason', title='Причины состояний')


def create_gantt_chart(df):
    df['duration_min'] = df['duration_min'].round()
    df = df.drop(columns=['duration_hour'])
    return px.timeline(df, x_start='state_begin', x_end='state_end', y='endpoint_name', color='state',
                       hover_data={
                                   'Duration (min)': df['duration_min'],
                                   'Shift Day': df['shift_day'],
                                   'Shift Name': df['shift_name'],
                                   'Operator': df['operator']
                                },
                       hover_name='state')

def register_callbacks(app):
    @app.callback(
        Output('client_info', 'children'),
        Output('pie_chart', 'figure'),
        Output('gantt_chart', 'figure'),
        Input('client_select', 'value'),
        Input('state_select', 'value'),
        prevent_initial_call=True,
    )
    def update_client_info(selected_client, selected_state):
        if selected_client is None:
            raise PreventUpdate

        df = get_data_from_db()
        client_data = df[df['client_name'] == selected_client]

        if selected_state is not None:
            client_data = client_data[client_data['state'] == selected_state]

        pie_chart = create_pie_chart(client_data)
        gantt_chart = create_gantt_chart(client_data)

        return (
            html.Div([
                html.H3(selected_client),
                dash_table.DataTable(
                    id='client_info_table',
                    columns=[
                        {"name": "Shift Day", "id": "shift_day"},
                        {"name": "Endpoint Name", "id": "endpoint_name"},
                        {"name": "State Begin", "id": "state_begin"},
                        {"name": "State End", "id": "state_end"},
                    ],
                    data=client_data.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    style_as_list_view=True,
                )
            ]),
            pie_chart,
            gantt_chart
        )
