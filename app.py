import pickle
import pandas as pd
import requests
import gdown
from flask import Flask, render_template, request

app = Flask(__name__)

#Get file from Google Drive
# https://drive.google.com/file/d/THIS_IS_THE_FILE_ID/view?usp=sharing
#paste the only link between d/   and  /view

MOVIE_LIST_FILE_ID = '1ef4ccUzgF7vQb0z85-CUqpsNeH64SGkO'
SIMILARITY_FILE_ID = '1q-HD9LnhP2G1Pt8sh974cUa9oPueMZGJ'

#download file will be here
MOVIE_LIST_PATH = 'movie_list.pkl'
SIMILARITY_PATH = 'similarity.pkl'

def download_files_from_gdrive():
    # downloads the pickle files from Google Drive if they don't exist.
    try:
        # check for movie list file
        try:
            with open(MOVIE_LIST_PATH, 'rb') as f:
                pass # File exists
        except FileNotFoundError:
            gdown.download(id=MOVIE_LIST_FILE_ID, output=MOVIE_LIST_PATH, quiet=False)

        # check for similarity file
        try:
            with open(SIMILARITY_PATH, 'rb') as f:
                pass # File exists
        except FileNotFoundError:
            gdown.download(id=SIMILARITY_FILE_ID, output=SIMILARITY_PATH, quiet=False)

    except Exception as e:
        print(f"CRITICAL: File download failed: {e}")
        print("Please ensure 'gdown' is installed and the File IDs are correct.")
        # exit if files can't be loaded
        raise

def fetch_poster(movie_id):
    #fetches the movie poster path from the TMDB API.
    placeholder_image = "https://placehold.co/500x750/333333/FFFFFF?text=Poster+Not+Found"
    
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=b08027ce10ed757dbd6c0cbd49c71bc6&language=en-US".format(movie_id)
        response = requests.get(url)
        response.raise_for_status()  # This will raise an error for bad responses (404, 500, etc.)
        
        data = response.json()
        poster_path = data.get('poster_path')
        
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return placeholder_image
            
    except requests.exceptions.RequestException as e:
        # Log important errors
        print(f"API request error for movie_id {movie_id}: {e}")
        return placeholder_image
    except Exception as e:
        print(f"An unexpected error occurred for movie_id {movie_id}: {e}")
        return placeholder_image

def recommend(movie):
    #recommends 5 similar movies based on the selected movie.
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommendations = []
        
        for i in distances[1:6]:  # Get top 5 movies (index 0 khud movie h vector m)
            movie_id = movies.iloc[i[0]].movie_id
            poster = fetch_poster(movie_id)
            name = movies.iloc[i[0]].title
            recommendations.append({"name": name, "poster": poster})
            
        return recommendations
        
    except Exception as e:
        print(f"Error during recommendation for movie '{movie}': {e}")
        return []

# download and Load models
# run only once
download_files_from_gdrive()

# Load pickle files in memory
movies_df = pickle.load(open(MOVIE_LIST_PATH, 'rb'))
movies = pd.DataFrame(movies_df)  # Ensure it's a pandas DataFrame
similarity = pickle.load(open(SIMILARITY_PATH, 'rb'))
movie_titles = movies['title'].values


# Flask Routes

@app.route('/')
def home():
    #Renders the main page with the movie dropdown.
    return render_template('index.html', movie_list=movie_titles)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    #Handles the form submission and returns recommendations.

    selected_movie = request.form['movie']
    recommendations = recommend(selected_movie)
    
    # Re-render the same page, but now with the recommendations list
    return render_template('index.html', 
                           movie_list=movie_titles, 
                           recommendations=recommendations, 
                           selected_movie=selected_movie)

if __name__ == '__main__':
    # Set debug=False for production
    app.run(debug=False, host='0.0.0.0')

