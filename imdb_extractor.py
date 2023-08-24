import requests
import time
import csv
import random
import concurrent.futures

from bs4 import BeautifulSoup

# =========================================================================== #

class IMDB_extractor(object):

    """
    Parâmetros:
        threads      -> número máximo de threads
        top_num      -> o número máximo de filmes/séries procurados. 
        content_type -> 'popular movies', 'popular series', 'best movies', 'best series'.
                        Os populares contém até 100 títulos, os melhores segundo o imdb, até 250.
    """

    def __init__(self, threads, top_num, content_type) -> None:
        self.max_threads = threads
        self.top_num = top_num
        self.content = content_type
        self.url = self._get_url()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
    # ---------------------------------------- #
    def _get_url(self):
        content_types = {
            'popular movies': 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm',
            'popular series': 'https://www.imdb.com/chart/tvmeter/?ref_=chtmvm_ql_5',
            'best movies': 'https://www.imdb.com/chart/top/?ref_=nv_mv_250',
            'best series': 'https://www.imdb.com/chart/toptv/?ref_=chtmvm_ql_6'
        }
        return content_types[self.content]
    # ---------------------------------------- #
    def extract_movie_details(self, movie_link):
        time.sleep(random.uniform(0, 0.2))
        response = BeautifulSoup(requests.get(movie_link, headers=self.headers).content, 'html.parser')
        movie_soup = response
        if movie_soup is not None:
            title = None
            date = None
            # ajustar o trecho abaixo de acordo com o site de um filme, exemplo : https://www.imdb.com/title/tt15398776/?ref_=chtmvm_t_1, usar inspecionar elemento para definir os elementos.
            movie_data = movie_soup.find('div', attrs={'class': 'sc-e226b0e3-3 jJsEuz'})
            if movie_data is not None:
                # h1 deve ser o título do nome do filme
                title = movie_data.find('h1').get_text()
                # date deve ser apenas a classe que representa o ano.
                date = movie_data.find('a', attrs={'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'}).get_text().strip()
            # rating é a nota do filme, por exemplo, 8.6.
            rating = movie_soup.find('span', attrs={'class': 'sc-bde20123-1 iZlgcd'}).get_text() if movie_soup.find(
                'span', attrs={'class': 'sc-bde20123-1 iZlgcd'}) else None
            # plot é o texto de sinopse do filme
            plot_text = movie_soup.find('span', attrs={'class': 'sc-466bb6c-0 kJJttH'}).get_text().strip() if movie_soup.find(
                'span', attrs={'class': 'sc-466bb6c-0 kJJttH'}) else None
            with open(f'{self.top_num} {self.content}.csv', mode='a') as file:
                movie_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                if all([title, date, rating, plot_text]):
                    print(title, date, rating, plot_text)
                    movie_writer.writerow([title, date, rating, plot_text])
    # ------------------------------------------------------------------- #
    def extract_movies(self, soup):
        # aqui são configurações de hierarquia da página, do ponto de encontro do filme até sua divisão e organização em elementos.
        movies_table = soup.find('div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')
        movies_table_rows = movies_table.find_all('li')
        movie_links = ['https://imdb.com' + movie.find('a')['href'] for movie in movies_table_rows][:(self.top_num + 1)]
        threads = min(self.max_threads, len(movie_links))
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.extract_movie_details, movie_links)
    # --------------------------------------------------------- #
    def run(self):
        start_time = time.time()
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        # # Main function to extract the 100 movies from IMDB Most Popular Movies
        self.extract_movies(soup)
        end_time = time.time()
        print('Total time taken: ', end_time - start_time)
# =========================================================================== #

def main():
    IMDB_extractor(threads=15, top_num=100, content_type='popular movies').run()

if __name__ == '__main__':
    main()
