__version__ = "1.0"

from Scraper import Scraper
from Plot import Plot
from os.path import exists
from os import environ
import json
import threading
from Const import *

# prevent kivy from parsing command line args
environ["KIVY_NO_ARGS"] = "1"  # nopep8

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder


class Plotter(App):
    def build(self):

        # get data which is a list of dictionaries, sorted by entry date
        potential_thread = None

        if exists(CACHE_PATH):
            # get catched data
            with open('data.json', 'r') as f:
                self.data = json.load(f)

            potential_thread = threading.Thread(
                target=self.init_scraper, name="Scraper-Initalizer")
            potential_thread.start()

        else:
            self.init_scraper()

        # get view
        Builder.load_file("app.kv")

        return Plot(self.data)

    def init_scraper(self):
        """Needs to be called to initalize the scraper, after refetching can be done by simply calling 'fetch_data' with 'self.scraper' as argument"""
        self.scraper = Scraper(DEBUG)
        self.fetch_data()
        print("Initalization done", len(self.data), self.data)

    def fetch_data(self) -> dict:
        # refetch data
        self.data = self.scraper.fetch_data(USERNAME, PASSWORD)

        # cache data
        data_json = json.dumps(self.data, indent=4)

        with open('data.json', 'w') as f:
            f.write(data_json)


if __name__ == '__main__':
    app = Plotter()
    app.run()
