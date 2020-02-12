import requests
import bz2
import os


class Downloading:
    @staticmethod
    def download_Russia_base():
        """"Загрузка OSM базы для России"""
        path = os.path.join("./data", "Russia.bz2")
        with requests.get("https://download.geofabrik.de/russia-latest.osm.bz2", stream=True) as r:
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        zipfile = bz2.BZ2File(path)
        new_path = os.path.join("./data", "Russia.osm")
        with open(new_path, 'wb') as d:
            for string in zipfile:
                d.write(string)
