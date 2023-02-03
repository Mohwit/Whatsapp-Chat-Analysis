from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd 
from collections import Counter 
import emoji

extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    
    # 1. number of messages
    num_messages = df.shape[0]

    # 2. number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())
    

    # 3. 
    num_media_msg = df[df['Message'] == '<Media omitted>'].shape[0]

    links = []

    for messages in df['Message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_msg, len(links)


def most_busy_user(df):
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts()/df.shape[0]) * 100, 2).reset_index().rename(columns={'index':'Name', 'User':'Percent'})

    return x, df

def create_wordcloud(selected_user, df):
    file = open('stop_word.txt', 'r')
    stop_words = file.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    
    temp = df[df['User'] != 'Notification']
    temp = temp[temp['Message'] != '<Media omitted>']

    def remove_stop_words(message):
        y = []

        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        
        return " ".join(y)


    wc = WordCloud(width=500, height=500, background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
    return df_wc


def most_common_word(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    
    temp = df[df['User'] != 'Notification']
    temp = temp[temp['Message'] != '<Media omitted>']

    words = []

    file = open('stop_word.txt', 'r')
    stop_words = file.read()

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []

    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojis_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month_Number', 'Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['Time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('Only_Date').count()['Message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Day'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_Name', columns='Period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap
