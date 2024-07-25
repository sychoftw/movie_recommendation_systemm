import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


similarity = pickle.load(open('similarity.pkl', 'rb'))

with open('movie_dict.pkl', 'rb') as file:
    movie_dict = pickle.load(file)

movies = pd.DataFrame(movie_dict)

st.title('Movie Recommendation System')

options = list(movies['title'])

option = st.selectbox('Select an option', options)

if st.button('Recommend'):
    names, posters = recommend(option)
    cols = st.columns(5)

    for i, col in enumerate(cols):
        if i < len(names):
            with col:
                st.text(names[i])
                st.image(posters[i])




