# Historic population dynamics in Victoria, Australia in the late 19th century


<p align="center">
  <img src="/Images/map-victoria-goldfields.gif" />
  <figcaption>Visualisation of settlements and goldmines.</figcaption>
</p>

## Contributors:

* Isha Bansod
* Aron Golombek
* Marcel van de Lagemaat
* Eva Lampret
* Elizabeth Law 

## Project description
The aim of this project will be to see if we can explain the population dynamics and the growth of large cities in the state of Victoria by examining the discovery of goldmines and corresponding movement of people in this time.

## Requirements
* Python 3.9+
* mesa
* mesa-geo
* pandas
* numpy
* random
* itertools
* matplotlib
* SALib

## Guide
To run the model, first clone the repository to your local machine. Then from the main folder run the command 'mesa runserver'. You will be asked to choose between the base model, which shows the population density, or the information spreading visualization. Type either M or I to see either model respectively. 


## Repository structure


| File Name           | Description                                                                                                                                                                                          |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|Data (Directory)| Contains all logged data for experiments run with the model.|
|Images (Directory)| Contains all plot and visualisations relevant for the project|
|Legacy (Directory)| Contains functions no longer in use. This includes drafting spaces and functions that have been revised.|
|Modelstates (Directory)| Contains files for the starting states of the model, as well as when to add newly discovered mines. |
|Shapefiles (Directory)| Contains shapefiles used during the project for the map visualization. | 
|agents.py | Python file that contains the extension for the mesa geo GeoAgent class. | 
|experiment.py | Can be run with 'experiment.py filename iters', where it saves all data to data_filename.csv for iters number of steps. | 
|model.py | Python file that contains the extension for the mesa Model class. | 
|run.py | Python file that uses the server to run the visualization part of the model. |
|sensitivity.py | Python file that contains the function used to run sensitivity analysis | 
|server.py | Python file that creates the server which runs the visualization part of the model. | 
