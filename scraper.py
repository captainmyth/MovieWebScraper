from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from imdb import Cinemagoer

app = Flask(__name__)

#Global Variable(s)
imdb_year = ''

#Fetch IMDB HTML
def fetch_imdb(movie_title):
    try:
        ia = Cinemagoer()
        imdb_search = ia.search_movie(movie_title)
        if imdb_search:
            for movie in imdb_search:
                if movie_title.lower() == movie['title'].lower():
                    imdb_movie = ia.get_movie(movie.movieID)
                    return imdb_movie
        else:
            print(f'Could not find the IMDB page for {movie_title}')
    except Exception as e:
        print(f'There was an error retrieving information from IMDB: {e}')
        return None

    

#Fetch Rotten Tomatoes HTML
def fetch_rotten_tomatoes(movie_title, year):
    try:
        movie_title = movie_title.replace(" ", "_").replace("&", "and").lower()
        rotten_tomatoes_website = f'https://www.rottentomatoes.com/m/{movie_title}'
        rotten_tomatoes_results = requests.get(rotten_tomatoes_website)

        if rotten_tomatoes_results.status_code == 200:
            rotten_tomatoes_html = rotten_tomatoes_results.content
            rotten_tomatoes_soup = BeautifulSoup(rotten_tomatoes_html, 'html.parser')
            rotten_tomatoes_div = rotten_tomatoes_soup.find('div', class_='media-scorecard')

            if rotten_tomatoes_div:
                rotten_tomatoes_element = rotten_tomatoes_div.find('rt-text')
                if rotten_tomatoes_element:
                    rotten_tomatoes_rating = rotten_tomatoes_element.text.strip()
                    return rotten_tomatoes_rating
            
        if year:    
            rotten_tomatoes_website = f'https://www.rottentomatoes.com/m/{movie_title}_{year}'
            rotten_tomatoes_results = requests.get(rotten_tomatoes_website)

            if rotten_tomatoes_results.status_code == 200:
                rotten_tomatoes_html = rotten_tomatoes_results.content
                rotten_tomatoes_soup = BeautifulSoup(rotten_tomatoes_html, 'html.parser')
                rotten_tomatoes_div = rotten_tomatoes_soup.find('div', class_='media-scorecard')

                if rotten_tomatoes_div:
                    rotten_tomatoes_element = rotten_tomatoes_div.find('rt-text')
                    if rotten_tomatoes_element:
                        rotten_tomatoes_rating = rotten_tomatoes_element.text.strip()
                        return rotten_tomatoes_rating
            
            else:
                print(f'Could not find the Rotten Tomatoes Tomatometer for {movie_title}')
                return None
    except Exception as e:
        print(f'There was an error retrieving information from Rotten Tomatoes: {e}')
        return None

#Fetch Metacritic HTML
def fetch_meta_critic(movie_title):
    try:
        movie_title = movie_title.lower().replace(" ", "-")
        meta_critic_website = f'https://www.metacritic.com/movie/{movie_title}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        meta_critic_results = requests.get(meta_critic_website, headers=headers)

        if meta_critic_results.status_code == 200:
            return meta_critic_results.content
        else:
            print(f"Could not find a Meta Critic page for {movie_title}")
    except Exception as e:
        print(f'There was an error retrieving information from Metacritic: {e}')
        return None

#Parse IMDB
def parse_imdb(html):
    imdb_title = html.get('title', 'NA')
    imdb_rating = html.get('rating', 'NA')
    imdb_year = html.get('year', 'NA')
    return imdb_title, str(imdb_rating), str(imdb_year)

def parse_meta_critic(html):
    meta_critic_soup = BeautifulSoup(html, 'html.parser')
    meta_critic_div = meta_critic_soup.find('div', class_='c-productScoreInfo_scoreNumber u-float-right')
    if meta_critic_div:
        meta_critic_element = meta_critic_div.find('span')
        if meta_critic_element:
            meta_critic_rating = meta_critic_element.text.strip()
            return meta_critic_rating
    else:  
        meta_critic_rating = 'NA'
    return meta_critic_rating

def movie_ratings(movie_title):
    try:
        imdb_html = fetch_imdb(movie_title)

        if imdb_html:
            imdb_title, imdb_rating, imdb_year = parse_imdb(imdb_html)
        else:
            imdb_title, imdb_rating = movie_title, 'NA'


        rotten_tomatoes_html = fetch_rotten_tomatoes(movie_title, imdb_year)

        if rotten_tomatoes_html:
            rotten_tomatoes_rating = fetch_rotten_tomatoes(movie_title, imdb_year)

        meta_critic_html = fetch_meta_critic(movie_title)
        if meta_critic_html:
            meta_critic_score = parse_meta_critic(meta_critic_html)

            return {
                'Title': imdb_title,
                'Year': imdb_year,
                'IMDB Rating': imdb_rating,
                'Rotten Tomatoes Tomatometer': rotten_tomatoes_rating,
                'Metacritic Metascore': meta_critic_score
            }
    except Exception as e:
        print(f'There was an error searching for {movie_title}')
        return {
                'Title': 'Not Found',
                'Year': 'Not Found',
                'IMDB Rating': 'Not Found',
                'Rotten Tomatoes Tomatometer': 'Not Found',
                'Metacritic Metascore': 'Not Found'
            }
    


    
@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        movie_information = {}
        if request.method == "POST":
            movie_title = request.form['movie_title']
            movie_information = movie_ratings(movie_title)
        return render_template('index.html', movie_information=movie_information)
    except Exception as e:
        print(f"There was an error searching for {movie_title}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
