import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Dados
semanas = ['05/04/2025', '12/04/2025', '19/04/2025', '26/04/2025']

peregrinos = {
    'Aldecir': [0, 4.08, 7.23, 0],
    'Almir': [0, 3, 0, 0],
    'André Simas': [0, 23.23, 0, 21.10],
    'Diego': [19, 10.4, 15.07, 0],
    'Edson': [0, 16.1, 7, 0],
    'Eduardo Silveira': [0, 57.84, 58.55, 6.42],
    'Emanuel Felipe': [5.02, 13.19, 0, 10.18],
    'Jhalyson': [6, 13.51, 12.93, 5.32],
    'Juarez': [15.25, 7.01, 10, 40.10],
    'Luiza Helena': [0, 27.33, 31.36, 30.46],
    'Luyper': [4.6, 4.6, 10.5, 0],
    'Maurício': [0, 11, 17.94, 8.41],
    'Ricardo': [53, 75, 75, 60]
}

# DataFrame
df = pd.DataFrame(peregrinos).T
df.columns = semanas
df['Total'] = df.sum(axis=1)

# Soma total por semana
soma_por_semana = df[semanas].sum(axis=0).tolist()

# Ranking Geral
df_geral = df[['Total']].sort_values(by='Total', ascending=False).reset_index()
df_geral.rename(columns={'index': 'Participante', 'Total': 'Quilometragem Total (km)'}, inplace=True)

# Ranking Semanal
rankings_semanais = {}
for semana in semanas:
    ranking = df[[semana]].sort_values(by=semana, ascending=False).reset_index()
    ranking.rename(columns={'index': 'Participante', semana: 'Quilometragem (km)'}, inplace=True)
    rankings_semanais[semana] = ranking

# App
app = dash.Dash(__name__)
app.title = "Dashboard de Corrida"

# Layout
app.layout = html.Div([
    html.H1('🏃‍♂️ Dashboard de Quilometragem 🏃‍♀️', style={'textAlign': 'center', 'color': '#003366'}),
    html.Br(),

    # Dropdown de Semana (com valor padrão para a mais atual)
    html.Div([
        dcc.Dropdown(
            id='dropdown-semana',
            options=[{'label': semana, 'value': semana} for semana in semanas],
            value=semanas[-1],  # Define a última semana como padrão
            style={'width': '50%', 'margin': '0 auto'}
        )
    ], style={'padding': '10px'}),

    # Gráfico Total do Grupo
    html.Div([
        dcc.Graph(
            id='grafico-total-grupo',
            figure={
                'data': [
                    go.Scatter(
                        x=semanas,
                        y=soma_por_semana,
                        mode='lines+markers',
                        name='Total do Grupo',
                        line=dict(color='blue', width=3),
                        marker=dict(size=10, color=['green' if v >= 300 else 'blue' for v in soma_por_semana])
                    ),
                    go.Scatter(
                        x=semanas,
                        y=[300]*len(semanas),
                        mode='lines',
                        name='Meta 300 km',
                        line=dict(dash='dash', color='red', width=2)
                    )
                ],
                'layout': go.Layout(
                    title='Total do Grupo por Semana vs Meta',
                    xaxis={'title': 'Semana'},
                    yaxis={'title': 'Quilometragem (km)'},
                    template='plotly_white',
                    legend=dict(orientation='h', y=-0.2)
                )
            }
        )
    ], style={'padding': '10px'}),

    # Gráfico Individual Dinâmico
    html.Div([
        dcc.Graph(id='grafico-individual')
    ], style={'padding': '10px'}),

    # Gráfico Pódio Top 6
    html.Div([
        dcc.Graph(
            id='grafico-top6',
            figure={
                'data': [
                    go.Bar(
                        x=list(df_geral['Participante'].head(6)),
                        y=list(df_geral['Quilometragem Total (km)'].head(6)),
                        marker_color=['gold', 'silver', '#cd7f32', '#1f77b4', '#2ca02c', '#ff7f0e']
                    )
                ],
                'layout': go.Layout(
                    title='🏆 Top 6 Participantes (Pódio)',
                    xaxis={'title': 'Participante'},
                    yaxis={'title': 'Quilometragem Total (km)'},
                    template='plotly_white'
                )
            }
        )
    ], style={'padding': '10px'}),

    html.Br(), html.Hr(),

    # Ranking Geral
    html.H2('📈 Ranking Geral', style={'textAlign': 'center'}),
    dash_table.DataTable(
        id='tabela-geral',
        columns=[{"name": col, "id": col} for col in df_geral.columns],
        data=df_geral.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_header={'backgroundColor': 'lightblue', 'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'row_index': 0}, 'backgroundColor': 'gold', 'color': 'black'},
            {'if': {'row_index': 1}, 'backgroundColor': 'silver', 'color': 'black'},
            {'if': {'row_index': 2}, 'backgroundColor': '#cd7f32', 'color': 'black'},
        ]
    ),

    html.Br(), html.Hr(),

    # Ranking Semanal (última semana)
    html.H2('📅 Ranking Semanal (Última Semana)', style={'textAlign': 'center'}),
    html.Div([
        html.H3(f"Semana de {semanas[-1]}", style={'textAlign': 'center'}),
        dash_table.DataTable(
            id=f'tabela-{semanas[-1]}',
            columns=[{"name": col, "id": col} for col in rankings_semanais[semanas[-1]].columns],
            data=rankings_semanais[semanas[-1]].to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'center'},
            style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
            style_data_conditional=[
                {'if': {'row_index': 0}, 'backgroundColor': 'gold', 'color': 'black'},
                {'if': {'row_index': 1}, 'backgroundColor': 'silver', 'color': 'black'},
                {'if': {'row_index': 2}, 'backgroundColor': '#cd7f32', 'color': 'black'},
            ]
        ),
    ])
], style={'maxWidth': '1200px', 'margin': '0 auto'})

# Callback para atualizar Tabela Semanal + Gráfico Individual
@app.callback(
    [Output('tabela-geral', 'data'),
     Output('grafico-individual', 'figure')],
    Input('dropdown-semana', 'value')
)
def atualizar_componentes(selecionada):
    # Atualiza a tabela de ranking geral
    df_geral = df[['Total']].sort_values(by='Total', ascending=False).reset_index()
    df_geral.rename(columns={'index': 'Participante', 'Total': 'Quilometragem Total (km)'}, inplace=True)

    # Atualiza o gráfico individual
    fig = {
        'data': [
            go.Bar(
                x=df_geral['Participante'],
                y=df_geral['Quilometragem Total (km)'],
                marker_color=['gold', 'silver', '#cd7f32'] + ['#1f77b4'] * (len(df_geral) - 3)
            )
        ],
        'layout': go.Layout(
            title=f'Quilometragem Total por Participante',
            xaxis={'title': 'Participante'},
            yaxis={'title': 'Quilometragem Total (km)'},
            template='plotly_white'
        )
    }

    return df_geral.to_dict('records'), fig

# Rodar o app
if __name__ == '__main__':
    app.run_server(debug=True)
