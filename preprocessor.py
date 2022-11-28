import re

import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[AaPp][Mm]\s-\s'
    pattern_1 = '\d{1,2}/\d{1,2}/\d{2,4},\s'
    pattern_3 = '\d{1,2}:\d{1,2}\s[AaPp][Mm]'
    messages = re.split(pattern, data)[2:]
    time = re.findall(pattern_3, data)
    dates = re.findall(pattern_1, data)

    final_date = []
    for i in range(0, len(dates) - 1):
        if len(time[i]) == 7:
            time[i] = "0" + time[i]

        final_date.append(dates[i] + str(time[i]))
    df = pd.DataFrame({'user_message': messages, 'date': final_date})
    # convert message_date type
    df['date'] = pd.to_datetime(df['date'], format="%m/%d/%y, %I:%M %p")
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_time'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str(00))
        elif hour == 0:
            period.append(str(00) + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
