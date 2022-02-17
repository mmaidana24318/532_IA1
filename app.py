from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd

def plot_altair(nb):
    df = pd.read_csv(r'data/crimedata_2022.csv')
    nb_list= []
    nb_list.append(nb)
    chart = alt.Chart(df[df["NEIGHBOURHOOD"].isin(nb_list)],
                        title=alt.TitleParams(text='Types of Crimes in Vancouver by Neighbourhood - 2022',
                        subtitle=nb)
                ).mark_bar().encode(
                alt.X('count()', title="Number of Crimes"),
                alt.Y('TYPE', title="Type of Crime", sort='x')
                )
    return chart.to_html()

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
    dcc.Dropdown(
            id='nb', 
            value='West End',
            style={'width': '50%'},
            clearable = False, 
            options=[{'label': i, 'value': i} for i in ['West End', 'Central Business District', 'Mount Pleasant',
                                                        'Sunset', 'Strathcona', 'Fairview', 'Kensington-Cedar Cottage', 
                                                        'Grandview-Woodland', 'Hastings-Sunrise', 'Kitsilano',
                                                        'Kerrisdale', 'Arbutus Ridge', 'Renfrew-Collingwood',
                                                        'South Cambie', 'Killarney', 'Dunbar-Southlands',
                                                        'Riley Park', 'West Point Grey', 'Victoria-Fraserview',
                                                        'Oakridge', 'Marpole', 'Shaughnessy', 'Musqueam']
                    ]),
    html.Iframe(
        id='plot',
        srcDoc=plot_altair(nb="West End"),
        style={'border-width': '0', 'width': '100%', 'height': '400px'})
    ]) 

@app.callback(
    Output('plot', 'srcDoc'),
    Input('nb', 'value'))

def update_output(nb):
    return plot_altair(nb)


if __name__ == '__main__':
    app.run_server(debug=True)