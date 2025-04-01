import numpy as np
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
dataDictionary = {
    'Year': [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],
    'Winner': ['Uruguay', 'Italy', 'Italy', 'Uruguay', 'Germany', 'Brazil', 'Brazil', 'England', 'Brazil', 'Germany', 'Argentina', 'Italy', 'Argentina', 'Germany', 'Brazil', 'France', 'Brazil', 'Italy', 'Spain', 'Germany', 'France', 'Argentina'],
    'RunnerUp': ['Argentina', 'Czechoslovakia', 'Hungary', 'Brazil', 'Hungary', 'Sweden', 'Czechoslovakia', 'Germany','Italy', 'Netherlands', 'Netherlands', 'Germany', 'Germany', 'Argentina', 'Italy', 'Brazil','Germany', 'France', 'Netherlands', 'Argentina', 'Croatia', 'France']
}
soccerData = pd.DataFrame(dataDictionary)
championCounts = soccerData['Winner'].value_counts().reset_index()
championCounts.columns = ['Country', 'Wins']
isoMap = {
    'Brazil': 'BRA',
    'Germany': 'GER',
    'Italy': 'ITA',
    'Argentina': 'ARG',
    'Uruguay': 'URY',
    'England': 'ENG',
    'France': 'FRA',
    'Spain': 'ESP'
}
championCounts['isoAlpha'] = championCounts['Country'].apply(lambda c: isoMap.get(c, None))
app = Dash(__name__)
server = server.app
app.layout = html.Div([
    html.H1("FIFA World Cup Finals", style={'textAlign': 'center'}),
    dcc.Tabs([
        dcc.Tab(label="All Winners", children=[
            html.Br(),
            html.H2("Countries That Have Won the World Cup"),
            dcc.Markdown(
                "*This tab displays all countries that have won the World Cup.*"
            ),
            html.Div(id="allWinnersDiv", style={'marginTop': '15px'})
        ]),
        dcc.Tab(label="Countrys Amount of Wins", children=[
            html.Br(),
            html.H2("Choose a Country to See Its World Cup Wins"),
            dcc.Dropdown(
                id="countryDropdown",
                options=[{'label': c, 'value': c} for c in championCounts['Country'].unique()],
                placeholder="Select a country..."
            ),
            html.Div(id="countryWinsOutput", style={'marginTop': '15px', 'fontWeight': 'bold'})
        ]),
        dcc.Tab(label="Final by Year", children=[
            html.Br(),
            html.H2("Select a World Cup Year for Winner & Runner-Up "),
            dcc.Dropdown(
                id="yearDropdown",
                options=[{'label': y, 'value': y} for y in soccerData['Year'].unique()],
                placeholder="Pick a year..."
            ),
            html.Div(id="yearWinnerRunnerupOutput", style={'marginTop': '15px', 'fontWeight': 'bold'})
        ]),
        dcc.Tab(label="Map of World Cup Winners", children=[
            html.Br(),
            html.H2("World Cup Wins by Country"),
            dcc.Graph(id="winsChoroplethFig")
        ])
    ])
])
@app.callback(
    Output("allWinnersDiv", "children"),
    Input("countryDropdown", "value")
)
def showAllWinners(_ignore):
    allWinnersList = championCounts['Country'].unique()
    return html.Ul([html.Li(country) for country in allWinnersList])
@app.callback(
    Output("countryWinsOutput", "children"),
    Input("countryDropdown", "value")
)
def showCountryWins(chosenCountry):
    row = championCounts[championCounts['Country'] == chosenCountry] if chosenCountry else pd.DataFrame()
    return "" if row.empty else f"{chosenCountry} has won the World Cup {row['Wins'].values[0]} time(s)."

@app.callback(
    Output("yearWinnerRunnerupOutput", "children"),
    Input("yearDropdown", "value")
)
def showYearlyWinnerRunnerup(chosenYear):
    row = soccerData[soccerData['Year'] == chosenYear] if chosenYear else pd.DataFrame()
    return "" if row.empty else f"In {chosenYear}, the winner was {row['Winner'].values[0]} and the runner-up was {row['RunnerUp'].values[0]}."
@app.callback(
    Output("winsChoroplethFig", "figure"),
    Input("countryDropdown", "value")
)
def updateMap(_ignoreCountry):
    fig = px.choropleth(
        championCounts,
        locations="isoAlpha",
        color="Wins",
        hover_name="Country",
        title="Total World Cup Wins by Country",
        color_continuous_scale=px.colors.sequential.Plasma,
        range_color=(0, championCounts['Wins'].max()),
        labels={'Wins': 'Number of Wins'}
    )
    fig.update_layout(margin={"r":0, "t":50, "l":0, "b":0})
    return fig
if __name__ == '__main__':
    app.run(debug=True)
