from flowmapviz.zoom import plot_graph_with_zoom
from matplotlib import pyplot as plt

'''
    This file is taken from repository FlowMapVideo (https://github.com/It4innovations/FlowMapVideo)
'''


class Ax_settings:
    def __init__(self, ylim, aspect):
        self.ylim = ylim
        self.aspect = aspect

    def apply(self, ax):
        ax.set_ylim(self.ylim)
        ax.set_aspect(self.aspect)


def twin_axes(g):
    f, ax_map = plt.subplots()
    ax_map = plot_graph_with_zoom(g, ax_map)
    ax_density = ax_map.twinx()
    settings = Ax_settings(ylim=ax_map.get_ylim(), aspect=ax_map.get_aspect())
    settings.apply(ax_density)
    ax_density.axis('off')
    return f, ax_density, ax_map
