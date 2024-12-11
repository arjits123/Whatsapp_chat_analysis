from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import pandas as pd
import string
import emoji
from collections import Counter

def fetch_user(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    
    # number of messages
    num_mesasges = df.shape[0]

    #number of words
    words = []
    for message in df['message']:
        words.extend(message.split(' '))

    # number of images
    media_messages = df[df['message'] == 'image omitted\r\n'].shape[0]

    #number of URLS
    links = []
    for message in df['message']:
        urls = extractor.find_urls(message)
        links.extend(urls)
    
    return num_mesasges, len(words), media_messages, len(links)

def fetch_most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df  = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index()
    new_df = new_df.rename(columns={'index': "name", 'user': 'Percentage'})
    return x, new_df

def create_word_cloud(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    
    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
    df_wc = wc.generate(df['message'].str.cat(sep = ' ')) # concatenate all the words in messages
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    
    temp_df  = df[df['user'] != 'Group notification']
    temp_df = temp_df[temp_df['message'] != 'image omitted\r\n']
    temp_df = temp_df[temp_df['message'] != 'sticker omitted\r\n']

    words = []
    punc = string.punctuation
    f = open('stop_hinglish.txt')
    stop_words  = f.read()
    for message in temp_df['message']:
        for word in message.lower().split():
            if word not in punc and word not in stop_words:
                words.append(word)
    counter = {}
    for w in words:
        if w in counter:
            counter[w] += 1
        else:
            counter[w] = 1

    final_list  = sorted(counter.items(), key=lambda x:x[1], reverse=True)
    top_10_words_df  = pd.DataFrame(final_list[:10])
    top_10_words_df = top_10_words_df.rename(columns={0:'Word',1:'Count'})
    return top_10_words_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    
    emojis = []
    for m in df['message']:
        emojis.extend([c for c in m if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df = emoji_df.rename(columns={0:'emoji', 1:'count'})
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    
    timeline_df = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline_df.shape[0]):
        time.append(timeline_df['month'][i]+ "-" +str(timeline_df['year'][i]))
    timeline_df['time'] = time

    return timeline_df

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    busy_day =  df['day_name'].value_counts()
    return busy_day

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]
    busy_month=  df['month'].value_counts()
    return busy_month