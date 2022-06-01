
from __future__ import print_function
import csv
import math
import queue
import heapq
import sys

class Nodes:
    
    def __init__(self,parent, start_pos,end_pos,size_of_map,initial_map):
        self.x = start_pos[0]
        self.y = start_pos[1]
        self.state = start_pos
        self.parent = parent
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.cost_his = 0
        #self.end_pos = end_pos
        
    def position(self):
        return [self.x, self.y]
    
    def elevate_value(self,x,y):
        elevate_value = initial_map[x][y]
        if elevate_value !="X":
            return int(elevate_value)
        else: 
            return elevate_value

    def euclideanDistance(self,end_pos):
        vert_dis = abs(end_pos[1]-self.state[1])
        horiz_dis = abs(end_pos[0]-self.state[0])
        return math.sqrt(pow(vert_dis,2)+pow(horiz_dis,2))

    def manhattanDistance(self,end_pos):
        vert_dis = abs(end_pos[1]-self.state[1])
        horiz_dis = abs(end_pos[0]-self.state[0])
        return vert_dis + horiz_dis
    
    def heuristics(self,distance,end_pos):
        if distance == "euclidean":
            return self.euclideanDistance(end_pos)
        elif distance == "manhattan":
            return self.manhattanDistance(end_pos)
    
    def checkEnd(self):
        if self.x == end_pos[0] and self.y == end_pos[1]:
            return True
        else:
            return False
    
    def validMove(self,moves):
        if moves == "U":
         return self.elevate_value(self.x,self.y-1) != "X"
        elif moves == "D":
         return self.elevate_value(self.x,self.y+1) != "X"
        elif moves == "L":
         return self.elevate_value(self.x-1,self.y) != "X"
        elif moves == "R":
         return self.elevate_value(self.x+1,self.y) != "X"
    
    def move(self):
        if self.validMove("U"):
            self.up = Nodes(self,[self.x,self.y-1],end_pos,size_of_map,initial_map)
        else:
            self.up = None
        
        if self.validMove("D"):
            self.down = Nodes(self,[self.x,self.y+1],end_pos,size_of_map,initial_map)
        else:
            self.down = None
        
        if self.validMove("L"):
            self.left = Nodes(self,[self.x-1,self.y],end_pos,size_of_map,initial_map)
        else:
            self.left = None
        
        if self.validMove("R"):
            self.right = Nodes(self,[self.x+1,self.y],end_pos,size_of_map,initial_map)
        else:
            self.right = None

    def finalPath(self):
        path_list = []
        path_list.append(self.state)
        node = self
        while node.parent.state[0] != start_pos[0] or node.parent.state[1] != start_pos[1]:
            path_list.append(node.parent.state)
            node = node.parent
        path_list.append(node.parent.state)
        return path_list

    def printFinalMap(self,path_list):
            
        for x in range(1, size_of_map[0] + 1):
            for y in range(1, size_of_map[1] + 1):
                if [x,y] in path_list:
                    print("*",end=" ") 
                elif y == size_of_map[1]:
                    print(initial_map[x][y])
                else:
                    print(initial_map[x][y],end=" ")
            
    def pathcost(self, neighb):
        if neighb.elevate_value(neighb.x,neighb.y) - self.elevate_value(self.x,self.y) > 0:
            return 1 + neighb.elevate_value(neighb.x,neighb.y) - self.elevate_value(self.x,self.y)
        else:
            return 1

    def updateCosthistory(self,cost):
        self.cost_his = cost     

    def bfsearch(self):
        try:
            path_queue = queue.Queue()
            visited_list = []
            count = 0
            path_queue.put(self)
            node = path_queue.get()
            visited_list.append(node.state)
            if self != None:
                while node.checkEnd() == False:
                    
                    node.move()
                    test_counter = 0
                    if node.left != None:
                        if node.left.state not in visited_list:
                            for elem in list(path_queue.queue):
                                if node.left.state == elem.state:
                                    test_counter = 1
                            if test_counter == 0:
                                path_queue.put(node.left)
                        else:
                            pass
                    test_counter = 0
                    if node.right != None:
                        if node.right.state not in visited_list:
                            for elem in list(path_queue.queue):
                                if node.right.state == elem.state:
                                    test_counter = 1
                            if test_counter == 0:
                                path_queue.put(node.right)
                        else:
                            pass
                    test_counter = 0
                    if node.up != None:
                        if node.up.state not in visited_list:
                            for elem in list(path_queue.queue):
                                if node.up.state == elem.state:
                                    test_counter = 1
                            if test_counter == 0:
                                path_queue.put(node.up)
                        else:
                            pass
                    test_counter = 0
                    if node.down != None:
                        if node.down.state not in visited_list:
                            for elem in list(path_queue.queue):
                                if node.down.state == elem.state:
                                    test_counter = 1
                            if test_counter == 0:
                                path_queue.put(node.down)
                        else:
                            pass

                    if path_queue.empty():
                        return None
                    else:
                        node = path_queue.get()
                    visited_list.append(node.state)                
                    count +=1
                   
                return node
            else:
                return None        
                
        except Exception as inst:
            return None
            

    def uniformCostSearch(self):
        try:
            path_queue = []
            visited_list = []
            count = 0
            base = 10000000000
            heapq.heappush(path_queue, (1, self))
            temp, node = heapq.heappop(path_queue)
            visited_list.append(node.state)
            if self != None:
                while node.checkEnd() == False:
                    node.move()

                    if node.left != None:
                        if node.left.state not in visited_list:
                            count +=1
                            heapq.heappush(path_queue, (node.pathcost(node.left)+count/base, node.left))
                        else:
                            pass
                    
                    if node.right != None:
                        if node.right.state not in visited_list:
                            count +=1
                            heapq.heappush(path_queue, (node.pathcost(node.right)+count/base, node.right))
                        else:
                            pass

                    if node.up != None:
                        if node.up.state not in visited_list:
                            count +=1
                            heapq.heappush(path_queue, (node.pathcost(node.up)+count/base, node.up)) 
                        else:
                            pass
                        
                    if node.down != None:
                        if node.down.state not in visited_list:
                            count +=1
                            heapq.heappush(path_queue, (node.pathcost(node.down)+count/base, node.down))
                            
                        else:
                            pass

                    temp, node = heapq.heappop(path_queue)
                    visited_list.append(node.state)                
                    
                return node
        except:
            return None
    def aStarSearch(self,distance):
        try:

            path_queue = []
            visited_list = []
            count = 0
            base = 10000000000
            heapq.heappush(path_queue, (1, self))
            temp, node = heapq.heappop(path_queue)
            visited_list.append(node.state)
            if self != None:
                while node.checkEnd() == False:
                    node.move()

                    if node.left != None:
                        if node.left.state not in visited_list:
                            count +=1
                            node.left.updateCosthistory(node.cost_his + node.pathcost(node.left))
                            heapq.heappush(path_queue, (node.left.cost_his + node.left.heuristics(distance,end_pos)+count/base, node.left))
                        else:
                            pass
                        
                    if node.right != None:
                        if node.right.state not in visited_list:
                            count +=1
                            node.right.updateCosthistory(node.cost_his + node.pathcost(node.right))
                            heapq.heappush(path_queue, (node.right.cost_his + node.right.heuristics(distance,end_pos)+count/base, node.right))
                        else:
                            pass

                    if node.up != None:
                        if node.up.state not in visited_list:
                            count +=1
                            node.up.updateCosthistory(node.cost_his + node.pathcost(node.up))
                            heapq.heappush(path_queue, (node.up.cost_his + node.up.heuristics(distance,end_pos) + count/base, node.up))
                            
                        else:
                            pass
                        
                    if node.down != None:
                        if node.down.state not in visited_list:
                            count +=1
                            node.down.updateCosthistory(node.cost_his + node.pathcost(node.down))
                            heapq.heappush(path_queue, (node.down.cost_his + node.down.heuristics(distance,end_pos)+count/base, node.down))
                            
                        else:
                            pass
                    
                            

                    temp, node = heapq.heappop(path_queue)
                    visited_list.append(node.state)                
                   
                return node
        except:
            return None 

if __name__ == "__main__":

    map_txt = sys.argv[1]
    algorithm = sys.argv[2]
    try:
        heuristic = sys.argv[3]
    except:
        pass
    
    f = open(map_txt)
    readMap = csv.reader(f)

    size_of_map_text = next(readMap)
    start_pos_text = next(readMap)
    end_position_text = next(readMap)

    state_map_list = []
    for row in readMap:
        state_map_list.append(row[0].split(" "))

    state_map = state_map_list

    size_of_map = list(map(int,size_of_map_text[0].split(" ")))

    start_pos = list(map(int,start_pos_text[0].split(" ")))

    end_pos = list(map(int,end_position_text[0].split(" ")))


    temp_map = []
    for iy in range(size_of_map[0]+2):
        temp_row = []
        if iy == 0:
            for ix in range(size_of_map[1]+2):
                    temp_row.append("X")
        elif iy == size_of_map[0]+1:
            for ix in range(size_of_map[1]+2):
                    temp_row.append("X")
        else:
            temp_row.append("X")
            for ix in range(size_of_map[1]):
                temp_row.append(state_map_list[iy-1][ix])
            temp_row.append("X")
        temp_map.append(temp_row)


    initial_map = temp_map


    node = Nodes(None,start_pos,end_pos,size_of_map,initial_map)
    node.move()
    
    if algorithm == "bfs":
        end_node = node.bfsearch()
    elif algorithm == "ucs":
        end_node = node.uniformCostSearch()
    elif algorithm == "astar":
        if heuristic == "euclidean":
            end_node = node.aStarSearch("euclidean")
        elif heuristic == "manhattan":
            end_node = node.aStarSearch("manhattan")
    if end_node == None:
        print("null")
    else:
        path_list = end_node.finalPath()
        end_node.printFinalMap(path_list)
