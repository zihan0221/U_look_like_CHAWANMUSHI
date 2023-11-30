import random
import sys

#initialize the global variable
PathwayChar = ' '
WallTexture = ':'
PlayerChar = '@'
DeadRobotChar = 'X'
RobotChar = 'R'

DeadRobot = 2
Total_Robots = 10
Total_Walls = 100
MapWidth = 40
MapHeight = 20
TeleportDevices = 2


def main():
    print('HUNGRY ROBOTS!')
    print('--snip--')
    game_map = generate_map() # call the map generator function
    robot_coordinates = insertRobot(game_map) # call the robot inserter function
    playerLocation = randomXY(game_map, robot_coordinates) # randomize the player starting location

    # stay on a loop until player is killed or all robots are destroyed
    while 1:
        display_map(game_map, robot_coordinates, playerLocation) # print the generated map
        playerLocation = key_movement(game_map, robot_coordinates, playerLocation) # ask for player moves
        
        # add a move robot function here (change as much as you like)
        
        # if player wins and all robots destroyed (change as much as you like)
        if not robot_coordinates:
          print('All the robots have crashed into each other and you lived to tell the tale! Good job!')
          sys.exit()

        # if a robot caught the player (change as much as you like)
        for x, y in robot_coordinates:
            if(x,y) == playerLocation:
                print('You have been caught by a robot!')
                sys.exit()


# function to move the player location
def key_movement(game_map, robot_coordinates, playerLocation):
    player_x, player_y = playerLocation
    global TeleportDevices

    # This is list of the movement keys
    # Q = go up left diagonally
    # W = go up
    # E = go up right diagonally
    # D = go right
    # C = go down right diagonally
    # X = go down
    # Z = go down left diagonally
    # A = go left
    # S = stop or no move
    movements = {
        'Q': (-1, -1), 'W': (0, -1), 'E': (1, -1),
        'D': (1, 0), 'C': (1, 1), 'X': (0, 1),
        'Z': (-1, 1), 'A': (-1, 0), 'S': (0, 0)
    }

    while True:
        print('(T)teleports remaining:{}'.format(TeleportDevices))
        print('                    (Q) (W) (E)')
        print('                    (A) (S) (D)')
        print('Enter move or Quit: (Z) (X) (C)')
        print('--snip--')
        key_input = input(' ').upper()

        # if player inputs a teleport key
        if key_input == 'T':
            if TeleportDevices > 0:
                TeleportDevices -= 1
                print("Teleport succeeded")
                print('--snip--')
                return randomXY(game_map, robot_coordinates)
            else:
                print('Your teleportation device is out of energy')
                print('--snip--')
                return playerLocation

        # if player wants to quit
        elif key_input == 'QUIT':
            print('Thanks for playing!')
            sys.exit()
        
        # make sure that the input key is valid
        elif key_input in movements:
            move = movements[key_input]
            new_x, new_y = player_x + move[0], player_y + move[1]

            # if the input is valid, make sure the input key movement is not block by any other object
            if no_object(new_x, new_y, game_map, robot_coordinates):
                return new_x, new_y
            else:
                print("Move blocked by another object. Try another direction.")
                print('--snip--')

        # If the input key is invalid, it will keep on looping until the valid key is inputted
        else:
            print("Invalid input, please try another key")
            print('--snip--')


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


# function to generate the game map
def generate_map():
    maze = [] # the generated objects will be stored in this list

    # Insert empty space for pathway
    for _ in range(MapHeight):
        empty = [PathwayChar] * MapWidth
        maze.append(empty)

    # Add border walls
    for x in range(MapWidth):
        maze[0][x] = WallTexture # top border wall
        maze[MapHeight - 1][x] = WallTexture # bottom border wall
    for y in range(MapHeight):
        maze[y][0] = WallTexture # left border wall
        maze[y][MapWidth-1] = WallTexture # right border wall

    # Insert random walls in the map
    for _ in range(Total_Walls):
        x, y = randomXY(maze,[])
        maze[y][x] = WallTexture

    # insert dead robot in the map
    for _ in range(DeadRobot):
        x, y = randomXY(maze,[])
        maze[y][x] = DeadRobotChar

    return maze


# function to print out the generated map
def display_map(game_map, robot_coordinates, playerLocation):
    for y, row in enumerate(game_map):
        for x, char in enumerate(row):
            if (x, y) == playerLocation:
                print(PlayerChar, end='') # print the player location
            elif (x, y) in robot_coordinates:
                print(RobotChar, end='') # print the robot location
            else:
                print(char, end='') # print the other objects such as wall or empty space
        print() # print a new line for printing the new row


# function to insert the enemy robots in random empty space
def insertRobot(game_map):
    robotLocation_list = [] # the generated robot coordinates will be stored in this list
    for i in range(Total_Robots):
        x, y = randomXY(game_map, robotLocation_list)
        robotLocation_list.append((x, y)) # append every new XY coordinate is generated

    return robotLocation_list


# function to move the robot
def robot_movement():
    # insert the robot movement function here (change as much as you like)
    robotMove = []


if __name__ == "__main__":
    main()
