from matplotlib import pyplot as plt
import osmnx as ox


class Ax_settings:
    def __init__(self, ylim, aspect):
        self.ylim = ylim
        self.aspect = aspect

    def apply(self, ax):
        ax.set_ylim(self.ylim)
        ax.set_aspect(self.aspect)


def twin_axes(g):
    f, ax_map = plt.subplots()
    _, ax_map = ox.plot_graph(g, ax=ax_map, node_size=0, show=False)
    ax_density = ax_map.twinx()
    ax_density.axis('off')
    ax_map_settings = Ax_settings(ylim=ax_map.get_ylim(), aspect=ax_map.get_aspect())
    ax_map_settings.apply(ax_density)
    return f, ax_density, ax_map_settings