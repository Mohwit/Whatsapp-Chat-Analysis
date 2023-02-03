import pandas as pd
import re

def preprocess(data):
    ## pattern to seperate data and time
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'Message':messages, 'Date':dates})

    ## convert messages_data type
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y, %H:%M - ')

    ## Separating user name and user message

    ## list for user
    users = []
    ## list for messages
    messages = []

    ## iterating in messages
    for message in df['Message']:
        ## splitting message with ':'
        entry = re.split('([\w\W]+?):\s', message)
        
        ## if it has value after ':'
        if entry[1:]: # user name
            ## appending users
            users.append(entry[1])
            ## appending message
            messages.append(entry[2][:-1])
        
        ## if it does not have a user name
        else:
            ## appending name as 'Notification'
            users.append('Notification')
            ## appending message
            messages.append(entry[0][:-1])
            
    ## dropping previous message column
    df.drop('Message', axis = 1, inplace=True)
    ## adding user column with user names
    df['User'] = users
    ## adding message column with just message
    df['Message'] = messages

    ## Separating Year, month, day, hour and minute from Date
    ## and creating specific column
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Month_Number'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    df['Only_Date'] = df['Date'].dt.date
    df['Day_Name'] = df['Date'].dt.day_name

    period = []
    for hour in df[['Day_Name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['Period'] = period

    return df