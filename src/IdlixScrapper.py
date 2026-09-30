import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote  # FIX 1: Import unquote untuk memproses nama video

class IdlixScrapper:
    def __init__(self):
        # FIX 2: Mengganti IP lama dengan URL baru dan menambahkan BASE_WEB_URL
        self.API = 'https://z2.idlixku.com'
        self.BASE_WEB_URL = 'https://z2.idlixku.com'

    def get_genre(self):
        r = requests.get(self.API + '/genre/')
        soup = BeautifulSoup(r.text, 'html.parser')
        genre = soup.find('div', class_='container').find_all('a')
        data_genre = []
        for i in genre:
            data_genre.append(i.get('title').replace(' Genre', ''))
        return data_genre

    def get_movie_in_genre(self, genre, page=1):
        r = requests.get(self.API + '/genre/' + genre + '/page/' + str(page))
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
        r = requests.get(self.API + '/trending/page/' + str(page) + '/?get=movies')
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
        r = requests.get(self.API + '/movie/' + link + '/')
        soup = BeautifulSoup(r.text, 'html.parser')

        tag_content = soup.find('div', class_='sgeneros')
        content_tag = []
        for i in tag_content:
            content_tag.append(i.findNext('a').text)

        if soup.find('span', class_='CR rated'):
            rating = soup.find('span', class_='CR rated').text
        else:
            rating = '-'

        if soup.find('span', class_='tagline'):
            tagline = soup.find('span', class_='tagline').text
        else:
            tagline = '-'
            
        return {
            'img': soup.find('div', class_='poster').find('img').get('src'),
            'title': soup.find('div', class_='data').find('h1').text,
            'description': soup.find('div', class_='wp-content').find('p').text,
            'tagline': tagline,
            'date': soup.find('span', class_='date').text,
            'country': soup.find('span', class_='country').text,
            'duration': soup.find('span', class_='runtime').text,
            'rating': rating,
            'tag': content_tag[:-1],
        }

    def get_tv_trending(self, page=1):
        r = requests.get(self.API + '/trending/page/' + str(page) + '/?get=tv')
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
        r = requests.get(self.API + '/tvseries/' + link + '/')
        soup = BeautifulSoup(r.text, 'html.parser')

        content_tag = []
        for i in soup.find('div', class_='sgeneros'):
            content_tag.append(i.findNext('a').text)

        data_sessions = []
        for i in soup.findAll('div', class_='se-c'):
            for j in i.find('ul', class_='episodios').findAll('li'):
                data_sessions.append({
                    'Session ' + i.find('span', class_='se-t').text: {
                        'title': j.find('a').text,
                        'date': j.find('span', class_='date').text,
                        'image': j.find('img').get('src'),
                        'link': j.find('a').get('href')
                    },
                })

        if soup.find('span', class_='CR rated'):
            rating = soup.find('span', class_='CR rated').text
        else:
            rating = '-'

        if soup.find('span', class_='tagline'):
            tagline = soup.find('span', class_='tagline').text
        else:
            tagline = '-'

        return {
            'image': soup.find('div', class_='poster').find('img').get('src'),
            'title': soup.find('div', class_='data').find('h1').text,
            'description': soup.find('div', class_='wp-content').find('p').text,
            'tagline': tagline,
            'date': soup.find('span', class_='date').text,
            'rating': rating,
            'tag': content_tag[:-1],
            'sessions': data_sessions,
            'total_movie': len(data_sessions)
        }

    def get_network_netflix(self, page=1):
        r = requests.get(self.API + '/network/netflix/page/' + str(page) + '/')
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
        r = requests.get(self.API + '/tvseries/page/' + str(page) + '/')
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
        r = requests.get(self.API + '/movie/page/' + str(page) + '/')
        soup = BeautifulSoup(r.text, 'html.parser')
        movie = soup.find('div', class_='animation-2 items full').findAll('article', class_='item movies')
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

    # ==========================================
    # Fungsi Baru yang Sudah Diperbaiki
    # ==========================================
    def get_video_data(self, url):
        if not url:
            return {'status': False, 'message': 'URL is required'}

        if not url.startswith(self.BASE_WEB_URL):
            return {'status': False, 'message': 'Invalid URL'}

        # FIX 3: Ganti self.request.get menjadi requests.get
        request = requests.get(url=url)
        if request.status_code != 200:
            return {'status': False, 'message': 'Failed to get video page'}

        bs = BeautifulSoup(request.text, 'html.parser')

        # ----------------------------------------------------------------------
        # 1. GET VIDEO ID (fallback untuk episode / tvseries)
        # ----------------------------------------------------------------------
        meta_postid = bs.find('meta', {'id': 'dooplay-ajax-counter'})
        if not meta_postid:
            # Fallback lain: some themes use data-post-id
            post_id_holder = bs.find(attrs={'data-postid': True})
            if post_id_holder:
                self.video_id = post_id_holder['data-postid']
            else:
                return {'status': False, 'message': 'Video ID not found'}
        else:
            self.video_id = meta_postid.get('data-postid')

        # ----------------------------------------------------------------------
        # 2. GET TITLE (ROBUST)
        # ----------------------------------------------------------------------
        video_name = None

        # Try itemprop="name"  (movie)
        meta_name = bs.find('meta', {'itemprop': 'name'})
        if meta_name:
            video_name = meta_name.get('content')

        # Try og:title (episodes)
        if not video_name:
            og_title = bs.find('meta', {'property': 'og:title'})
            if og_title:
                video_name = og_title.get('content')

        # Try title tag
        if not video_name and bs.title:
            video_name = bs.title.text

        # Try h1
        if not video_name:
            h1 = bs.find('h1')
            if h1:
                video_name = h1.get_text(strip=True)

        # Last fallback
        if not video_name:
            video_name = "Unknown_Title"

        self.video_name = unquote(video_name)

        # ----------------------------------------------------------------------
        # 3. GET POSTER (fallbacks)
        # ----------------------------------------------------------------------
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

        # DONE
        return {
            'status': True,
            'video_id': self.video_id,
            'video_name': self.video_name,
            'poster': self.poster
        }
