- Supported boundaries, obstacles and enemy drones

1. encode flight pattern
  - scale it up from smaller maps?
  - use some kind of vector space? Mathematical notation?
- how to encode the flight pattern
- how to deal with the situation with the boundary is exceeded

Solution
- for encoding, use the initial position as the origin (0, 0), and
  explore the neighboring cells that best fits the flight pattern
specification (
- constraints - make the width of the fly 8
  (https://en.wikipedia.org/wiki/Lemniscate) the length of the map

when exceeding the boundary of the map, simply ignore the cell outside
of the boundary without writing it


Documentation
- Internal Map
  - Map that is represented internally
  - 2-D array of MapCell objects (x_cor, y_cor, )

- Output Map
  - Map that is fed in to the seaborn heatmap

!!!
- explore the neighbors, find the best fit (vertically) coordinates to the graph, no turning back
- output execution sequence, 
- take the right side if both are the same


Issue:
!!! - when using attribute it has index out of range error
- how to handle flying outside of the bound
- allow boundaries to be set within the map (using coordinates)
