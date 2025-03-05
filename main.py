import streamlit as st
import pickle
import requests

movies = pickle.load(open("./model/movie_list.pkl", "rb"))
similarity = pickle.load(open("./model/similarity.pkl", "rb"))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=04628a40ec1d6bbc6536f5367f2bb1e5&language=en-US"
    response = requests.get(url)
    data = response.json()
    if "poster_path" in data and data["poster_path"]:
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    return "https://via.placeholder.com/200x300?text=No+Image"

def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    index = movies[movies["title"] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])), 
        reverse=True, 
        key=lambda x: x[1]
    )

    recommended_movies = []
    recommended_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Choose a movie:", movies["title"].values)

if st.button("Recommend"):
    recommendations, posters = recommend(selected_movie)

    if recommendations:
        st.subheader("Recommended Movies:")
        cols = st.columns(5)

        for i, col in enumerate(cols):
            with col:
                st.image(posters[i], use_container_width=True)
                st.write(f"**{recommendations[i]}**")
    else:
        st.warning("No recommendations found. Try another movie!")
