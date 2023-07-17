import streamlit as st
import numpy as np
import seaborn as sn
import pandas as pd
import re
from datetime import datetime


def gettimeanddate(string):
    string = string.replace('[', '').replace(']', '')
    string = string.split(',')
    date, time = string[0], string[1]
    date = datetime.strptime(date, "%d/%m/%y").strftime("%m/%d/%y")
    time = time.strip()
    time = datetime.strptime(time, '%I:%M:%S %p')
    time = datetime.strftime(time, '%H:%M:%S')
    return date+' '+time


def getstring(text):
    return text.split('\n')[0]


def preprocess(data):
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}:\d{2} [AP]M\] '
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = df['message_date'].apply(lambda text: gettimeanddate(text))
    df.rename(columns={'message_date': 'date'}, inplace=True)

    user = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            user.append(entry[1])
            messages.append(entry[2])
        else:
            user.append('Group notification')
            messages.append(entry[0])

    df['User'] = user
    df['messages'] = messages

    df['messages'] = df['messages'].apply(lambda text:getstring(text))

    df = df.drop(['user_message'], axis=1)
    df = df[['messages', 'date', 'User']]

    df = df.rename(columns={'messages': 'Message',
                            'date': 'Date'})

    df['Only date'] = pd.to_datetime(df['Date']).dt.date
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    df['Month_num'] = pd.to_datetime(df['Date']).dt.month
    df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
    df['Day'] = pd.to_datetime(df['Date']).dt.day
    df['Day_name'] = pd.to_datetime(df['Date']).dt.day_name()
    df['Hour'] = pd.to_datetime(df['Date']).dt.hour
    df['Minute'] = pd.to_datetime(df['Date']).dt.minute

    return df

if __name__ == "__main__":
    print("hi")