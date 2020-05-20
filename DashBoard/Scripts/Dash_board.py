import dash
import os
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.offline as pyo
import plotly.graph_objs as go
from Scripts.Data_preperation import Global_data , State_data , Daily_data ,Age_Gender

#-----------------------------------------------------------------------------
# path = '/home/ryouk/Desktop/DashBoard/Data'
path = os.getcwd()+'/Data'
gd = Global_data(path+'/global_covid19.csv')
sd = State_data(path+'/state_wise.csv')
dd = Daily_data(path+'/daily_count.csv')
ag = Age_Gender(path)
#-----------------------------------------------------------------------------
#Global_data
def get_world():
    return gd.plot_data()
global_df = gd.add_text()
#-----------------------------------------------------------------------------
#State_data
state_options , state_code = sd.get_options()
status = sd.get_status()
state_df = sd.get_df()
#-----------------------------------------------------------------------------
#Daily_data
daily_df = dd.get_df()
daily_options  =dd.get_options()
#-----------------------------------------------------------------------------
#Age and Gender

def get_age():
    return ag.get_bar()

def get_gender():
    return ag.get_pie()
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
app = dash.Dash(__name__)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True
server = app.server

app.layout = html.Div([ dcc.Tabs( id = 'Tabs' , tabs = [{'label':'GLOBAL',"value":'tab1'},{'label':'INDIA-STATE',"value":'tab2'},
                                                        {'label':"TIMELINE",'value':'tab3'},{'label':'AGE & GENDER',"value":'tab4'}],
                                 value = 'tab1'),
                        html.Div(id = "Output")
                    ])

#-----------------------------------------------------------------------------
#callback for state

@app.callback(Output('State','figure'),[Input('select-state','value')])
def select_state(value):
    plots = []
    df = pd.DataFrame()

    for code in value:
        df =  df.append(state_df[state_df.State_code == code])

    for Status in status:
        plots.append(go.Bar(x = df.State , y = df[Status] , name = Status))

    layout = go.Layout(xaxis = dict(title = 'States') , yaxis = dict(title = 'Count') , paper_bgcolor = '#f5f5f5',
                       font = {'color': '#111111' , 'size' : 15} , height = 500 ,
                        margin = dict(l = 70 , r = 0 , t = 0 , b = 60 , pad = 2))

    return dict(data = plots , layout = layout)

#-----------------------------------------------------------------------------
#callback for daily

@app.callback(Output('Daily' , 'figure') , [Input('select-month','value')])
def select_month(value):
    plots = []
    df = daily_df

    if value == 0:
        for status in df.Status.unique():
            temp = df[df.Status == status]
            plots.append(go.Scatter(x = temp.Date , y = temp.TT , mode = 'marker+lines' , name = status))

    else:
        df = daily_df[daily_df.Month == value]

        for status in df.Status.unique():
            temp = df[df.Status == status]
            plots.append(go.Scatter(x = temp.Date , y = temp.TT , mode = 'marker+lines' , name = status))

    layout = go.Layout(xaxis = dict(title = 'Timeline') , yaxis = dict(title = 'Count') , paper_bgcolor = '#f5f5f5',
                        font = {'color':'#111111' , 'size' : 15} , height = 500 ,
                        margin = dict(l = 70 , r = 0 , t = 0 , b = 60 , pad = 2))

    return dict(data = plots , layout = layout)
#-----------------------------------------------------------------------------

#Tabs
@app.callback(Output('Output','children') , [Input('Tabs','value')])
def select_tab(value):
    if value == 'tab1':
        return html.Div([html.H2('GLOBAL COUNT' , style = {'textAlign':'center'}),
                        dcc.Graph(id = 'Global' , figure = get_world() , config = dict(scrollZoom = False , diaplaylogo = False)),
                        html.Br(),
                        html.Div(id = 'info' , children = ['*Hover over the countries to view count'])
                        ])
    if value == 'tab2':
        return html.Div([html.H2('STATE COUNT' , style = {'textAlign':'center'}),
                        dcc.Graph(id = 'State'),
                        html.Br(),
                        html.Div(id = 'prompt-state' , children = 'Select States' , style = {'fontSize': 20}),
                        html.Br(),
                        dcc.Dropdown(id = 'select-state' , options = state_options , value = state_code[:5] ,
                         clearable = False , multi = True )
                        ])
    if value == 'tab3':
        return html.Div([html.H2('DAILY COUNT' , style = {'textAlign':'center'}),
                        dcc.Graph(id = 'Daily'),
                        html.Br(),
                        html.Div(id = 'prompt-month' , children = 'Select Month' , style = {'fontSize': 20}),
                        html.Br(),
                        dcc.Dropdown(id = 'select-month' , options = daily_options , value = 0 , clearable = False)
                        ])
    if value == 'tab4':
        return html.Div([html.H2('AGE & GENDER COVID-19' , style = {'textAlign':'center'}),
                         html.Div(dcc.Graph(id = 'age' , figure = get_age())),
                         html.Div(dcc.Graph(id = 'gender' , figure = get_gender()))])
#-----------------------------------------------------------------------------
def start_server():
    if __name__ != '__main__':
        app.run_server(debug = True)
