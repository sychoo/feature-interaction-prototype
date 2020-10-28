- mask function, pass in list of coordinates[(x_cor, y_cor)] (allow list, deny list)
- get_neighbor_4 function (get a list of map cells of only 4 neighbors)
- speed limit 
- record path for drones (step as the main time line)
[step#: (x_cor, y_cor)]

- formalize data structure for response_data {
    "step"
}

- Animation software given the sequential path for the movement

- test out the Python abstract method in the example folder

- Show path for the movement





- abstract the coordinates to coordinates class

- Algorithm contains all necessary algorithms

- !!! fix the run function for the flight.py so that it will handle the flight path of the initial step

- ~!~ Exciting! Parser that parses the STL formula

- tedious task
    - !!! convert all coordinates to the Coords object
    - use the algorithm class (instead of write one's own) to calculate robustness values

- ~!~ fly using waitpoints instead of mathemtical equations

- ~!~ ability to set the speed for each drones

- signal estmator should be put in the ego drone

- !!connect STL to signal estimator

- Incorporate the concept of Radar

- Standardaize response data nad signal element

- Continuation Integration haha probably just run the unit test

- Documentation Standard: Napoleon Sphinx extension: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/

https://www.sphinx-doc.org/en/master/usage/quickstart.html

https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings

- convert the docs to rst (reStructured Text)
- sphinx-apidoc -f -o <output-directory> <project-directory> 

- sphinx-build -b html sourcedir builddir

- quickstart: https://pythonhosted.org/an_example_pypi_project/sphinx.html





- Q and A: can't import numpy in documentation Sphinx

https://stackoverflow.com/questions/15889621/sphinx-how-to-exclude-imports-in-automodule


sphinx-apidoc -f -o docs/source .
- command "make install"
- things changed: system path
- add modules in index.rst (like this https://www.youtube.com/watch?v=b4iFyrLQQh4&t=105s)

- gitignore file

- [X] Finished


# To Do For Research Meeting Tomorrow:

- [X] Get Distance_To_Enemy_Drone to work

- Robustness score evaluation during runtime

- implement signal estimator in the execution process, give feedbacks during runtime like
    - "Violation of R1"
    - "Violation of R2"
    - "Violation of Both Features"

- make the signal estimator generate certain duration of signal based on the range G\[begin, end\]() STL Expression 
    - Signal_Estimator(STL_Expr()) # grab the "begin" and "end" attribute from the Global attribute

- message board, get message from shared_flight_data -> ATC_Flight_Data -> "message" key -> message to display during the flight path visualization
    - "Violation of R1"
    - "Violation of R2"
    - "Violation of Both Features"

# Maybe Future Work

- STL Compiler - Based on [Metrics for Signal Temporal Logic Formulae](https://arxiv.org/abs/1808.03315)