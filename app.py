import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from text_cleaner import clean_text, clean_text_spacy
from nlp_functions import show_wordcloud , plot_top_ngrams_bar_chart,detect_emotions,detect_overall_sentiment_avg,classify_custom,summarize_large_text

st.title('INTERACTIVE TEXT ANALYSIS PLATFORM')
st.divider()

a = st.sidebar.radio("SELECT ONE", ["Analyze Textual Data", "Analyze CSV File"])

if a == "Analyze Textual Data":
    st.header("Input Textual Data")
    text = st.text_area("Enter Textual Data", height=150)

    if st.button("Analyze"):
        if not text.strip():
            st.warning("Please enter Textual Data")
        else:
            #clean and process
            cleaned = clean_text(text)
            tokens = clean_text_spacy(cleaned)

            # WORD CLOUD
            if tokens:
                st.subheader("Word Cloud")
                wc_plot = show_wordcloud(tokens)
                st.pyplot(wc_plot)
            st.divider()

            # N-GRAM ANALYSIS.
            st.subheader("N-Gram Analysis")
            plot_top_ngrams_bar_chart(tokens, gram_n=3)
            st.divider()


            #Emotion Detection
            st.subheader("Emotion Detection")

            top_emotions_df = detect_emotions(text)
            max_index = top_emotions_df["Score"].idxmax()
            Emotion = top_emotions_df.loc[max_index, "Emotion"]
            Score = top_emotions_df.loc[max_index, "Score"]

            st.write(f"**Detected Primary Emotion:** {Emotion}  \n**Confidence Score:** {Score * 100:.2f}%")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Top 5 Detected Emotions")
                st.dataframe(top_emotions_df)

            with col2:
                st.markdown("### Emotion Distribution")
                fig = px.bar(
                    top_emotions_df,
                    x="Emotion",
                    y="Score",
                    color="Emotion"
                )
                fig.update_layout(
                    template='plotly_white',
                    height=290
                )
                st.plotly_chart(fig)
            st.divider()


            # SENTIMENTAL ANALYSIS
            st.subheader("Sentiment Analysis")
            result = detect_overall_sentiment_avg(text)
            if "error" in result:
                st.write("Error:", result["error"])
            else:
                st.write("Overall Sentiment:", result["overall_sentiment"])
                st.write("Average Scores:",
                    pd.DataFrame(list(result['average_scores'].items()), columns=['Emotion', 'Score']))
                st.divider()

            # TONE OF SPEECH DETECTION.
            st.subheader("Tone of Speech Classification")
            output = classify_custom(text)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"Predicted  : {output['predicted_category']}, score : {output['score']}")
                st.write("Other Top Predicted Categories")
                for label, score in output["all_categories"][1:6]:
                    st.write(f"Label :- {label}, Score:- {score}")

            with col2:
                labels = []
                scores = []
                for label, score in output["all_categories"][1:6]:
                    labels.append(label)
                    scores.append(score)

                fig = px.bar(x=labels, y=scores, color=labels, title="Other Top  5 Predicted Categories",
                                 height=400
                                 )
                st.plotly_chart(fig)
            st.divider()

            # SUMMARY GENERATION
            st.subheader("Text Summarization")
            output = summarize_large_text(text)
            st.write(output)

if a=="Analyze CSV File":
    st.header("Upload Your CSV File for Analysis")
    uploaded_file= st.file_uploader("Select a CSV file to begin analysis", type="csv")
    st.markdown("Make sure your file is in `.csv` format and contains headers.")

    if uploaded_file is not None:
            df= pd.read_csv(uploaded_file,  encoding="latin1")
            st.success("File uploaded successfully")
            st.divider()

            st.header("Filter and Analyze Your Data")

            # user selecting column to filter data
            column_name= st.selectbox("Select a column to filter the data:", df.columns)

            #selecting unique values
            unique_vals= df[column_name].dropna().unique()
            selected_value= st.multiselect(f"Choose value(s) from '{column_name}':", unique_vals)

            #select the column that is textual column
            text_processing_column= st.selectbox("Select a column for text analysis:", df.columns)

        # filtering
            if selected_value:
                filtered_df=  df[df[column_name].isin(selected_value)]
                filtered_df= filtered_df[text_processing_column]
                st.subheader("Filtered Data")
                st.dataframe(filtered_df)
                st.divider()
                text= " ".join(filtered_df.dropna().astype(str))

                # CLEANING OF TEXT
                cleaned = clean_text(text)
                tokens = clean_text_spacy(cleaned)
                # st.subheader("Cleaned and Lemmitized Text.")
                # st.write(" ".join(tokens) if tokens else "No meaning-full tokens Extracted")

                # WORD CLOUD
                if tokens:
                    st.subheader("Word Cloud")
                    wc_plot = show_wordcloud(tokens)
                    st.pyplot(wc_plot)
                st.divider()

                # N-GRAM ANALYSIS
                st.subheader("N-GRAM ANALYSIS")
                plot_top_ngrams_bar_chart(tokens, gram_n=3)
                st.divider()

               # EMOTION DETECTION
                st.subheader("Emotion Detection")

                top_emotions_df = detect_emotions(text)
                max_index = top_emotions_df["Score"].idxmax()
                Emotion = top_emotions_df.loc[max_index, "Emotion"]
                Score = top_emotions_df.loc[max_index, "Score"]

                st.write(f"**Detected Primary Emotion:** {Emotion}  \n**Confidence Score:** {Score * 100:.2f}%")

                col1, col2 = st.columns(2)

                with col1:
                   st.markdown("### Top 5 Detected Emotions")
                   st.dataframe(top_emotions_df)

                with col2:
                    st.markdown("### Emotion Distribution")
                    fig = px.bar(
                        top_emotions_df,
                        x="Emotion",
                        y="Score",
                        color="Emotion"
                    )
                    fig.update_layout(
                        template='plotly_white',
                        height=290
                    )
                    st.plotly_chart(fig)
                st.divider()

                # SENTIMENTAL ANALYSIS
                st.subheader("Sentiment Analysis")
                result = detect_overall_sentiment_avg(text)
                if "error" in result:
                    st.write("Error:", result["error"])
                else:
                    st.write("Overall Sentiment:", result["overall_sentiment"])
                    st.write("Average Scores:",
                             pd.DataFrame(list(result['average_scores'].items()), columns=['Emotion', 'Score']))
                st.divider()

                # TONE OF SPEECH DETECTION.
                st.subheader("Tone of Speech Classification")
                output = classify_custom(text)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"Predicted  : {output['predicted_category']}, score : {output['score']}")
                    st.write("Other Top Predicted Categories")
                    for label, score in output["all_categories"][1:6]:
                        st.write(f"Label :- {label}, Score:- {score}")

                with col2:
                    labels = []
                    scores = []
                    for label, score in output["all_categories"][1:6]:
                        labels.append(label)
                        scores.append(score)

                    fig = px.bar(x=labels, y=scores, color=labels, title="Other Top  5 Predicted Categories",
                                 height=400
                                 )
                    st.plotly_chart(fig)
                st.divider()
