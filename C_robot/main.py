import random, sys

PathwayChar = ' '
PlayerChar = '@'
RobotChar = 'R'
DeadRobotChar = 'X'
WallTexture = '⫶⫶'

MapWidth = 40
MapHeight = 20
Total_Robots = 10
TeleportDevice = 2
DeadRobot = 2
Total_Walls = 100

def main():
    print('HUNGRY ROBOTS!')
    input('Press Enter to start playing...')
    maze = generate_maze()
    display_map(maze)

    if Total_Robots == 0:
      print('All the robots have crashed into each other and you lived to tell the tale! Good job!')
      sys.exit()

#generate the game map
def generate_maze():
    maze = [[PathwayChar] * MapWidth for _ in range(MapHeight)]

    #Add edge walls
    for x in range(MapWidth):
        maze[0][x] = WallTexture
        maze[MapHeight - 1][x] = WallTexture
    for y in range(MapHeight):
        maze[y][0] = WallTexture
        maze[y][MapWidth-1] = WallTexture

    #Add random walls in the pathway on every row
    for _ in range(Total_Walls):
        x, y = random.randint(1, MapWidth - 2), random.randint(1, MapHeight - 2)
        maze[y][x] = WallTexture

    return maze

#print out the map
def display_map(maze):
    for row in maze:
        print(''.join(row))

if __name__ == "__main__":
    main()
