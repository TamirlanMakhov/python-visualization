from dash import html, dcc
import dash_mantine_components as dmc
import dash_table
from .data import get_data_from_db

CARD_STYLE = dict(withBorder=True,
                  shadow="sm",
                  radius="md",
                  style={'height': '400px'})


def get_layout():
    df = get_data_from_db()

    return html.Div([
        dmc.Paper([
            dmc.Grid([
                dmc.Col([
                    dmc.Card([
                        dmc.Select(
                            label='Выберите клиента',
                            data=[{'label': client, 'value': client} for client in df['client_name'].unique()],
                            id='client_select'
                        ),
                        dmc.Select(
                            label='Выберите состояние',
                            data=[{'label': state, 'value': state} for state in df['state'].unique()],
                            id='state_select',
                            clearable=True,
                        ),
                        html.Div(id='client_info'),
                    ], **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        dcc.Graph(id='pie_chart')],
                        **CARD_STYLE)
                ], span=6),
                dmc.Col([
                    dmc.Card([
                        dcc.Graph(id='gantt_chart')],
                        **CARD_STYLE)
                ], span=12),
            ], gutter="xl", )
        ])
    ])
