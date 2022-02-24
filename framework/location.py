
import http.client
import json
import urllib.parse
import socket
import os
import sys
import sqlite3

import crud
from logger import get_logger

lgr = get_logger(__name__)

class location(crud.database):

    def __init__(self) -> None:
        self.db_path = 'retention/location.db'

        super().__init__(self.db_path)
        self.create_location_memory()

    def create_location_memory(self) -> None:
        self.connect()

        """
        create a database table for locations
        """

        location_memory_query = '''
            CREATE TABLE IF NOT EXISTS location_memory(
                id STRING PRIMARY KEY,
                licence STRING,
                osm_type STRING,
                osm_id INTEGER,
                boundingbox STRING,
                lat STRING,
                lon STRING,
                display_name STRING,
                class STRING,
                type STRING,
                importance INTEGER
            )
        '''

        try:
            self.cursor.execute(location_memory_query)
            self.conn.commit()
            self.close()
        except sqlite3.OperationalError as e:
            lgr.error("Error creating location_memory table: {}".format(e))
            sys.exit(1)

    def get_location_from_query_from_api(self, query):

        http_conn = http.client.HTTPSConnection("nominatim.openstreetmap.org")
        parsed_location = urllib.parse.quote(query)

        try:
            http_conn.request("GET", "/search/{}?format=json".format(parsed_location))
        except socket.gaierror as e:
            raise Exception("Could not connect to server: {}".format(e))

        http_res = http_conn.getresponse()
        decoded = json.loads(http_res.read().decode("utf-8"))

        if len(decoded) == 0:
            raise Exception("No results found for query: {}".format(query))

        return decoded[0]


if __name__ == '__main__':
    l = location()
    print(l.get_location_from_query_from_api('New York'))
