from PIL import Image, ImageDraw
import math as m
import random
import numpy as np
import sys


from datetime import datetime
import os

version = 5

sys.setrecursionlimit(15000)
print("MaxRecursion= ", sys.getrecursionlimit())

if version == 1:
    right = 2
    left = 1
    down = 5 
    up = 5
    offset = 1
    scale = 2
    umfang = 360 #standard 360 v1
    hoehe = 180 #standard 180 v1
    basis = 5 #adds a base without labyrinth
    rand = 1 #adds a top without labyrinth
elif version == 2:
    right = 2
    left = 1
    down = 5 
    up = 5
    offset = 1
    scale = 2
    umfang = 270 #standard 360 v1
    hoehe = 180 #standard 180 v1
    basis = 5 #adds a base without labyrinth
    rand = 1 #adds a top without labyrinth
elif version == 3:
    right = 2
    left = 1
    down = 5 
    up = 5
    offset = 1
    scale = 2
    umfang = 302 #standard 328 v1
    hoehe = 160 #standard 150 v1
    basis = 7 #adds a base without labyrinth
    rand = 2 #adds a top without labyrinth
elif version == 4:
    right = 2
    left = 1
    down = 5 
    up = 5
    offset = 1
    scale = 2
    umfang = 330 #standard 328 v1 max= 554
    hoehe = 180 #standard 150 v1 max= 180
    basis = 1 #adds a base without labyrinth
    rand = 1 #adds a top without labyrinth
elif version == 5:
    name = "Uka"
    right = 40
    left = 40
    down = 1
    up = 1
    offset = 1
    scale = 4
    umfang = int(380/scale) #standard 328 v1
    hoehe = int(180/scale) #standard 150 v1
    basis = 2 #adds a base without labyrinth
    rand = 2 #adds a top without labyrinth

if rand + basis >= hoehe:
    print("Rand und Basis zu groß")

if umfang%2 != 0:
    print("Umfang muss gerade sein!")

def createArray(width, height):
    # creates List of list for the maze
    maze = np.ones((height, width), dtype=np.int32 )
    return maze

def fillMaze(maze, start, right = 1, left = 1, down = 20, up = 20):
    #fills a given array(maze)(list of list) with a labyrinth. Starts at start. Returns exit. 
    
    # stack of the last visited points
    lastPoint = []

    lastPoint.append([start[1], start[0]])
    
    #print(lastPoint)
    
    #height = len(maze)
    width = len(maze[0])


    x = start[0]
    y = start[1]

    #loops = 0

    #init cooordinates for exit
    exit = []
    exit.append([x , y])
   
    options = checkNeighbours(maze, start, right, left, down, up)
    #print(options)

    #as long as we have unvisited cells
    while lastPoint:

        #set current point as visited
        maze[y][x] = 1

        #take last point from stack as current point
        x = lastPoint[len(lastPoint)-1][1]        
        y = lastPoint[len(lastPoint)-1][0] 
       
        #remember lowest lastest point for exit
        if  y >= exit[len(exit)-1][1] and (x,y) not in exit:
            exit.append([x , y])
        
        #check if unvisited cells
        options = checkNeighbours(maze,(x,y))

        #print(options)

        if len(options) > 0:
            
            #choose from options a cell
            cell_chosen = (random.choice(options)) 


            if cell_chosen == "right":
                #remove wall
                maze[y][(width+x+1)%width] = 1
                #print('right')
                #new point on the stack
                lastPoint.append([y,(width+x+2)%width])

            elif cell_chosen == "left":
                #remove wall
                maze[y][(width+x-1)%width]  = 1 
                #print('left')
                #new point on the stack
                lastPoint.append([y,(width+x-2)%width])

            elif cell_chosen == "down":
                #remove wall
                maze[y+1][x] = 1
                #print('down')
                #new point on the stack
                lastPoint.append([y+2,x])

            elif cell_chosen == "up":
                #remove wall
                maze[y-1][x] = 1
                #print('up')
                #new point on the stack
                lastPoint.append([y-2,x])
        
        else:
            #if no unvisited neighbours remove the point from the list
            lastPoint.pop()
         
    
    #print(maze)
    #print(exit)

    exit = exit.pop()
    #print("exit:", exit)
    return exit, maze
           
def checkNeighbours(maze, point, right = 1, left = 1, down = 1, up = 1):
    #checks if unvisited cells behind the walls of the given point
    
    height = len(maze)
    width = len(maze[0])

    x = point[0]
    y = point[1]

   # print('x= ' + str(x))
    #print('y= ' + str(y))
    
    options = []
    
    # can pass the rigt and left border
    if (maze[y][loop(x+2,width)] == -1):
        for i in range(right):
            options.append('right')
    
    # can pass the rigt and left border    
    if(maze[y][loop(x-2,width)]  == -1 ):
        for i in range(left):
            options.append('left')
        #options.extend(['left' for i in range(factor[1])])
    
    #only if point is in the grid no passing to top or bottom
    if y+2 < height-1:
        if(maze[y+2][x]  == -1):
            for i in range(down):
                options.append('down') 
    #only if point is in the grid no passing to top or bottom
    if y-2 > 0:   
        if(maze[y-2][x] == -1):
            for i in range(up):
                options.append('up')
    
    return options

def markStart(maze, start):
    #removes the wall over the starting point for entrance
    x = start[0]
    y = start[1]
    for i in range( 0, y, 1):
        maze[i][x] = 1

    return maze

def markExit(maze, start):
    #removes the wall over the starting point for entrance
    
    height = len(maze)
    
    x = start[0]
    y = start[1]

    for i in range( y, height, 1):
        maze[i][x] = 1

    return maze

def findStartpoint(maze):
    #finds the first unvisited cell in the given maze 
    
    height = len(maze)
    width = len(maze[0])

    for h in range(height):
        for w in range(width):
            if maze[h][w] == -1:
                start = (w,h)
                return start  

def patternMaze(maze):
    #fills the given array with walls every second line
    
    height = len(maze)
    width = len(maze[0])

    maze[range(0, height, 2)] = 0
    maze[height-1] = 0
    for i in range(1, height, 2):
        for j in range (0, width, 2):
            maze[i][j] = 0


    return maze

def addBase(maze, base):
    #adds a base with given hight of solid walls
    
    height = len(maze)
    width = len(maze[0])

    for i in range(height - base, height):
        for j in range (0, width):
            maze[i][j] = 0

    return maze

def addTop(maze, top):
    #adds a top Ring with given hight
    
    width = len(maze[0])

    for i in range(0, top):
        for j in range (0, width):
            maze[i][j] = 0

    return maze
    
def loop(position, width):
    
    newPosition = (width + position) % width
    
    return newPosition

def toEisenScriptV1(maze):
    #converts a given array in a 120mm diameter and 180mm high EisenScript 

    moveCenter = 30 #defined for the Eisenscript

    height = len(maze)
    width = len(maze[0])

    # datetime object containing current date and time
    now = datetime.now()
    
    #print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d-%m_%H-%M-%S")
    print("date and time =", dt_string)	

    file = open(r"D:\LambyrinthLamp\Test\Lapev1" + dt_string + ".es","w")

    file.write ( '//' + dt_string )

    file.write (''' //--created by billManuel
    start
    ''')

    file.write ('rule start {')

    for h in range(height):
        for w in range(width):
            file.write( '{ rz ' + str(w) + ' x ' + str(moveCenter - (maze[h][w] * 0.35)) + ' z ' + str(-h) + ' s 60 1 1 } box \n')
        
    file.write('}')

    file.close()

def toEisenScriptV2(maze):
    #converts a given array in a 120mm diameter and 180mm high EisenScript 

    height = len(maze)
    width = len(maze[0])

    #how deep the secound layer is
    offset = 0.4

    #turning angle
    angle = 360/width
    #place it from center
    moveCenter = (width/(2*m.pi))/2 - 0.5 #calculate distance to move from center
    # moveCenter = 15 
    # print('moveCenter: ' + str(moveCenter))

    # datetime object containing current date and time
    now = datetime.now()
    
    #print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d-%m_%H-%M-%S")
    print("date and time =", dt_string)	

    file = open(r"D:\LambyrinthLamp\Test\Lapev2" + "_offset" + str(offset) + "_h" + str(height) + "circ" + str(width) + "_" + dt_string + ".es","w")

    file.write ( '//' + dt_string )

    file.write (''' //--created by billManuel
    start
    ''')

    file.write ('rule start {')

    for h in range(height):
        for w in range(width):
            file.write( '{ rz ' + str(w*angle) + ' x ' + str(moveCenter - (maze[h][w] * offset)) + ' z ' + str(-h) + ' s ' + str(moveCenter*2) + ' 1 1 } box \n')
        
    file.write('}')

    file.close()

def toEisenScriptSolid(maze, offset, name):
    #converts a given array in a 120mm diameter and 180mm high EisenScript 

    height = len(maze)
    width = len(maze[0])

    #how deep the secound layer is
    #offset = 0.3

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d-%m_%H-%M-%S")
    #print("date and time =", dt_string)	I'm da biggest Mothafucka


    #turning angle
    angle = 360/width
    #place it from center
    moveCenter = (width/(2*m.pi))/2 - 0.5 #calculate distance to move from center
    # moveCenter = 15 
    # print('moveCenter: ' + str(moveCenter))

    path = r'D:\LambyrinthLamp\Test\\' 
    #print(path)
    
    fileName = "Lampe_" + name + "_offset" + str(offset) + "_h" + str(height) + "circ" + str(width) + "_" + "scale" + str(scale)+ "_" + dt_string +  ".es"
    print(fileName)

    file = open(path + fileName,"w")

    file.write ( '//' + dt_string )

    file.write (''' //--created by billManuel
    start
    ''')

    file.write ('rule start {')

    for h in range(height):
        for w in range(width):
            file.write( '{ rz ' + str(w*angle) + ' x ' + str(moveCenter - (maze[h][w] * offset)) + ' z ' + str(-h) + ' s ' + str(moveCenter*2) + ' 1 1 } box \n')
        
    file.write('}')

    file.close()

def toEisenScriptSlimWalls(maze):
    #converts a given array in a 120mm diameter and 180mm high EisenScript 

    height = len(maze)
    width = len(maze[0])

    nozzle = 1

    #how deep the secound layer is
    offset = 0.3

    #turning angle
    angle = 360/width
    #place it from center
    moveCenter = (width/(m.pi))/2 - (nozzle/2) #calculate distance to move from center
    # moveCenter = 15 
    # print('moveCenter: ' + str(moveCenter))

    # datetime object containing current date and time
    now = datetime.now()
    
    #print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d-%m_%H-%M-%S")
    print("date and time =", dt_string)	

    file = open(r"D:\LambyrinthLamp\Test\Lapev4" + "_offset" + str(offset) + "_h" + str(height) + "circ" + str(width) + "_" + dt_string + ".es","w")

    file.write ( '//' + dt_string )

    file.write (''' //--created by billManuel
    start
    ''')

    file.write ('rule start {')

    for h in range(height):
        for w in range(width):
            file.write( '{ rz ' + str(w*angle) + ' x ' + str(moveCenter - (maze[h][w] * offset)) + ' z ' + str(-h) + ' s ' + str(nozzle) + ' 1 1 } box \n')
        
    file.write('}')

    file.close()

def markAllCellsUnvisited(maze):
    # mark all cells as unvisited (-1)
    maze = maze*-1 
    return maze

def markSolution(maze):
    #make list of lists with size of maze and fill ist with zeroes. Then mark the Path in the new maze and give new maze and maze to recursive solution funktion

    #finds the first unvisited cell in the given maze 
    start = findStartforSolution(maze)
    end = findEndforSolution(maze)
    
    solution = np.zeros((len(maze), len(maze[0])), dtype=np.int32 )

    solution = recursiveSolution(maze, solution, start, end)

   # h, w = start

    #maze[h][w] = 9
   # if isinstance(solution, type(np.zeros((2,3)))):
   #     solution[h][w] = 9

    #h, w = end

    #maze[h][w] = 3
    #if isinstance(solution, type(np.zeros((2,3)))):
    #    solution[h][w] = 3

        
    #print(maze)
    #print(solution)

    return solution

def recursiveSolution(maze, solution, currentPoint, end):
    #searches recursive the solution to deep to use
    
    h, w = currentPoint
    solution[h][w] = 1

    height = len(maze)
    width = len(maze[0])
    

    if currentPoint != end:
        #down
        if  h+1 < height and solution[h + 1][w] == 0  and  maze[h + 1][w] == 1:
            test = recursiveSolution(maze, solution, (h+1, w), end)
            if isinstance(test, np.ndarray):
                return test
        #up
        if h-1 > 0 and solution[h - 1][w] == 0 and maze[h - 1][w] == 1:
            test = recursiveSolution(maze, solution, (h -1, w), end)
            if isinstance(test, np.ndarray):
                return test
        #right
        if solution[h][(width + w + 1)%width] == 0 and maze[h][(width + w + 1)%width] == 1:
            test = recursiveSolution(maze, solution, (h, (width + w + 1)%width), end)
            if isinstance(test, np.ndarray):
                return test
        #left
        if solution[h][(width + w - 1)%width] == 0 and maze[h][(width + w - 1)%width] == 1:
            test = recursiveSolution(maze, solution, (h, (width + w - 1)%width), end)
            if isinstance(test, np.ndarray):
                return test
        #deadend
        else:
            pass

    else:
        #end recursion
        return solution
        
def findStartforSolution(maze):
    #find the start of the maze for the solution
    height = len(maze)
    width = len(maze[0])

    for h in range(height):
        for w in range(width):
            if maze[h][w] == 1:
                start = (h, w)
                #print ("start:", start)
                return start 

def findEndforSolution(maze):
    #find the start of the maze for the solution
    height = len(maze)
    width = len(maze[0])

    for h in range(height-1, 0, -1):
        for w in range(width-1, 0, -1): 
            if maze[h][w] == 1:
                end = (h, w)
                #print ("end: ", end)
                return end
    
def scaleMaze(maze, scale):
    #scales the maze up the given factor
    
    height = len(maze)
    width = len(maze[0])
    
    # creates List of list for the scaled maze
    scaleMaze = np.zeros((height*scale, width*scale), dtype=np.int32 )

    for h in range(height):
        for sh in range((h*scale), (h*scale)+scale):
            for w in range(width):
                for sw in range((w*scale), (w*scale)+scale):
                    scaleMaze[sh][sw] = maze [h][w]

    return scaleMaze




maze = createArray(umfang, hoehe)
maze = patternMaze(maze)
#print(maze)
maze = addBase(maze, basis)
maze = addTop(maze, rand)
#print(maze)
maze = markAllCellsUnvisited(maze)
start = findStartpoint(maze)
#print('start: ' + str(start))
exit, maze = fillMaze(maze, start, right, left, down, up)
maze = markStart(maze,start)
maze = markExit(maze, exit)
#print(maze)
#print(solution)

if version == 1:
    toEisenScriptV1(maze) 
elif version == 2:
    toEisenScriptV2(maze) 
elif version == 3:
    toEisenScriptSolid(maze, 0.3, "v3") 
elif version == 4:
    toEisenScriptSlimWalls(maze) 
elif version == 5:
    solution = markSolution(maze)
    #maze = maze+solution
    solutionScaled = scaleMaze(solution, scale - 1)
    maze = scaleMaze(maze, scale)
    toEisenScriptSolid(maze, offset, name + "_Maze")
    toEisenScriptSolid(solution, offset, name + "_Solution")
    toEisenScriptSolid(solutionScaled, offset, name + "_solutionScaled")