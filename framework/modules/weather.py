
import http.client
import json
import sqlite3
from pprint import pprint
from time import sleep
import time

from moduleb import mobase


class weather(mobase):

    def __init__(self) -> None:
        super().__init__(
                "Weather", 
                "Manages Weather", 
                "0.0.1",
            )
        self.lgr = self.logger(__name__)
        self.create_weather_database()

        self.running = True

        self.run()

    def fetch_weather(self, type=None, city=None) -> dict:

        if type is None:
            type = 'weather'
        if city is None:
            city = self.config['weather']['location']

        http_conn = http.client.HTTPSConnection("api.openweathermap.org")

        query = "q={}".format(city)
        key = "appid={}".format(self.config['weather']['key'])
        units = "units={}".format(self.config['weather']['units'] or 'metric')
        params = "&".join([key, query, units])

        http_conn.request("GET", "/data/2.5/{}?{}".format(type,params))
        http_res = http_conn.getresponse()
        decoded = json.loads(http_res.read().decode("utf-8"))

        return decoded

        # file = open("framework/modules/weather/weather.json", "w")
        # json.dump(decoded, file, indent=4)
        # file.close()

    def get_current_weather_from_api(self, city=None) -> None:
        try:
            res = self.fetch_weather(city=city)

            if res['cod'] == '429':
                raise Exception('API rate limit exceeded')
            elif str(res['cod']) != '200':
                raise Exception('API returned error: {}'.format(res['cod']))

            data = (
                self.create_id(),
                res['dt'],
                res['timezone'],
                res['name'],
                res['sys']['country'],
                res['coord']['lon'],
                res['coord']['lat'],
                res['base'],
                res['weather'][0]['description'],
                res['weather'][0]['icon'],
                res['weather'][0]['main'],
                res['main']['temp'],
                res['main']['feels_like'],
                res['main']['temp_min'],
                res['main']['temp_max'],
                res['main']['pressure'],
                res['main']['humidity'],
                res['visibility'],
                res['wind']['speed'],
                res['wind']['deg'],
                res['clouds']['all'],
            )

            self.push_weather_data(data)

        except Exception as e:
            self.lgr.error("Error fetching current weather: {}".format(e))

    def get_forecast_from_api(self, city=None) -> None:
        try:
            res = self.fetch_weather(type='forecast', city=city)

            if res['cod'] == '429':
                raise Exception('API rate limit exceeded')
            elif str(res['cod']) != '200':
                raise Exception('API returned error: {}'.format(res['cod']))

            weather_list = res['list']
            city = res['city']
            res_weather_list = []

            for weather in weather_list:
                res_weather_list.append(
                    (
                        self.create_id(),
                        weather['dt'],
                        city['timezone'],
                        city['name'],
                        city['country'],
                        city['coord']['lon'],
                        city['coord']['lat'],
                        None,
                        weather['weather'][0]['description'],
                        weather['weather'][0]['icon'],
                        weather['weather'][0]['main'],
                        weather['main']['temp'],
                        weather['main']['feels_like'],
                        weather['main']['temp_min'],
                        weather['main']['temp_max'],
                        weather['main']['pressure'],
                        weather['main']['humidity'],
                        weather['visibility'],
                        weather['wind']['speed'],
                        weather['wind']['deg'],
                        weather['clouds']['all'], 
                    )
                )

            for data in res_weather_list:
                self.push_weather_data(data)

        except Exception as e:
            self.lgr.error("Error fetching forecast: {}".format(e))

    def create_weather_database(self) -> None:
        self.connect()

        weather_db_query = '''
            CREATE TABLE IF NOT EXISTS weather(
                id STRING PRIMARY KEY,
                dt INTEGER,
                timezone INTEGER,
                city STRING,
                country STRING,
                lon FLOAT,
                lat FLOAT,
                base STRING,
                description STRING,
                icon STRING,
                main STRING,
                temp FLOAT,
                feels_like FLOAT,
                temp_min FLOAT,
                temp_max FLOAT,
                pressure INTEGER,
                humidity INTEGER,
                visibility INTEGER,
                wind_speed FLOAT,
                wind_deg FLOAT,
                clouds INTEGER
            )
        '''

        try:
            self.cursor.execute(weather_db_query)
            self.conn.commit()
            self.close()
        except sqlite3.OperationalError as e:
            self.lgr.error("Error pushing weather data from create_weather_database: {}".format(e))
    
    def push_weather_data(self, _data) -> None:
        self.connect()

        push_weather_data = '''
            INSERT INTO weather VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''

        try:
            self.cursor.execute(push_weather_data, _data)
            self.conn.commit()
            self.close()
        except sqlite3.OperationalError as e:
            self.lgr.error("Error pushing weather data from push_weather_data: {}".format(e))

    def check_if_latest_weather_is_outdated(self) -> bool:
        self.connect()

        try:
            result = self.cursor.execute('''
                SELECT dt FROM weather ORDER BY dt DESC LIMIT 1
            ''').fetchone()
            self.close()

            if result is None:
                return True

            if result[0] < int(time.time()):
                return True

            return False

        except sqlite3.OperationalError as e:
            self.lgr.error("Error checking if latest weather is outdated: {}".format(e))

    def get_closest_weather_data_by_date_from_curret_time(self, _time=None):
        
        if _time is None:
            _time = int(time.time())

        self.connect()

        get_current_data = '''
            SELECT * FROM weather WHERE dt <= ? ORDER BY dt DESC LIMIT 1
        '''

        try:
            result = self.cursor.execute(get_current_data, (_time,)).fetchone()
            self.close()

            return result

        except sqlite3.OperationalError as e:
            self.lgr.error("Error getting closest weather data by date from current time: {}".format(e))
        except Exception as e:
            self.lgr.error("Error : {}".format(e))


    @mobase.run_in_thread
    def get_latest_weather_if_database_not_lastest(self) -> None:
        self.lgr.info("Database is dated: {}".format(self.check_if_latest_weather_is_outdated()))
        while self.running:
            if self.check_if_latest_weather_is_outdated():
                self.lgr.info("Fetching latest weather data")
                self.get_current_weather_from_api()
                self.get_forecast_from_api()
            sleep(15)

    @mobase.run_in_thread
    def run(self):
        self.get_latest_weather_if_database_not_lastest()
        sleep(.1) # put a small delay to stop getting an error
        # get_weather = self.get_closest_weather_data_by_date_from_curret_time()
        