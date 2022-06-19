import pprint

import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox
import pandas as pd

from matplotlib.widgets import Button, Slider
from shapely import wkt
from datetime import datetime

from app_io import load_input
from ax_settings import Ax_settings
from app_plot import plot_graph_route, plot_segment_edge


def get_route_network_small():
    cz010 = ox.geocode_to_gdf({"country": "Czech Republic", "county": "Hlavní město Praha"})
    return ox.graph_from_polygon(cz010.geometry[0], network_type="drive", retain_all=True, clean_periphery=False,
                                 custom_filter='["highway"~"motorway|trunk|primary|secondary"]')


def get_route_network():
    polygon = wkt.loads(
        'POLYGON ((13.724566394419828 50.19289060261473, 13.724624076646098 50.194361634608306, 13.725407507883915 50.20353176943156, 13.727030703970772 50.212591039360454, 13.729479915601951 50.22146270772478, 13.73273439669673 50.23007162693597, 13.736766580128347 50.23834487502573, 13.73722502619708 50.23918499009526, 13.742785781981263 50.24820349501278, 13.749269501396627 50.25658304263669, 13.75660340116829 50.264229567989936, 13.85274250361999 50.35438032745427, 13.859676122021563 50.360311415306924, 13.86712148507786 50.365585828659555, 13.887069840949536 50.37839221695742, 13.897098899037916 50.38404327468892, 13.907710953897343 50.3885043004998, 14.224372255359832 50.500645809948224, 14.227550557168328 50.50177090820576, 14.239908823836469 50.50527061954408, 14.344749013441003 50.527802566378924, 14.35305605122234 50.529224635458945, 14.422295549068872 50.53809330082273, 14.426281886634536 50.5385228643055, 14.427941803785057 50.5386681381397, 14.436600685740588 50.53904891059604, 14.513647875752602 50.539094880318316, 14.51631535557383 50.53906088882698, 14.517867907538438 50.53902038736257, 14.526532300634619 50.538417052184606, 14.52736662315097 50.53832240236515, 14.537449721443808 50.53665289331485, 14.55747165046973 50.532276184677144, 14.558667894057924 50.532006996095895, 14.873261429355622 50.45918536031678, 14.884655216957656 50.4558236904255, 14.895569970595737 50.45113462085913, 15.046798329465934 50.37522689188502, 15.05651143996165 50.369649649507345, 15.065539928828201 50.363021185369405, 15.073770533539097 50.355424653651944, 15.113647550574498 50.31425148528919, 15.115558459690352 50.31222263812372, 15.185636696808746 50.23571048839469, 15.192028806094742 50.22798751136112, 15.197615527943944 50.219663331259476, 15.202340713882515 50.210821608959435, 15.206156874168489 50.2015512068076, 15.209025655079994 50.19194529553033, 15.210918224383331 50.182100417835954, 15.211815561106834 50.17211551812741, 15.211947867913311 50.1687661832719, 15.212025771466111 50.16489288956034, 15.212038270103891 50.14797290501892, 15.212036480276359 50.147296193649225, 15.212032804444867 50.14668645463974, 15.2116219379415 50.138213702470615, 15.197878734227068 49.987408289072526, 15.196520095721175 49.97774550469588, 15.194226169907084 49.96826113835655, 15.191018798468367 49.95904549573364, 15.186928520488555 49.95018632384531, 15.138865342947541 49.858168929650724, 15.133548871791826 49.84917026554016, 15.127322199214369 49.84077566192013, 15.120253345897817 49.83307682213004, 15.112419532576386 49.82615784892809, 15.103906336470205 49.820094325745806, 14.939667694035974 49.71560467813416, 14.931107506375543 49.71073349839335, 14.92210965151938 49.706728025532826, 14.748736476067517 49.63957169418094, 14.741197029968836 49.63699176276107, 14.733476099031098 49.63502033711935, 14.730210054433332 49.63432372655263, 14.725893253489303 49.63350172551746, 14.456976472803946 49.5883936461159, 14.451325496160992 49.587610757493, 14.45078411464789 49.587551437850685, 14.445816288647782 49.58713212820897, 14.371069795620809 49.58269630084507, 14.364192597991904 49.58252521574945, 14.362825766739622 49.582538243946125, 14.358985245070233 49.58264866291369, 14.357412474132884 49.582724142761656, 14.35499969785498 49.58286918208963, 14.353858007718847 49.5829516715782, 14.352112059125975 49.58309320182729, 14.350312353366434 49.58325496770625, 14.345885956477574 49.58375243498413, 14.181930710067464 49.60588661292304, 14.1731848173693 49.60746582546753, 14.172369016982028 49.60765090520118, 14.167959482742459 49.608757257469364, 14.102092299333297 49.626884361803214, 14.094294005140334 49.6293781283395, 14.086725849394588 49.63250147309564, 14.079438563157344 49.63623345958462, 14.07834502868634 49.63685124940702, 14.072767879390174 49.64024688909609, 13.950168346003593 49.72049210448177, 13.939940758574018 49.72816311243925, 13.85577338397978 49.80014053901855, 13.848921552371396 49.80658185301451, 13.842705100026736 49.813638328241616, 13.837179004083131 49.8212475585579, 13.832392136295514 49.829342249359165, 13.74299896361949 49.99815347753967, 13.73840262317609 50.00812033744601, 13.734926245591938 50.018530882136695, 13.732611708925099 50.029259701357944, 13.73148689515864 50.040177550773244, 13.72460361958404 50.184198497576006, 13.724566394419828 50.19289060261473))')
    return ox.graph_from_polygon(polygon, network_type="drive", retain_all=True, clean_periphery=False,
                                 custom_filter='["highway"~"motorway|trunk|primary|secondary"]')


def plot_timestamp_test(time, g, ax):
    if time == 1:
        plot_segment_edge(g, 1835840419, 409801399, ax, 1, 50)
    if time == 2:
        plot_segment_edge(g, 409801399, 29166269, ax, 50, 50)
        plot_segment_edge(g, 1835840419, 409801399, ax, 1, 50)
        plot_segment_edge(g, 409801399, 29166269, ax, 50, 50)
        plot_segment_edge(g, 29166269, 8811408, ax, 50, 30)
    if time == 3:
        plot_segment_edge(g, 1835840419, 409801399, ax, 1, 50)
        plot_segment_edge(g, 409801399, 29166269, ax, 50, 50)
        plot_segment_edge(g, 29166269, 8811408, ax, 50, 30)
        plot_segment_edge(g, 8811408, 8811405, ax, 30, 30)
        plot_segment_edge(g, 8811405, 1262229633, ax, 30, 1)


class FrameSwitch:
    def __init__(self, g, ax, ax_settings, times=None):
        self.i = 0
        self.g = g
        self.ax_settings = ax_settings
        self.ax = ax
        self.times = times

    def plot(self):
        print(self.i)
        self.ax.clear()
        self.ax_settings.apply(self.ax)
        self.ax.axis('off')

        if self.times is not None:
            self.check_bounds()
            print(self.times[self.i])
            segments = self.times[self.i]
            _ = plot_graph_route(self.g, segments, ax=self.ax, show=False, close=False, node_size=1)  # ax2 plot
        else:
            plot_timestamp_test(self.i, self.g, self.ax)
        plt.show()

    def check_bounds(self):
        if self.i < 0:
            self.i = 0
        elif self.i >= len(self.times):
            self.i = len(self.times) - 1

    def next(self, event):
        self.i = self.i + 1
        self.plot()

    def prev(self, event):
        self.i = self.i - 1
        self.plot()


def twin_axes(g):
    f, ax_map = plt.subplots()
    _, ax_map = ox.plot_graph(g, ax=ax_map, node_size=0, show=False)
    ax_density = ax_map.twinx()
    ax_density.axis('off')
    ax_map_settings = Ax_settings(ylim=ax_map.get_ylim(), aspect=ax_map.get_aspect())
    ax_map_settings.apply(ax_density)
    return f, ax_density, ax_map_settings


def with_buttons():
    g = get_route_network()
    times = pd.read_pickle("../data/times.pickle")
    # times = None

    # twin axes
    ax_density, ax_map_settings = twin_axes(g)

    # add buttons
    callback = FrameSwitch(g, ax_density, ax_map_settings, times)

    axprev = plt.axes([0.7, 0.005, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.005, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)

    plt.show()


def with_slider():
    g = get_route_network()
    times = pd.read_pickle("../data/times.pickle")
    f, ax_density, ax_map_settings = twin_axes(g)

    # get max car count
    max_count = 0
    for time in times:
        for segment in time:
            max_count = max(max_count, segment.vehicle_count)
    print('max', max_count)

    # add slider
    plt.subplots_adjust(bottom=0.1)
    time_slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])
    time_slider = Slider(ax=time_slider_ax, label='Time [s]', valmin=0, valmax=len(times) - 1, valstep=1)

    def update(val):
        print(val)
        start = datetime.now()
        ax_density.clear()
        ax_map_settings.apply(ax_density)
        ax_density.axis('off')

        segments = times[val]
        _ = plot_graph_route(g, segments, ax=ax_density, show=False, node_size=1, max_count=max_count)
        f.canvas.draw_idle()
        finish = datetime.now()
        print(finish - start)

    time_slider.on_changed(update)

    plt.show()


if __name__ == "__main__":
    with_slider()
