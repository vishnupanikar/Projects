import pandas as pd

#Gathering state_wise_daily data
State_wise_daily = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise_daily.csv')
State_wise_daily = State_wise_daily.iloc[:,:3]
State_wise_daily.to_csv('daily_count.csv' , index = False)

#Gathering state_wise data
State_wise = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
State_wise = State_wise.iloc[1:,:]
State_wise = State_wise[['State' , 'Confirmed' , 'Recovered' , 'Deaths' , 'Active' , 'State_code']]
State_wise.to_csv('state_wise.csv' , index = False)


#Gathering age and gender data
Age_and_Gender = pd.read_csv('https://api.covid19india.org/csv/latest/raw_data3.csv')
Age_and_Gender = Age_and_Gender[['Age Bracket' , 'Gender']]

def age_bucket(age):
    if age <= 10:
        return '0-10'
    elif 11 <= age <=20:
        return '11-20'
    elif 21 <= age <=30:
        return '21-30'
    elif 31 <= age <=40:
        return '31-40'
    elif 41 <= age <=50:
        return '41-50'
    elif 51 <= age <=60:
        return '51-60'
    elif 61 <= age <=70:
        return '61-70'
    elif 71 <= age <=80:
        return '71-80'
    elif 81 <= age <=90:
        return '81-90'
    elif 91 <= age <=100:
        return '91-100'

Age_and_Gender['age_bucket'] = Age_and_Gender['Age Bracket'].apply(age_bucket)
Age_and_Gender.to_csv('raw_data2.csv',index = False)
