from config import *
import random
import sys
import numpy as np

#initialize the global variable
PathwayChar = ' '
WallTexture = 'B'
PlayerChar = '@'
DeadRobotChar = 'X'
RobotChar = 'R'

DeadRobot = DEAD_ROBOT
Total_Robots = TOTAL_ROBOT
Total_Walls = 100
MapWidth = 40
MapHeight = 20
TeleportDevices = 2

def generate_map():
    maze = [] # the generated objects will be stored in this list

    # Insert empty space for pathway
    for _ in range(MAP_HEIGHT):
        empty = [PathwayChar] * MAP_WIDTH
        maze.append(empty)

    # Add border walls
    for x in range(MAP_WIDTH):
        maze[0][x] = WallTexture # top border wall
        maze[MAP_HEIGHT - 1][x] = WallTexture # bottom border wall
    for y in range(MAP_HEIGHT):
        maze[y][0] = WallTexture # left border wall
        maze[y][MAP_WIDTH-1] = WallTexture # right border wall

    # Insert random walls in the map
    for _ in range(Total_Walls):
        x, y = randomXY(maze,[])
        maze[y][x] = WallTexture

    return maze

# function to find a random empty space
def randomXY(game_map, robotLocation_list):
    while 1:
        randomX = random.randint(1, MapWidth - 2) 
        randomY = random.randint(1, MapHeight - 2)
        if no_object(randomX, randomY, game_map, robotLocation_list):
            break

    return (randomX, randomY)

# function to make sure that the current XY value in the random space is really empty
def no_object(randomX, randomY, game_map, robotLocation_list):
    is_pathway = game_map[randomY][randomX] == PathwayChar # is an empty space and not a wall
    not_in_robots = (randomX, randomY) not in robotLocation_list # doesn't blocked by robot
    return is_pathway and not_in_robots

# function to insert the enemy robots in random empty space
def insertRobot(game_map):
    robotLocation_list = [] # the generated robot coordinates will be stored in this list
    for i in range(Total_Robots):
        x, y = randomXY(game_map, robotLocation_list)
        game_map[y][x] = 'R'
        robotLocation_list.append((x, y)) # append every new XY coordinate is generated

    return robotLocation_list


game_map = generate_map()
robot_coordinates = insertRobot(game_map) # call the robot inserter function
(tx, ty) = randomXY(game_map, robot_coordinates) # randomize the player starting location
playerLocation = [0, 1]
playerLocation[0] = tx
playerLocation[1] = ty
game_map[playerLocation[1]][playerLocation[0]] = 'P'

# for i in range(MAP_HEIGHT):
# 	for j in range(MAP_WIDTH):
# 		print(game_map[i][j], end='')
# 	print()
