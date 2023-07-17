from urlextract import URLExtract
import pandas as pd
import numpy as np
from collections import Counter
from wordcloud import WordCloud
import emoji

extract = URLExtract()


def monthactivitymap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    return df['Month'].value_counts()


def weekactivitymap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Day_name'].value_counts()


def monthtimeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df.groupby(['Year', 'Month_num', 'Month']).count()[
        'Message'
    ].reset_index()
    time = []
    for i in range(temp.shape[0]):
        time.append(temp['Month'][i]+'-'+str(temp['Year'][i]))
    temp['Time'] = np.array(time)
    return temp


def getemojistats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def fetchstats(selected_user, df):
    total_messages = df.shape[0]
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())

    mediaommitted = df[df['Message'] == '<Media omitted>']

    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), mediaommitted.shape[0], len(links), total_messages


def fetchbusyuser(df):
    count = df['User'].value_counts().head()
    newdf = pd.DataFrame(round((df['User'].value_counts()/df.shape[0])*100, 2))
    return count, newdf


def createwordclound(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10,background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))
    return df_wc


def getcommonwords(selecteduser, df):
    file = open('stop_hinglish.txt', 'r')
    stopwords = file.read()
    stopwords = stopwords.split('\n')

    if selecteduser != 'Overall':
        df = df[df['User'] == selecteduser]

    temp = df[df['User'] != '<Media omitted>']

    words = []
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    mostcommon = pd.DataFrame(Counter(words).most_common(20))
    return mostcommon


if __name__ == '__main__':
    # print(emoji.__version__)
    emojis = []
    message = 'hey how are you😃'
    emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    print(emojis)