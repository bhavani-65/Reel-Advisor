import tarfile
import pickle
import streamlit as st
import requests
import pandas as pd
import os

# URL to the GitHub release asset
# RELEASE_URL = 'https://github.com/bhavani-65/Reel-Advisor/releases/download/v1.0.0/similarity.tar.gz'
tar_file_path = 'similarity.tar.gz.part-aa'
extract_folder = os.path.dirname(tar_file_path)

# # Function to download the file from the release URL
# def download_file(url, dest_path):
#     with requests.get(url, stream=True) as r:
#         r.raise_for_status()
#         with open(dest_path, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=8192):
#                 f.write(chunk)

# # Download the tar.gz file if it does not exist
# if not os.path.exists(tar_file_path):
#     download_file(RELEASE_URL, tar_file_path)

# Extract the tar.gz file
with tarfile.open(tar_file_path, 'r:gz') as tar:
    tar.extractall(path=extract_folder)

# Load similarity.pkl
pickle_file_path = os.path.join(extract_folder, 'similarity.pkl')
similarity = pickle.load(open(pickle_file_path, 'rb'))

# Load movies_dict.pkl
movies_dict_path = 'movies_dict.pkl'
movies_dict = pickle.load(open(movies_dict_path, 'rb'))
movies = pd.DataFrame(movies_dict)

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3615ea3be5317db32db3c49f897cd73d&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Function to recommend movies

    return recommended_movies

# Streamlit app starts here
st.title('Reel-Advisor')
option = st.selectbox('Select your movie:', movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movies = recommend(option, similarity)
    st.write("Top 10 Recommendations:")
    st.write("---")
    col1, col2, col3, col4, col5 = st.columns(5)  # 5 columns for 10 recommendations (2 movies per column)
    for i in range(0, 10, 2):  # Iterate through recommended_movies two at a time
        with col1:
            st.image(recommended_movies[i]['poster_url'], caption=recommended_movies[i]['title'], use_column_width=True)
        with col2:
            if i + 1 < 10:  # Ensure not to exceed list length
                st.image(recommended_movies[i + 1]['poster_url'], caption=recommended_movies[i + 1]['title'], use_column_width=True)
        # Repeat for col3, col4, and col5 if needed
