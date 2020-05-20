import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Global_data:

    def __init__(self , path):
        self.__df = pd.read_csv(path)

    def add_text(self):
        #---------------------for apply()-----------------------
        def text(country_data):
            country = country_data[0]
            t1 = 'Cases : '+str(country_data[1])
            t2 = 'Recovered : '+str(country_data[3])
            t3 = 'Deaths : '+str(country_data[2])

            phrase = '<B>'+country+'</B>'+'<br><br>'+t1+'<br>'+t2+'<br>'+t3
            return phrase

        self.__df['Text'] = self.__df.apply(text , axis = 1)
        self.__df = self.__df.sort_values(by = ['Cases'] , ascending = False)

        return self.__df

    def plot_data(self):

        df = self.add_text()

        data = go.Choropleth(locations = df.Country , locationmode = 'country names',
                             colorscale = 'Greys' , reversescale = True , text = df.Text , z = df.Cases,
                             showscale = False , hoverinfo = 'text', colorbar = {'title':'COVID19 COUNT'})

        layout = dict(paper_bgcolor = '#f5f5f5' , height = 640 , margin = dict(l = 50 , r = 0 , t = 0 , b = 0 , pad = 2),
                        geo = dict(scope = 'world' , projection = {'type':'miller'}))

        return dict(data = [data] , layout = layout)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class State_data:

    def __init__(self,path):
        self.__df = pd.read_csv(path)
        self.__Status = ['Confirmed','Active', 'Recovered' , 'Deaths']

    def get_df(self):
        self.__df = self.__df.sort_values(by = ['Confirmed'] , ascending = False)
        return self.__df

    def get_status(self):
        return self.__Status

    def get_options(self):
        df = self.get_df()

        State_list = list(df.State)
        State_code = list(df.State_code)

        options = []

        for label , value in zip(State_list , State_code):
            options.append({'label' : label , 'value' : value})

        return options , State_code

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Daily_data:

    def __init__(self,path):
        self.__df = pd.read_csv(path)

    def get_df(self):

        self.__df.Date = pd.to_datetime(self.__df.Date)

        def month(date):
            date = date.strftime('%m')
            return date

        self.__df['Month'] = self.__df.Date.apply(month).astype(int)

        return self.__df

    def get_options(self):
        Month = ['UP-TO-DATE','JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
        Month_number = [0,1,2,3,4,5,6,7,8,9,10,11,12]

        options = []

        for mon , mon_nu in zip(Month , Month_number):
            options.append({'label' : mon , 'value' : mon_nu})

        return options

#------------------------------------------------------------------------------------------------------------------------------------------
class Age_Gender:

    def __init__(self,path):
        self.__df = pd.concat([pd.read_csv(path+'/raw_data1.csv') , pd.read_csv(path+'/raw_data2.csv')])

    def clean(self):
        self.__df['Gender'].replace('M' , 'Male' , inplace = True)
        self.__df['Gender'].replace('F' , 'Female' , inplace = True)

        self.__df = self.__df.sort_values(by = ['age_bucket'] , ascending=True)

        return self.__df

    def get_bar(self):
        df = self.clean()

        data = [go.Histogram(x = df.age_bucket , hoverinfo='y', marker = dict(color = '#1b1b2f'))]
        layout = go.Layout(paper_bgcolor = '#f5f5f5',
                        font = {'color':'#111111' , 'size' : 15} , height = 500 ,
                        margin = dict(l = 70 , r = 0 , t = 0 , b = 60 , pad = 2))

        return dict(data = data , layout = layout)

    def get_pie(self):
        df = self.clean()

        gender = df.Gender.value_counts()
        labels = list(gender.index)[:2]
        values = list(gender.values)[:2]

        data = [go.Pie(labels = labels , values = values , hole = 0.45 , hoverinfo = 'label+percent' ,
                         textinfo = 'none' , marker = dict(colors = ['#5c3c92','#F95700FF']))]
        layout = go.Layout(paper_bgcolor = '#f5f5f5',
                            font = {'color':'#111111' , 'size' : 15} , height = 500 ,
                            margin = dict(l = 70 , r = 0 , t = 0 , b = 60 , pad = 2))

        return dict(data = data , layout = layout)
