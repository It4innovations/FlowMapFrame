# flowmapviz

Flowmapviz is a simple package for traffic flow visualization.
It includes functionality for rendering a single frame of a traffic flow map, that can be used for video rendering.
The color and width of the line is determined by the number of vehicles on the road segment.
The library is based on matplotlib and osmnx.

## Installation

```bash
python pip install https://github.com/It4innovations/FlowMapFrame
```

## Examples
This package is used in [FlowMapVideo](https://github.com/It4innovations/FlowMapFrame)
for rendering videos of traffic flow based on the data from the [Ruth](https://github.com/It4innovations/ruth) simulator.

As example use, you can run a slider interactive visualization to try all configurable parameters.
To run the example, download the **data folder** from this repository and run the following command in the terminal:
```bash
flowmapviz-example ./data/map.graphml ./data/sim_data.pickle
```


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
Loading the preprocessed data from [FlowMapVideo](https://github.com/It4innovations/FlowMapFrame)
```python
import pandas as pd
times_dic = pd.read_pickle("sim_data.pickle")
```
**Rendering the base map:**

```python
from flowmapviz.zoom import plot_graph_with_zoom
import matplotlib.pyplot as plt
            
fig, ax = plt.subplots()
ax_map = plot_graph_with_zoom(g, ax)
```
**Rendering the traffic flow:**

- Min and max density define the range of values for the color scale.
- Min and max width density define the range of values for the width scale.
- Default linewidth is the width of the line when the density is min density.
- Width modifier is the width of the line when the density is max density.
- Road types by zoom is a boolean value that determines whether the road types are filtered by zoom level.
- hidden lines width is the width of the lines that are not "visible" at the current zoom level.
```python
import networkx as nx
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

---

## Zadaní práce:

**Téma**: Vizualizace vývoje dopravního toku v čase.

Student nebo studentka se bude v rámci své práce věnovat vizualizaci vývoje dopravního toku v čase. Informace o dopravě budou získávány z dopravního simulátoru, který pro daný časový interval, a tak zvanou origin-destination matici, provede simulaci průběhu jednotlivých vozidel na mapě. Pohyby jednotlivých vozidel jsou v pravidelných intervalech zaznamenávány. Cílem práce je ze záznamu pohybu aut vygenerovat plynulé video zobrazující dopravní tok z dané simulace. Vizualizační nástroj bude umožňovat také nastavení stylu konečné vizualizace. 

Jednotlivé body zadání jsou:
1.	Seznámit se s aktuálním stavem dopravního simulátoru vyvíjeného na IT4Innovations, zejména s formátem záznamu pohybu aut.
2.	Prozkoumat aktuální možnosti vizualizace dopravních toků.
3.	Prozkoumat vhodné knihovny a technologie, provést srovnání a vybrat nejvhodnější kombinaci s ohledem na dostupnost zdrojových kódů. Musí se jednat o open-source knihovny.
4.	Implementovat vizualizační nástroj s možností konfigurace konečné vizualizace.

## Literatura

* https://matplotlib.org/
* https://d3js.org/
* W. Chen, F. Guo and F. -Y. Wang, "A Survey of Traffic Data Visualization," in IEEE Transactions on Intelligent Transportation Systems, vol. 16, no. 6, pp. 2970-2984, Dec. 2015, doi: 10.1109/TITS.2015.2436897.
  * [link](https://ieeexplore.ieee.org/abstract/document/7120975?casa_token=SS_93qCqCkoAAAAA:HoxHGaz1nd4d4u_TCP7qhNqVbFyGSFSGeUl7hip1F0jfK0h17_CniYEfNoPmTdoi5fMxwAkiBnA)
* D. Guo, "Flow Mapping and Multivariate Visualization of Large Spatial Interaction Data," in IEEE Transactions on Visualization and Computer Graphics, vol. 15, no. 6, pp. 1041-1048, Nov.-Dec. 2009, doi: 10.1109/TVCG.2009.143.
