import requests
from bs4 import BeautifulSoup
from imdb import Cinemagoer


#Fetch IMDB HTML
def fetch_imdb(movie_title):
    ia = Cinemagoer()
    imdb_search = ia.search_movie(movie_title)
    if imdb_search:
        for movie in imdb_search:
            if movie_title.lower() == movie['title'].lower():
                imdb_movie = ia.get_movie(movie.movieID)
        return imdb_movie
    else:
        print(f'Could not find the IMDB page for {movie_title}')

    

#Fetch Rotten Tomatoes HTML
'''def fetch_rotten_tomatoes(movie_title):
    rotten_tomatoes_website = f'https://www.rottentomatoes.com/m/{movie_title.replace(" ", "_")}'
    rotten_tomatoes_results = requests.get(rotten_tomatoes_website)

    if rotten_tomatoes_results.status_code == 200:
        return rotten_tomatoes_results.content
    else:
        print(f"Could not find a Rotten Tomatoes page for {movie_title}")
'''
#Fetch Metacritic HTML
'''def fetch_meta_critic(movie_title):
    formatted_title = movie_title.lower().replace(" ", "_")
    meta_critic_website = f'https://www.metacritic.com/movie/{formatted_title}'
    meta_critic_results = requests.get(meta_critic_website)

    if meta_critic_results.status_code == 200:
        return meta_critic_results.content
    else:
        print(f"Could not find a Meta Critic page for {movie_title}")
'''
#Parse IMDB
def parse_imdb(html):
    imdb_title = html.get('title', 'NA')
    imdb_rating = html.get('rating', 'NA')
    return imdb_title, str(imdb_rating)

'''def parse_rotten_tomatoes(html):
    rotten_tomatoes_soup = BeautifulSoup(html, 'html.parser')
    rotten_tomatoes_rating = rotten_tomatoes_soup.find('score-board').find('span', class_='mop-ratings-wrap__percentage').text.strip()
    return rotten_tomatoes_rating
'''
'''def parse_meta_critic(html):
    meta_critic_soup = BeautifulSoup(html, 'html.parser')
    meta_critic_element = meta_critic_soup.find('div', class_='metascore_w')
    if meta_critic_element:
        meta_critic_rating = meta_critic_element.text.strip()
    else:
        meta_critic_rating = 'NA'
    return meta_critic_rating
'''    
def movie_ratings(movie_title):
    imdb_html = fetch_imdb(movie_title)
    #rotten_tomatoes_html = fetch_rotten_tomatoes(movie_title)
    #meta_critic_html = fetch_meta_critic(movie_title)

    if imdb_html:
        imdb_title, imdb_rating = parse_imdb(imdb_html)
    else:
        imdb_title, imdb_rating = movie_title, 'NA'
    return {
        'Title ': imdb_title,
        'IMDB Rating ': imdb_rating
    }

    


movie_title = input("Please enter a movie title:\n")
print(movie_ratings(movie_title))
