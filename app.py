import streamlit as st
import pandas as pd
import numpy as np
import preprocessor, utils
import re
import matplotlib.pyplot as plt

st.sidebar.title('Whatsapp chat analyser')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.date_preprocessor(data)
    # st.dataframe(df)


    #Fetch unique users 
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'Overall')
    
    selected_user = st.sidebar.selectbox('Show analysis for:',user_list)

    # Analysis
    if st.sidebar.button('Show analysis'):
        
        # Key Performance indicators
        num_messages, words , media_messages, links = utils.fetch_user(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Texts')
            st.title(num_messages)
        
        with col2:
            st.header('Total words')
            st.title(words)

        with col3:
            st.header('Media shared')
            st.title(media_messages)
        
        with col4:
            st.header('Links shared')
            st.title(links)
        
        #yearly and month timeline
        st.title('Timeline')
        timeline_df = utils.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline_df['time'], timeline_df['message'], color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)


        #Activity map
        st.title('Activity map')
        col1, col2 = st.columns(2)

        # For Days
        with col1:
            st.header("Most busy day")
            busy_day = utils.week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'purple')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        #For Month
        with col2:
            st.header("Most busy Month")
            busy_month = utils.month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'orange')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)


        
        # Most activate users on Group basis
        if selected_user == 'Overall':
            st.title('Most active users')

            x, new_df = utils.fetch_most_busy_users(df)
            name = x.index
            count = x.values
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(name, count)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            
            with col2:
                st.dataframe(new_df)
        
        
        #most used words and emojis
        col1, col2 = st.columns(2)
        with col1:
            #Most used words
            st.title("Most used words")
            top_10_words_df = utils.most_common_words(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(top_10_words_df['Word'], top_10_words_df['Count'], color = 'brown')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            # Most used emojis
            st.title('Most used emoji')
            emoji_df = utils.emoji_helper(selected_user,df)
            st.dataframe(emoji_df.head(10))
        
        # Word cloud
        st.title('Word cloud')
        wc_image = utils.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc_image)
        st.pyplot(fig)




            
