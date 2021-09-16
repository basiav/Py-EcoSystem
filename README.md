# Py-EcoSystem
### author: Barbara Wojtarowicz, September 2021

Program for creating simple ecosystem simulations using python threading library. Each animal's behaviour is handled by a different thread. The main thread supervises the animal threads and communicates with them using threading.Event objects. Shared memory multithreading safety is supplied with simple threading.Lock objects.


<img src="https://github.com/basiav/Py-EcoSystem/blob/main/utils/anim_1.png"/>

### Task Description
<img src="https://github.com/basiav/Py-EcoSystem/blob/main/utils/task.png" width="600"/>

### Running the program
Run the program with app/main.py.

### Start Menu
<img src="https://github.com/basiav/Py-EcoSystem/blob/main/utils/start_menu.png" width="600"/>

* start a sample simulation immediately with default parameters
* enter the settings menu to chose your preferences

### Settings Menu
<img src="https://github.com/basiav/Py-EcoSystem/blob/main/utils/settings_menu.png" width="600"/>
Use sliders to chose your parameter preferences:

* 'N' - size of the map field,
* 'Rabbits' and 'Wolves' - no. of rabbits and no. of wolves,
* 'Rabbit Reproduction Chances' and 'Wolf Reproduction Chances' - parameter for better managing possible overpopulation issue.

Use buttons for:
* getting back to start menu,
* moving further to map settings menu,
* saving current settings, including map preferences, and running the simulation.

### Map Menu
<img src="https://github.com/basiav/Py-EcoSystem/blob/main/utils/map_generation_1.png" width="600"/>

* Use the slider to chose how many 'Fence Islands' (labyrinth elements) you'd like your maze to contain - choose anything from 0 up to 4. The maze will be placed on the map, which size you've picked in the settings menu.
* Click on the map field to generate the maze randomly and display its' preview. Every time you click on the map, a new maze containing the number of elements you've chosen will be generated and displayed.
* Save your settings and get back to setting menu, from where you can start the simulation!

<p float="center">
<img src="https://github.com/basiav/Py-EcoSystem/blob/main/utils/map_generation_2.png" width="450"/> <img src="https://github.com/basiav/Py-EcoSystem/blob/main/utils/map_generation_3.png" width="450"/>
</p>


### Pause, Resume or Quit Simulation
<img src="https://github.com/basiav/Py-EcoSystem/blob/main/utils/anim_2.png" width="600"/>

* Pause the simulation using the 'Pause' button in the right bottom corner.
  - Once the simulation is paused, the 'Pause' button will become replaced with the 'Resume' button.
  - If the simulation had started just started and you cannot observe new animal statistic plots yet, it make take a few seconds for the program to catch up with the plot and pausing issues. That's because at the very beginning, each animal needs to get spawned and only after can the program react to pausing, resuming or quitting.
 * Resume the simulation using the 'Resume' button, once stopped.
 * Quit the simulation using the 'Quit and Return to Start Menu' button. Only from there can you quit the whole program.

<img src="https://github.com/basiav/Py-EcoSystem/blob/main/utils/anim_3.png" width="600"/>
