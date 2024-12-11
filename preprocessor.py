import pandas as pd
import numpy as np
import re
from datetime import datetime

def date_preprocessor(data):
    pattern = '\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}\s[ap]\.m\.\]\s'

    #messages
    messages = re.split(pattern,data)[1:]

    #dates
    dates = re.findall(pattern, data)
    new_dates  = []
    for date in dates:
        new_date = date.replace('\u202f', ' ').strip('[] ')
        new_dates.append(new_date)
    
    #Creating the dataframe
    df = pd.DataFrame({'user_message': messages, 'message_date': new_dates})
    
    #formating dates column
    df['message_date'] = df['message_date'].str.replace('a.m.', 'AM', case=False)
    df['message_date'] = df['message_date'].str.replace('p.m.', 'PM', case=False)
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %I:%M:%S %p')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    #Formatting message column
    users = []
    message = []
    for messages in df['user_message']:
        pattern = '([\w\W]+?):\s'
        entry = re.split(pattern, messages)
        users.append(entry[1])
        message.append(entry[2])
            

    df['user'] = users
    df['message'] = message
    new_message = []
    for m in df['message']:
        new_message.append(m.replace('\u200E', ''))
    df['message'] = new_message
    df['user'] = df['user'].replace({'The Boys':'Group notification'})
    df.drop(columns=['user_message'], inplace=True)

    #Splitting the date column in day, month, year and time
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()

    return df

