import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

class IdlixScrapper:
    def __init__(self):
        # Samakan API dan BASE_WEB_URL ke domain utama yang terdeteksi aktif di browser
        self.API = 'https://z2.idlixku.com'
        self.BASE_WEB_URL = 'https://z2.idlixku.com'
        
        # Tambahkan Headers global untuk menyamar sebagai browser Android
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
            'Referer': self.API,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    def get_genre(self):
        r = requests.get(self.API + '/genre/', headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        genre = soup.find('div', class_='container').find_all('a')
        data_genre = []
        for i in genre:
            data_genre.append(i.get('title').replace(' Genre', ''))
        return data_genre

    def get_movie_in_genre(self, genre, page=1):
        r = requests.get(self.API + '/genre/' + genre + '/page/' + str(page), headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        movie = soup.findAll('article', class_='item movies')
        data_movie = []
        for i in movie:
            data_movie.append({
                'img': i.find('div', class_='poster').find('img').get('src'),
                'title': i.find('div', class_='data').find('a').text,
                'rating': i.find('div', class_='rating').text,
                'quality': i.find('div', class_='mepo').find('span').text,
                'slug': i.find('div', class_='poster').find('a').get('href').split('/')[-2],
                'date': i.find('div', class_='data').find('span').text,
                'link': i.find('div', class_='data').find('a').get('href')
            })
        return data_movie

    def get_movie_tranding(self, page=1):
        r = requests.get(self.API + '/trending/page/' + str(page) + '/?get=movies', headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        movie = soup.findAll('article', class_='item movies')
        data_movie = []
        for i in movie:
            data_movie.append({
                'img': i.find('div', class_='poster').find('img').get('src'),
                'title': i.find('div', class_='data').find('a').text,
                'rating': i.find('div', class_='rating').text,
                'quality': i.find('div', class_='mepo').find('span').text,
                'slug': i.find('div', class_='poster').find('a').get('href').split('/')[-2],
                'date': i.find('div', class_='data').find('span').text,
                'link': i.find('div', class_='data').find('a').get('href')
            })
        return data_movie

    def get_info_movie(self, link):
        r = requests.get(self.API + '/movie/' + link + '/', headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        tag_content = soup.find('div', class_='sgeneros')
        content_tag = []
        if tag_content:
            for i in tag_content:
                content_tag.append(i.findNext('a').text)

        rating_elem = soup.find('span', class_='CR rated')
        rating = rating_elem.text if rating_elem else '-'

        tagline_elem = soup.find('span', class_='tagline')
        tagline = tagline_elem.text if tagline_elem else '-'
            
        return {
            'img': soup.find('div', class_='poster').find('img').get('src') if soup.find('div', class_='poster') else '',
            'title': soup.find('div', class_='data').find('h1').text if soup.find('div', class_='data') else '',
            'description': soup.find('div', class_='wp-content').find('p').text if soup.find('div', class_='wp-content') else '',
            'tagline': tagline,
            'date': soup.find('span', class_='date').text if soup.find('span', class_='date') else '',
            'country': soup.find('span', class_='country').text if soup.find('span', class_='country') else '',
            'duration': soup.find('span', class_='runtime').text if soup.find('span', class_='runtime') else '',
            'rating': rating,
            'tag': content_tag[:-1],
        }

    def get_tv_trending(self, page=1):
        r = requests.get(self.API + '/trending/page/' + str(page) + '/?get=tv', headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        movie = soup.findAll('article', class_='item tvshows')
        data_movie = []
        for i in movie:
            data_movie.append({
                'img': i.find('div', class_='poster').find('img').get('src'),
                'title': i.find('div', class_='data').find('a').text,
                'rating': i.find('div', class_='rating').text,
                'slug': i.find('div', class_='poster').find('a').get('href').split('/')[-2],
                'date': i.find('div', class_='data').find('span').text,
                'link': i.find('div', class_='data').find('a').get('href')
            })
        return data_movie

    def get_info_tv(self, link):
        r = requests.get(self.API + '/tvseries/' + link + '/', headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')

        content_tag = []
        sgeneros = soup.find('div', class_='sgeneros')
        if sgeneros:
            for i in sgeneros:
                content_tag.append(i.findNext('a').text)

        data_sessions = []
        for i in soup.findAll('div', class_='se-c'):
            se_t = i.find('span', class_='se-t')
            episodios = i.find('ul', class_='episodios')
            if se_t and episodios:
                for j in episodios.findAll('li'):
                    data_sessions.append({
                        'Session ' + se_t.text: {
                            'title': j.find('a').text if j.find('a') else '',
                            'date': j.find('span', class_='date').text if j.find('span', class_='date') else '',
                            'image': j.find('img').get('src') if j.find('img') else '',
                            'link': j.find('a').get('href') if j.find('a') else ''
                        },
                    })

        rating_elem = soup.find('span', class_='CR rated')
        rating = rating_elem.text if rating_elem else '-'

        tagline_elem = soup.find('span', class_='tagline')
        tagline = tagline_elem.text if tagline_elem else '-'

        return {
            'image': soup.find('div', class_='poster').find('img').get('src') if soup.find('div', class_='poster') else '',
            'title': soup.find('div', class_='data').find('h1').text if soup.find('div', class_='data') else '',
            'description': soup.find('div', class_='wp-content').find('p').text if soup.find('div', class_='wp-content') else '',
            'tagline': tagline,
            'date': soup.find('span', class_='date').text if soup.find('span', class_='date') else '',
            'rating': rating,
            'tag': content_tag[:-1],
            'sessions': data_sessions,
            'total_movie': len(data_sessions)
        }

    def get_network_netflix(self, page=1):
        r = requests.get(self.API + '/network/netflix/page/' + str(page) + '/', headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        movie = soup.findAll('article', class_='item tvshows')
        data_movie = []
        for i in movie:
            data_movie.append({
                'img': i.find('div', class_='poster').find('img').get('src'),
                'title': i.find('div', class_='data').find('a').text,
                'rating': i.find('div', class_='rating').text,
                'slug': i.find('div', class_='poster').find('a').get('href').split('/')[-2],
                'date': i.find('div', class_='data').find('span').text,
                'link': i.find('div', class_='data').find('a').get('href')
            })
        return data_movie

    def get_serial_tv(self, page=1):
        r = requests.get(self.API + '/tvseries/page/' + str(page) + '/', headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        movie = soup.findAll('article', class_='item tvshows')
        data_movie = []
        for i in movie:
            data_movie.append({
                'img': i.find('div', class_='poster').find('img').get('src'),
                'title': i.find('div', class_='data').find('a').text,
                'rating': i.find('div', class_='rating').text,
                'slug': i.find('div', class_='poster').find('a').get('href').split('/')[-2],
                'date': i.find('div', class_='data').find('span').text,
                'link': i.find('div', class_='data').find('a').get('href')
            })
        return data_movie

    def get_movie_series(self, page=1):
        r = requests.get(self.API + '/movie/page/' + str(page) + '/', headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Tambahkan error handling jika div tidak ditemukan
        container = soup.find('div', class_='animation-2 items full')
        data_movie = []
        if container:
            movie = container.findAll('article', class_='item movies')
            for i in movie:
                data_movie.append({
                    'img': i.find('div', class_='poster').find('img').get('src'),
                    'title': i.find('div', class_='data').find('a').text,
                    'rating': i.find('div', class_='rating').text,
                    'slug': i.find('div', class_='poster').find('a').get('href').split('/')[-2],
                    'date': i.find('div', class_='data').find('span').text,
                    'link': i.find('div', class_='data').find('a').get('href')
                })
        return data_movie

    def get_video_data(self, url):
        if not url:
            return {'status': False, 'message': 'URL is required'}

        if not url.startswith(self.BASE_WEB_URL):
            return {'status': False, 'message': 'Invalid URL'}

        # Sisipkan headers di sini juga
        request = requests.get(url=url, headers=self.headers)
        if request.status_code != 200:
            return {'status': False, 'message': f'Failed to get video page. Status code: {request.status_code}'}

        bs = BeautifulSoup(request.text, 'html.parser')

        # 1. GET VIDEO ID
        meta_postid = bs.find('meta', {'id': 'dooplay-ajax-counter'})
        if not meta_postid:
            post_id_holder = bs.find(attrs={'data-postid': True})
            if post_id_holder:
                self.video_id = post_id_holder['data-postid']
            else:
                return {'status': False, 'message': 'Video ID not found'}
        else:
            self.video_id = meta_postid.get('data-postid')

        # 2. GET TITLE 
        video_name = None
        meta_name = bs.find('meta', {'itemprop': 'name'})
        if meta_name:
            video_name = meta_name.get('content')

        if not video_name:
            og_title = bs.find('meta', {'property': 'og:title'})
            if og_title:
                video_name = og_title.get('content')

        if not video_name and bs.title:
            video_name = bs.title.text

        if not video_name:
            h1 = bs.find('h1')
            if h1:
                video_name = h1.get_text(strip=True)

        if not video_name:
            video_name = "Unknown_Title"

        self.video_name = unquote(video_name)

        # 3. GET POSTER 
        poster = None
        itemprop_img = bs.find('img', {'itemprop': 'image'})
        if itemprop_img:
            poster = itemprop_img.get('src')

        if not poster:
            og_image = bs.find('meta', {'property': 'og:image'})
            if og_image:
                poster = og_image.get('content')

        if not poster:
            poster = ""

        self.poster = poster

        return {
            'status': True,
            'video_id': self.video_id,
            'video_name': self.video_name,
            'poster': self.poster
        }
