import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    # stream of data
    bytes_data = uploaded_file.getvalue()
    # string of data
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):

        # stats Area
        st.title("Top Stats")
        num_words, num_messages, num_media, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Total Media Shared")
            st.title(num_media)

        with col4:
            st.header("Total Links Shared")
            st.title(num_links)

        # month timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline

        st.title("Daily Timeline")
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['only_time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map

        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy Day")
            timeline = helper.weekly_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(timeline.index, timeline.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            timeline = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(timeline.index, timeline.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Hourly Activity

        st.title("Hourly Activity")
        heat_map=helper.daily_heat(selected_user,df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(heat_map)
        st.pyplot(fig)



        # finding the busiest users in group
        if selected_user == "Overall":
            st.title("Most Active Users")
            x, new_df = helper.fetch_mostBusyUsers(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color="#FF4B4B")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Word Cloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # most common emojis
        st.title("Most Common Emojis")

        most_common_emoji = helper.most_common_emojis(selected_user, df)
        st.dataframe(most_common_emoji)
