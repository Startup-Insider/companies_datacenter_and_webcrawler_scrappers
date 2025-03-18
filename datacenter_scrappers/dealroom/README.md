# How to run startup_map_berlin.py
## install the requirements.txt
## Running the file
It will create a csv file called startup_map_berlin.csv and iterate over startups in the website, then for every iteration, it will insert new rows to the csv directly.

# Antipattern in this project
deelroom_module.py and startup_map_berlin.py have the same code, but they have been repeated just to change the area parameters.
