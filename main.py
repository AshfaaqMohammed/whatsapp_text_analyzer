import streamlit as st
from streamlit_option_menu import option_menu
import time
import matplotlib.pyplot as plt
import numpy as np
import preprocess
import stats
import plotly.express as px
from query_defs import start_query, get_response, small_df
from ui import set_openai_api_key, reset_results, set_initial_state

# st.sidebar.title("Whatsapp Chat Analyzer")
st.sidebar.image("whatsapp image.png", caption='Analyzing Made Easy')

uploaded_file = st.sidebar.file_uploader("Choose a file")


if uploaded_file is not None:

    with st.sidebar:
        selected = option_menu(
            menu_title="Options",
            options=["Visualization", "Chatbot"],
            icons=["search", "robot"],
            menu_icon="cast",
            default_index=0
        )

    def getdf(uploaded_file):
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        dataframe = preprocess.preprocess(data)
        return dataframe

    df = getdf(uploaded_file)

    if selected == 'Visualization':
        user_list = df['User'].unique().tolist()

        # user_list.remove('Group notification')
        user_list.sort()

        user_list.insert(0, 'Overall')
        user_list = tuple(user_list)

        selected_user = st.sidebar.selectbox(
            "Show analysis with respect to", user_list)
        st.title("📈 chat analysis - " + selected_user)
        if st.sidebar.button("Show Analysis"):
            num_messages, num_words, media_omitted, links, total_messages = stats.fetchstats(
                selected_user, df
            )

            col1, col2, col3, col4 = st.columns(4, gap='large')

            with col1:
                st.info("Total Messages", icon='💭')
                st.metric(label=selected_user ,value=f'{num_messages}')
            # col1.metric("Total Messages", num_messages)
            with col2:
                st.info("Total Words", icon="🔤")
                st.metric(label=selected_user, value=f'{num_words}')
            with col3:
                st.info("Media Shared", icon="🖼")
                st.metric(label=selected_user, value=f'{media_omitted}')
            with col4:
                st.info("Links Shared", icon="🔗")
                st.metric(label=selected_user, value=f'{links}')

            if selected_user == 'Overall':

                st.title("Most Busy User")
                busycount, newdf = stats.fetchbusyuser(df)
                fig, ax = plt.subplots()
                col1, col2 = st.columns(2, gap='large')
                with col1:
                    ax.bar(busycount.index, busycount.values, color='blue')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                    st.info(f"{busycount.index[0]}" + " is busiest user", icon="🥇")

                with col2:
                    st.dataframe(newdf)

            if selected_user != 'Overall':
                st.markdown(
                    """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",
                    unsafe_allow_html=True, )
                target = total_messages
                current = num_messages
                percent = round((current/target*100))
                mybar = st.progress(0)

                if percent>100:
                    st.subheader("Target done!")
                else:
                    st.write(f"{selected_user} have ", percent, "% ", "of ", (format(target, 'd')))
                    for percent_complete in range(percent):
                        time.sleep(0.1)
                        mybar.progress(percent_complete+1, text=" Target Percentage")

            st.title('Word Cloud')
            df_img = stats.createwordclound(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_img)
            st.pyplot(fig)

            most_common_df = stats.getcommonwords(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            st.title("Most common words")
            st.pyplot(fig)
            try:
                emoji_df = stats.getemojistats(selected_user, df)
                emoji_df.columns = ['Emoji', 'Count']
                st.title("Emoji Analysis")

                col1, col2 = st.columns(2, gap='large')

                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    emojicount = list(emoji_df['Count'])
                    perlist = [(i / sum(emojicount)) * 100 for i in emojicount]
                    emoji_df['Percentage Use'] = np.array(perlist)
                    # st.dataframe(emoji_df)
                    fig = px.pie(labels=emoji_df['Emoji'],
                                 values=emoji_df['Percentage Use'])
                                 # hover_data=[emoji_df['Percentage Use']]
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
            except ValueError:
                st.title("No Emojis Used")

            st.title("Monthly Timeline")
            time = stats.monthtimeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(time['Time'], time['Message'], color='green')
            plt.xticks(rotation='vertical')
            plt.tight_layout()
            st.pyplot(fig)

            st.title("Activity Maps")
            col1, col2 = st.columns(2, gap='large')

            with col1:
                st.header('Most Busy Day')
                busy_day = stats.weekactivitymap(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='purple')
                plt.xticks(rotation='vertical')
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)

            with col2:
                st.header("Most Busy Month")
                busy_month = stats.monthactivitymap(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='yellow')
                plt.xticks(rotation='vertical')
                plt.tight_layout()
                st.pyplot(fig, use_container_width=True)

    if selected == 'Chatbot':
        set_initial_state()
        st.title("🤖 Welcome to ChatBot Section")


        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below\n"
            "2. Enter your question\n"
            "3. Enjoy 🤗\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)

        if st.session_state.get("OPENAI_API_KEY"):
            small_df(df)
            start_query()
            st.session_state['api_key_configured'] = True
            prompt, button = st.columns(2)
            with prompt:
                question = st.text_input("Ask Question", on_change=reset_results)

            with button:
                st.write('')
                st.write('')
                run_pressed = st.button("Submit")
        else:
            st.write("Please provide your OpenAI key to start using chatbot")

        if st.session_state.get('api_key_configured'):
            # run_pressed = (
            #     run_pressed or question != st.session_state.question
            # )
            if run_pressed and question:
                reset_results()
                st.session_state.question = question
                with st.spinner('🔍'):
                    # try:
                    st.session_state.result = get_response(question)
                    # except

        if st.session_state.result:
            ans = st.session_state.result
            st.info(ans.response)