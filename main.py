import requests
from bs4 import BeautifulSoup

#Fetch IMDB HTML
def fetch_imdb(movie_title):
    imdb_website = f'https://www.imdb.com/title/{movie_title}/'
    imdb_results = requests.get(imdb_website)

    if imdb_results.status_code == 200:
        return imdb_results.content
    else:
        print(f"Could not find an IMDB page for {movie_title}")

#Fetch Rotten Tomatoes HTML
def fetch_rotten_tomatoes(movie_title):
    rotten_tomatoes_website = f'https://www.rottentomatoes.com/m/{movie_title.replace(" ", "_")}'
    rotten_tomatoes_results = requests.get(rotten_tomatoes_website)

    if rotten_tomatoes_results.status_code == 200:
        return rotten_tomatoes_results.content
    else:
        print(f"Could not find a Rotten Tomatoes page for {movie_title}")

#Fetch Metacritic HTML
def fetch_meta_critic(movie_title):
    formatted_title = movie_title.lower().replace(" ", "_")
    meta_critic_website = f'https://www.metacritic.com/movie/{formatted_title}'
    meta_critic_results = requests.get(meta_critic_website)

    if meta_critic_results.status_code == 200:
        return meta_critic_results.content
    else:
        print(f"Could not find a Meta Critic page for {movie_title}")

#Parse IMDB
def parse_imdb(html):
    imdb_soup = BeautifulSoup(html, 'html.parser')
    imdb_title = imdb_soup.find('h1').text.strip()
    imdb_rating_element = imdb_soup.find('span', itemprop='ratingValue')
    if imdb_rating_element:
        imdb_rating = imdb_rating_element.text.strip()
    else:
        imdb_rating = 'NA'
    return ("\nMovie Title:\n" + {imdb_title} + "\nMovie Rating: " + imdb_rating)

def parse_rotten_tomatoes(html):
    rotten_tomatoes_soup = BeautifulSoup(html, 'html.parser')
    rotten_tomatoes_rating = rotten_tomatoes_soup.find('score-board').find('span', class_='mop-ratings-wrap__percentage').text.strip()
    return rotten_tomatoes_rating

def parse_meta_critic(html):
    meta_critic_soup = BeautifulSoup(html, 'html.parser')
    meta_critic_element = meta_critic_soup.find('div', class_='metascore_w')
    if meta_critic_element:
        meta_critic_rating = meta_critic_element.text.strip()
    else:
        meta_critic_rating = 'NA'
    return meta_critic_rating
    
def movie_ratings(movie_title):
    imdb_html = fetch_imdb(movie_title)
    rotten_tomatoes_html = fetch_rotten_tomatoes(movie_title)
    meta_critic_html = fetch_meta_critic(movie_title)

    if imdb_html:
        imdb_title, imdb_rating = parse_imdb(imdb_html)
    else:
        imdb_title, imdb_rating = movie_title, 'NA'
    
    if rotten_tomatoes_html:
        rotten_tomatoes_score = parse_rotten_tomatoes(rotten_tomatoes_html)
    else:
        rotten_tomatoes_score = 'NA'
    
    if meta_critic_html:
        metascore = parse_meta_critic(meta_critic_html)
    else:
        metascore = 'NA'
    

    return {
        'Title': imdb_title,
        '\nIMDB Rating': imdb_rating,
        '\nRotten Tomatoes Rating': rotten_tomatoes_score,
        '\nMetacritic Score': metascore
    }


movie_title = input("Please enter a movie title:\n")
movie_ratings(movie_title)
