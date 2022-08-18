import pprint

import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.widgets import Slider
from datetime import datetime

from app_io import load_input
from ax_settings import twin_axes

from app_collection_plot import plot_routes
from app_base_graph import get_route_network_small, get_route_network_simple, get_route_network
from app_plot import plot_segments
from app_plot_cars import plot_cars


def data():
    d = pd.read_parquet("../data/data-global-view-20210616_7-10/gv_202106016_7_10.parquet", engine="fastparquet")
    print(d)


def create_sliders(max_time, max_width):
    plt.subplots_adjust(bottom=0.1)
    time_slider_ax = plt.axes([0.2, 0.06, 0.65, 0.03])
    width_slider_ax = plt.axes([0.2, 0.03, 0.65, 0.03])
    time_slider = Slider(ax=time_slider_ax, label='Time [s]', valmin=0, valmax=max_time, valstep=1)
    width_slider = Slider(ax=width_slider_ax, label='Width', valmin=2, valmax=max_width, valstep=1, valinit=10)
    return time_slider, width_slider


def with_slider():

    g = get_route_network_simple()

    times = pd.read_pickle("../data/times.pickle")
    f, ax_density, ax_map_settings = twin_axes(g)

    # get max car count
    max_count = 0
    for time in times:
        for segment in time:
            max_count = max(max_count, segment.vehicle_count)

    # add slider
    time_slider, width_slider = create_sliders(len(times) - 1, 70)
    is_with_cars = False
    width_style = 1

    def on_press(event):
        nonlocal is_with_cars
        nonlocal width_style

        if event.key == 'right':
            time_slider.set_val(time_slider.val + 1)
        elif event.key == 'left':
            time_slider.set_val(time_slider.val - 1)
        elif event.key == 'up':
            width_slider.set_val(width_slider.val + 1)
        elif event.key == 'down':
            width_slider.set_val(width_slider.val - 1)
        elif event.key == 'c':
            is_with_cars = not is_with_cars
            update()
        elif event.key.isnumeric():
            width_style = int(event.key) % 4
            update()

    f.canvas.mpl_connect('key_press_event', on_press)

    def width_update(val):
        if time_slider.val > -1:
            update()

    def update(val=None):
        if val is None:
            val = time_slider.val

        start = datetime.now()
        # clear ax and copy base map
        ax_density.clear()

        ax_map_settings.apply(ax_density)
        ax_density.axis('off')

        segments = times[val]

        # MAIN PLOT FUNCTION
        width = width_slider.val
        _ = plot_routes(g, segments, ax=ax_density, max_count=max_count, width_modifier=width, width_style=width_style)

        # plot cars
        if is_with_cars:
            plot_cars(g, segments, ax_density)

        f.canvas.draw_idle()

        finish = datetime.now()
        print(finish - start)

    time_slider.on_changed(update)
    width_slider.on_changed(width_update)
    plt.show()


if __name__ == "__main__":
    with_slider()
    pass

