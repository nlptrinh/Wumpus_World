import os
import time
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
map_size = 10
Map = [[] for i in range(100)]
map_state = [['']*100 for i in range(100)]
explored = [[False]*100 for i in range(100)]
already_in_queue = [[] for i in range(100)]
is_shot = [[False]*100 for i in range(100)]
successor = [[0]*100 for i in range(100)]
dx = [-1,0,0,1] 
dy =  [0,-1,1,0]
way_back = [[0]*100 for i in range(100)]
arrow_point = -100
gold_point = 100
class pile:
    def __init__(self,x,y): 
        self.x = x
        self.y = y
start_state = pile(0,0) 

def inMap( current_pile):
    if (current_pile.x >= 0 and current_pile.x < map_size and current_pile.y >= 0 and current_pile.y < map_size):
        return True
    return False

def backtrack(current_pile):
    back_pile = successor[current_pile.x][current_pile.y]
    while (back_pile.x != start_state.x or back_pile.y != start_state.y):
        back_pile = successor[back_pile.x][back_pile.y]
    
def reset_already_in_queue():
    for i in range(map_size):
        for j in range(map_size):
            already_in_queue[i][j] = False
        
    

def shortest_path( current_pile):

    adjacent_piles = []
    adjacent_piles.append(pile(current_pile.x,current_pile.y + 1 ))
    adjacent_piles.append(pile(current_pile.x - 1,current_pile.y ))
    adjacent_piles.append(pile(current_pile.x + 1,current_pile.y ))
    adjacent_piles.append(pile(current_pile.x,current_pile.y - 1 ))
    min_dis = 1000000000
    min_dis_pile = pile(0,0)
    for adjacent_pile in adjacent_piles:
        if (inMap(adjacent_pile) and explored[adjacent_pile.x][adjacent_pile.y]):
            min_dis = min(min_dis, way_back[adjacent_pile.x][adjacent_pile.y])
            min_dis_pile = adjacent_pile
        
    way_back[current_pile.x][current_pile.y] = min_dis + 1
    successor[current_pile.x][current_pile.y] = min_dis_pile

def shoot_pile(current_pile, current_point):
    if (inMap(current_pile) and explored[current_pile.x][current_pile.y] == False):
        if (not is_shot[current_pile.x][current_pile.y]):
            print("Shooting arrow at (" + str(current_pile.x) + "," + str(current_pile.y) + ")")
            current_point += arrow_point
            
            is_shot[current_pile.x][current_pile.y] = True
            if (Map[current_pile.x][current_pile.y] == "W"):
                Map[current_pile.x][current_pile.y] = "-"
            
            if (map_state[current_pile.x][current_pile.y] != "potential_pit" and map_state[current_pile.x][current_pile.y] != "absolute_pit"):
                map_state[current_pile.x][current_pile.y] = "safe"
        
    

def guess_gold( current_pile, current_point):
    current_point += gold_point
    print("Collecting gold.)

def guess_safe( current_pile):
    if (inMap(current_pile)):
        map_state[current_pile.x][current_pile.y] = "safe"
    

def guess_ok( current_pile):
    bottom_pile = pile(current_pile.x,current_pile.y + 1 )
    left_pile = pile(current_pile.x - 1,current_pile.y )
    right_pile = pile(current_pile.x + 1,current_pile.y )
    top_pile = pile (current_pile.x,current_pile.y - 1 )
    guess_safe(top_pile)
    guess_safe(left_pile)
    guess_safe(right_pile)
    guess_safe(bottom_pile)

def casting_full_pit( current_pile):
    if (inMap(current_pile) and explored[current_pile.x][current_pile.y] == False):
        if (map_state[current_pile.x][current_pile.y] == "potential_pit"):
            map_state[current_pile.x][current_pile.y] = "absolute_pit"
        
def guess_pit( current_pile, count):
    if (inMap(current_pile) and explored[current_pile.x][current_pile.y] == False):
        if (map_state[current_pile.x][current_pile.y] != "safe"):
            if (map_state[current_pile.x][current_pile.y] == ""):
                map_state[current_pile.x][current_pile.y] = "potential_pit"
            count += 1
        
def guess_breeze( current_pile):
    bottom_pile = pile (current_pile.x,current_pile.y + 1 )
    left_pile = pile (current_pile.x - 1,current_pile.y )
    right_pile = pile (current_pile.x + 1,current_pile.y )
    top_pile = pile (current_pile.x,current_pile.y - 1 )
    count = 0
    guess_pit(top_pile, count)
    guess_pit(left_pile, count)
    guess_pit(right_pile, count)
    guess_pit(bottom_pile, count)
    if (count == 1):
        casting_full_pit(top_pile)
        casting_full_pit(left_pile)
        casting_full_pit(right_pile)
        casting_full_pit(bottom_pile)
    
def guess_stench( current_pile, current_point):
    bottom_pile = pile (current_pile.x,current_pile.y + 1 )
    left_pile = pile (current_pile.x - 1,current_pile.y )
    right_pile = pile (current_pile.x + 1,current_pile.y )
    top_pile = pile (current_pile.x,current_pile.y - 1 )
    shoot_pile(top_pile, current_point)
    shoot_pile(left_pile, current_point)
    shoot_pile(right_pile, current_point)
    shoot_pile(bottom_pile, current_point)
    if (Map[current_pile.x][current_pile.y] == "S"):
        Map[current_pile.x][current_pile.y] = "-"

def guess_abstract(current_pile, current_point):

    if (Map[current_pile.x][current_pile.y] == "B"):
        print("Current point: (" + str(current_pile.x) + " " + str(current_pile.y) + ")")
        print("Found Breeze")
        guess_breeze(current_pile)
    
    if (Map[current_pile.x][current_pile.y]== "S"):
        print("Current point: (" + str(current_pile.x) + " " + str(current_pile.y) + ")")
        print("Found Stench")
        guess_stench(current_pile, current_point)
    
    if (Map[current_pile.x][current_pile.y] == "G"):
        print("Current point: (" + str(current_pile.x) + " " + str(current_pile.y) + ")")
        print("Found Gold")
        guess_gold(current_pile, current_point)
        if (Map[current_pile.x][current_pile.y] == "G"):
            Map[current_pile.x][current_pile.y] = "-"
    
    if (Map[current_pile.x][current_pile.y] == "-"):
        print("Current point: (" + str(current_pile.x) + ", " + str(current_pile.y) + ")")
        guess_ok(current_pile)

def printMap( current_pile ):
    time.sleep(1)
    cls()
    tmp_map = [['']*100 for i in range(100)]
    for i in range(map_size):
        for j in range(map_size):
            tmp_map[i][j] = Map[i][j]
            if (Map[i][j] == "A"):
                tmp_map[i][j] = "-"
            
    for i in range(map_size):
        for j in range(map_size):
            if (current_pile.x == i and current_pile.y == j):
                tmp_map[i][j] = "A"

    for i in range(map_size):
        for j in range(map_size):
            print(tmp_map[i][j],end=' ')
        print()
    

def go_next_pile( current_pile, current_point, finish, steps):

    printMap(current_pile)
    guess_abstract(current_pile, current_point)
    if (way_back[current_pile.x][current_pile.y] + steps == 20):
        print("Wait! Agent have to come back home!")
        backtrack(current_pile)
        finish = True
        return
    
    for i in range(4):
        next_pile = pile (current_pile.x + dx[i],current_pile.y + dy[i] )
        if (inMap(next_pile)):
            if (explored[next_pile.x][next_pile.y] == False and map_state[next_pile.x][next_pile.y] == "safe"):
                explored[next_pile.x][next_pile.y] = True
                shortest_path(next_pile)
                steps += 1
                go_next_pile(next_pile, current_point, finish, steps)
                if (finish):
                    return
                steps += 1
             
def play_games(start_pile):
    point = 0
    Map[start_pile.x][start_pile.y] = "-"
    finish = False
    explored[start_pile.x][start_pile.y] = True
    step = 0
    go_next_pile(start_pile, point, finish, step)
    point += 10
    print( "Total point: " + str(point))

def read_map(file_path):
    file = open(file_path)
    if (file == ''):
        return False
    line = file.readline()
    map_size = int(line)
    cnt = 0
    
    while line:
        line = file.readline().split(".")
        if line == ['']: break
        for i in range(len(line)):
            Map[cnt].append(line[i])
        cnt += 1

    for i in range(map_size):
        for j in range(map_size):
            if (Map[i][j] == "A"):
                start_state = pile(i,j)
    return True

path = "map1.txt"
if (read_map(path)):
    for i in range(map_size):
        for j in range(map_size): 
            print(Map[i][j],end = " ")
        print()
    print()
    play_games(start_state)

else: print("Can not read file")