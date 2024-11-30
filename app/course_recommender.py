# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from data_loader import loaded_df


# Load DataFrame and store in session state
# st.session_state.df = pd.read_csv("../assets/datasets/course_sentiments.csv")
st.session_state.df = loaded_df

def main():
    df = st.session_state.df
    
    # Create a search functionality
    def course_search(query):
        courses = pd.Series(df['course_name'].unique())
        vectorizer = TfidfVectorizer().fit(courses)
        query_vector = vectorizer.transform([query])
        course_vectors = vectorizer.fit_transform(courses)
        similarities = cosine_similarity(query_vector, course_vectors).flatten()
        top_10_indices = similarities.argsort()[-10:][::-1]
        top_10_courses = courses.loc[top_10_indices].tolist()
        results = df[df['course_name'].isin(top_10_courses)]
        return results

    # Create sentiment aggregation for recommendation
    def calculate_recommendation_score(df):
        recommendation_df = df.groupby('course_name').agg(
            course_source=('course_source', 'first'),
            positive_ratio=('sentiment', lambda x: x.value_counts().get('positive', 0) / len(x)),
            total_reviews=('sentiment', 'size')
        ).reset_index()
        return recommendation_df.sort_values(['total_reviews', 'positive_ratio'], ascending=False)

    # Integrate search and recommendation
    def recommend_courses(query):
        search_df = course_search(query)
        recommended_courses = calculate_recommendation_score(search_df)
        return recommended_courses
    
    st.title("Course Recommendation")

    search_query = st.text_input("Enter your course search query:")

    if search_query:
        with st.spinner("Searching for courses..."):
            recommendations = recommend_courses(search_query)

        st.dataframe(recommendations)

if __name__ == "__main__":
  main()