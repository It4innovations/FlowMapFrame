# flowmapviz

flowmapviz is a simple package for traffic flow visualization that was created as part of a bachelor's thesis.
It includes functionality for rendering a single frame of a traffic flow map, that can be used for video rendering.
This functionality is based on the matplotlib and osmnx packages.

The traffic map is rendered as a network graph where the color and width of edges are determined by the number of vehicles on the road segment.

flowmapviz is mainly used in [FlowMapVideo](https://github.com/It4innovations/FlowMapVideo)
for rendering videos of traffic flow based on the data from the [Ruth](https://github.com/It4innovations/ruth) simulator.

## Installation

```bash
python pip install https://github.com/It4innovations/FlowMapFrame
```

## Examples
As an example, you can run an interactive slider visualization to try the configurable parameters.
To run the example, download input data from [Zenodo](https://doi.org/10.5281/zenodo.7843650) and run the following command in the terminal:
```bash
flowmapviz-example map.graphml sim_data.pickle
```
<p align="center">
<img src="https://github.com/It4innovations/FlowMapFrame/blob/main/docs/example.gif" height="400"/>
</p>

## Step-by-step guide
The following code shows how to use the package to render a single frame of a traffic flow map.

Importing the package:
```python
import flowmapviz
```
Loading graph representing the map:
```python
import osmnx as ox
g = ox.load_graphml("map.graphml")
```
Loading the preprocessed data saved from [FlowMapVideo](https://github.com/It4innovations/FlowMapVideo):
```python
import pandas as pd
times_dic = pd.read_pickle("sim_data.pickle")
```
**Rendering the base map:**

```python
from flowmapviz.zoom import plot_graph_with_zoom
import matplotlib.pyplot as plt
            
fig, ax = plt.subplots()
ax = plot_graph_with_zoom(g, ax)
```
**Rendering the traffic flow:**

- Min and max density define the range of values for the color scale.
- Min and max width density define the range of values for the width scale.
- Default linewidth is the width of the line when the density is min density.
- Width modifier is the width of the line when the density is max width density.
- Road types by zoom is a boolean value that determines whether the road types are filtered by zoom level.
- Hidden lines width is the width of the lines that are not "visible" at the current zoom level.
```python
from flowmapviz.plot import plot_routes, WidthStyle
import matplotlib.pyplot as plt

one_frame_data =  list(times_dic.items())[0]
nodes_from = [s['node_from'] for s in one_frame_data]
nodes_to = [s['node_to'] for s in one_frame_data]
densities = [s['counts'] for s in one_frame_data]

plot_routes(g, ax, nodes_from, nodes_to, densities,
            min_density = 1, max_density = 10,
            min_width_density = 10, max_width_density = 50,
            default_linewidth = 3, width_modifier = 1,
            width_style = WidthStyle.BOXED,
            round_edges = True,
            roadtypes_by_zoom = False, hidden_lines_width = 1,
            plot = True)

plt.show()
```
