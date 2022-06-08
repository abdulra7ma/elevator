# Elevator

## Table of contents
- [Elevator](#elevator)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
  - [Simulation](#simulation)
  - [Run](#run)
  - [Notes](#notes)

## Setup
1. create venv and activate it
```
python -m venv venv
source venv/bin/activate
```
2. install needed packages from requirements.txt
```
pip install -r requirements.txt
```

## Simulation
1. generate a random number of floors between 5 and 20
2. generate a random number of passenger for each floor between 1 and 10
    * passenger can not have the same floor arrival as the floor that was generated on.
3. Elevator always start from bottom to up
4. if the elevator become empty than we check the nearest floor that has passengers and determine the direction of the elevator according to the  majority of passengers the want to go in  each direction
5. Elevator runs until finishing all the passengers on each floor

## Run
1. program starts by showing all the passengers in each floor
   ```
    ******************************
    PASSENGERS IN EACH FLOOR 
    ******************************

    F1  :  🕵️ | 🕵️ | 🕵️ | 🕵️ | 🕵️ | 🕵️ | 🕵️ | 🕵️ | 
    F2  :  🕵️ | 🕵️ | 🕵️ | 
    F3  :  🕵️ | 🕵️ | 🕵️ | 🕵️ | 🕵️ | 🕵️ | 
    F4  :  🕵️ | 🕵️ | 🕵️ | 🕵️ | 🕵️ | 
   ```
2. According to the  Direction of the elevator it shows the common message
```
******************************
 Elevator is moving Up 
******************************
```
**or**

```
******************************
 Elevator is moving Down 
******************************
```

3. each step it shows the current floor and another two floors previous and next, Respectively.
   1. ⬅️ -> points to current floor
   2. 🔼 or 🔽 determine wheather the passenger want to go up or down
   3. passengers to the right of the previous and next floors are the one waiting to take the elevator

```
...
Direction: ⬆️  Floor: 2
|----------------------------------------------
|F1|                            | 🕵️ 6-> 3  🔼  🕵️ 7-> 4  🔼  🕵️ 8-> 3  🔼  
|----------------------------------------------
|F2|  🕵️ P1 -> 4  🕵️ P3 -> 4  🕵️ P4 -> 4  🕵️ P5 -> 3  ⬅️                           | 🕵️ 9-> 3  🔼  🕵️ 10-> 3  🔼  🕵️ 11-> 1  🔽  
|----------------------------------------------
|F3|                            | 🕵️ 12-> 1  🔽  🕵️ 13-> 4  🔼  🕵️ 15-> 1  🔽  
|----------------------------------------------
...
```

## Notes
   ** The progrom UI was not that fancy as We had a limited time