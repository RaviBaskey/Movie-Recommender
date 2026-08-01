# 🎬 Content-Based Movie Recommendation Engine

## 📖 Overview

A machine learning-powered recommendation system that suggests movies based on content similarity. Using Natural Language Processing (NLP) techniques, the engine analyzes movie metadata — such as plot overviews, genres, cast, and crew — to find and recommend films that closely match a user's favorite selections.

The system is served through a **Flask** web application with a clean UI, and fetches live movie posters from the **TMDB API**.

---

## 🚀 Key Features

- **Content-Based Filtering** — Recommends movies purely based on textual features of films, ensuring recommendations are highly relevant to the selected movie's themes and genre.
- **TF-IDF Vectorization** — Converts text data into meaningful numerical representations, penalizing overly common words and highlighting unique keywords that define a movie.
- **Cosine Similarity** — Calculates mathematical distance between movie vectors in high-dimensional space to accurately rank and retrieve the top 5 most similar movies.
- **Live Movie Posters** — Fetches real-time poster images from the TMDB API for a rich visual experience.
- **Google Drive Integration** — Pre-computed model files (`.pkl`) are automatically downloaded from Google Drive on first run via `gdown`.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.x |
| **Web Framework** | Flask |
| **ML / NLP** | scikit-learn (TF-IDF Vectorizer, Cosine Similarity) |
| **Data Manipulation** | pandas, numpy |
| **API** | TMDB (The Movie Database) API |
| **Model Storage** | Google Drive + gdown |
| **Templating** | Jinja2 (via Flask) |
| **Production Server** | Gunicorn |

---

## 📂 Project Structure

```
Movie-Recommender/
├── app.py                      # Flask application (routes, recommendation logic)
├── Movie-Recommender.ipynb     # Jupyter Notebook (model training & exploration)
├── templates/
│   └── index.html              # Frontend UI template
├── movie_list.pkl              # Serialized movie metadata (auto-downloaded)
├── similarity.pkl              # Pre-computed cosine similarity matrix (auto-downloaded)
├── requirements.txt            # Python dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8 or higher

### 1. Clone the Repository

```bash
git clone https://github.com/RaviBaskey/Movie-Recommender.git
cd Movie-Recommender
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The app will start on `http://0.0.0.0:5000`. On first launch, the pre-trained model files (`movie_list.pkl` and `similarity.pkl`) will be **automatically downloaded** from Google Drive.

> **Note:** The similarity matrix file is ~185 MB. The initial download may take a few minutes depending on your internet connection.

---

## 🧠 How It Works

1. **Data Preprocessing** — The dataset is cleaned and relevant features (genres, keywords, cast, director, and overview) are merged into a single `tags` column for every movie.

2. **Text Vectorization** — The `TfidfVectorizer` from scikit-learn transforms these textual tags into a sparse matrix of TF-IDF features.

3. **Similarity Calculation** — The `cosine_similarity` function computes the angle between movie vectors. A score closer to **1** implies a high degree of similarity.

4. **Recommendation Generation** — When a user selects a movie title:
   - The engine looks up its index in the dataset
   - Retrieves the similarity scores for that movie against all others
   - Sorts scores in descending order
   - Returns the **top 5 most similar movies** with their posters

5. **Poster Fetching** — Each recommended movie's poster is fetched in real-time from the TMDB API for visual display.

---

## 🖥️ Usage

1. Open the app in your browser at `http://localhost:5000`
2. Select a movie from the dropdown menu
3. Click **Recommend**
4. View the top 5 similar movies along with their posters

---

## 📊 Dataset

This project uses the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) from Kaggle. The dataset has been preprocessed and serialized into pickle files for efficient loading.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [TMDB](https://www.themoviedb.org/) for the movie data and poster API
- [Kaggle](https://www.kaggle.com/) for the TMDB 5000 Movie Dataset
- [scikit-learn](https://scikit-learn.org/) for the ML/NLP tools
