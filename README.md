[//]: # "Designed by Simon Chu"
[//]: # "Wed Oct  7 14:32:09 EDT 2020"
[//]: # "README.md"
[//]: # "File to explain repository hierarchies"

# Feature Interaction Prototype

## Repository Hierarchies
```
├── README.md
├── docs : contains generated documentation
    ├── build
    ├── source
    └── README.md
├── examples : contains example Python scripts
├── code_size.sh : bash script that recursively check the code size of the project
└── src : contains source code of the project

```
You can switch between the branches to see different release or version of the drone simulator

## Documentation
- [Python Code Style (Google)](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings)
- [Sphinx Napoleon Extension Meta Documentation](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html)
- [Sphinx Napoleon Extension Setup](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/)
- Path Animation [2D](https://www.youtube.com/watch?v=Ercd-Ip5PfQ) [3D](https://www.youtube.com/watch?v=sRYI5egdWLo) [3D unzip password: thankyou]
- MissionApp [Repository](https://bitbucket.org/gamoreno/missionapp)
- Formal STL (Signal Temporal Logic) [Paper](https://arxiv.org/abs/1808.03315)

## How does it work?
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
