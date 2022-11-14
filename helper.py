import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import advertools as adv

stop_words = open('stop_hinglish.txt', 'r')
stop_words = stop_words.read()


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # 1. fetch number of messages
    num_messages = df.shape[0]
    # 2. fetch number of words
    words = []
    for message in df["message"]:
        words.extend(message.split())

    # 3. media omitted
    df_media = df[df['message'] == '<Media omitted>\n']

    # 4. number of links
    extractor = URLExtract()
    urls = []
    for message in df["message"]:
        urls.extend(extractor.find_urls(message))
    return len(words), num_messages, len(df_media), len(urls)


def fetch_mostBusyUsers(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df


def create_wordcloud(selected_user, df):
    df_new = df[df["message"] != "<Media omitted>\n"]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)

    if selected_user != "Overall":
        df_new = df_new[df_new['user'] == selected_user]
    df_new = df_new[df_new["message"] != "This message was deleted\n"]
    df_new = df_new[df_new["message"] != df_new["message"].str.find("group's icon\n")]
    df_new["message"] = df_new["message"].apply(remove_stop_words)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df_new['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    df_new = df[df["message"] != "<Media omitted>\n"]
    df_new = df_new[df_new["message"] != "This message was deleted\n"]
    df_new = df_new[df_new["message"] != df_new["message"].str.find("group's icon\n")]
    # df_new = df_new[df_new["message"] != df_new["message"].str.find("changed the subject")]
    if selected_user != "Overall":
        df_new = df_new[df_new['user'] == selected_user]

    words = []
    for mes in df_new["message"]:
        for m in mes.lower().split(" "):
            if m not in stop_words:
                words.append(m)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def most_common_emojis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    emoji_summary = adv.extract_emoji(df["message"].to_list())
    for i in emoji_summary['emoji']:
        for j in i:
            emojis.extend(j)
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    print(timeline)
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_time = df.groupby('only_time').count()['message'].reset_index()
    return daily_time


def weekly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()


def month_activity(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def daily_heat(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    activity=df.pivot_table(index='day_name',columns='period',values="message",aggfunc="count").fillna(0)
    return activity
