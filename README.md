# flowmapviz

* [Roadmap](../../wikis/Roadmap)

## Použití
Pro spuštění je potřeba GRAPHML soubor s mapou vykreslované oblasti a soubor s počtem aut v jednotlivých časech na segmentech.
Viz *segments* níže.

**Zavolání funkce pro vykreslení snímku:**

```python
from flowmapviz.plot import plot_routes
```
* `node_from` a `node_to` (osmnx id definující segment)
* `densities`, definující počet aut u těchto nodů
* `min/max_density`: rozmezí určující barvu segmentu - od žluté (min_density) po červenou (max_density)
* `min_width_density`: počet aut, při kterém se začně zvyšovat šířka vykreslené cesty
* `max_width_density`: počet aut, při kterém nastane maximální šířka cesty
* `width_modifier`: maximální šířka cesty v bodech (pro šířku v lat stupních či v metrech použíjte převod)
* `width_style` = enum
  * BOXED - zubatý okraj (šířka v pixelech) - pro plynulost třeba zapnout round_edges
  * CALLIGRAPHY - kaligrafický okraj
  * EQUIDISTANT - okraj počítaný pomocí equidistanty
* round_edges: proměnná určující, zda se na ohraj segmentů mají vykreslit kruhy pro plynulejší přechod
* `plot`: pokud nastaveno na False, pak dojde pouze ke generování kolekcí čar a polygonů, ne k jejich vykreslení
(tvary lze do ax přidat později pomocí mathplotlib.add_collection)
```python
def plot_routes(g: nx.MultiDiGraph,
                ax: Axes,
                nodes_from: list[int],
                nodes_to: list[int],
                densities: list[int] | list[list[int]],
                min_density: int = 1, max_density: int = 10,
                min_width_density: int = 10, max_width_density: int = 50,
                width_modifier: float = 1,
                width_style: WidthStyle = WidthStyle.BOXED,
                round_edges: bool = True,
                plot: bool = True)
```
**Funkce pro převod jednotek:**  
Vrací dvojici prvků, kdy první vyjadřuje poměr k ose y a druhá k ose x.
V implementaci funkce plot_routes jsem zvolila převod dle osy x.
```python
from flowmapviz.plot import map_distance_to_point_units
```

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
