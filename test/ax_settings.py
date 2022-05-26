class Ax_settings:
    def __init__(self, ylim, aspect):
        self.ylim = ylim
        self.aspect = aspect

    def apply(self, ax):
        ax.set_ylim(self.ylim)
        ax.set_aspect(self.aspect)
