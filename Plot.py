from os import environ

# prevent kivy from parsing command line args
environ["KIVY_NO_ARGS"] = "1"  # nopep8

from matplotlib import pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib import FigureCanvasKivyAgg


class Plot(BoxLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)

        self.data = data

        self.plot_time_total_sends()

    def plot_time_total_sends(self):

        sends_by_date = self.get_sends_by_date()

        x = list(sends_by_date.keys())                # dates of sends
        y = [len(y) for x, y in sends_by_date.items()]  # number of sends

        print(x, y, len(x), len(y))
        plt.plot(x, y)

        plt.xlabel('Sessions')
        plt.ylabel('Number of sends')

        box = self.ids.box
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def get_sends_by_date(self) -> dict:
        sends_by_date = {}

        for point in self.data:

            dmy = point["Date"]
            date = str(dmy[0]) + '.' + str(dmy[1]) + '.' + str(dmy[2])

            if date in sends_by_date:
                sends_by_date[date].append(point)
            else:
                sends_by_date[date] = [point]

        return sends_by_date
