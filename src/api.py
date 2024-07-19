import requests
import requests_cache
import src.database

requests_cache.install_cache('cache_name', expire_after=3600)

class api:
    def test():
        print()
        
        #r = requests.get('https://api.themoviedb.org/3/movie/11?api_key=9074e0579d84fd2ce0f82d4bbe3d89ac')
        # r = requests.get('https://api.themoviedb.org/3/movie/11', headers={'Authorization':'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MDc0ZTA1NzlkODRmZDJjZTBmODJkNGJiZTNkODlhYyIsIm5iZiI6MTcyMTM3OTY2My4wNjQ4MzksInN1YiI6IjY2OTk0MWIzNWM0ZGRiYjRkYWM5YTc5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tIys_6ekI2RUJKrGXO1wLWRfo-84Z8I2iErR26hwTvM'})
        
        #requests.headers['Authorization'] = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5MDc0ZTA1NzlkODRmZDJjZTBmODJkNGJiZTNkODlhYyIsIm5iZiI6MTcyMTM3OTY2My4wNjQ4MzksInN1YiI6IjY2OTk0MWIzNWM0ZGRiYjRkYWM5YTc5MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tIys_6ekI2RUJKrGXO1wLWRfo-84Z8I2iErR26hwTvM'
        #print(r.headers['Authorization'])

        # print(r)
        # print(r.status_code)

        url = "https://api.themoviedb.org/3/movie/popular?language=de-DE&page=1"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        print(response.text)




        





