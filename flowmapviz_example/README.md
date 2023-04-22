# Flowmapviz example with slider

Download the input data from [Zenodo](https://doi.org/10.5281/zenodo.7843650). Then run the following command in the terminal:
```bash
flowmapviz-example map.graphml sim_data.pickle
```
### Navigation Keyboard Shortcuts:

* `left arrow`/`right arrow` to change time
* `up arrow`/`down arrow` to change width modifier
* change width style:
  * `0` no width modification
  * `1` style BOXED
  * `2` style CALLIGRAPHY
  * `3` style EQUIDISTANT
* `r` - toggle round edges
* `z` - toggle road types filter by zoom
* `v` - save next 20 frames as GIF

### Useful Matplotlib Keyboard Shortcuts:
* `s` - save the current figure as png
* `h` - home/reset
* `f` - toggle fullscreen