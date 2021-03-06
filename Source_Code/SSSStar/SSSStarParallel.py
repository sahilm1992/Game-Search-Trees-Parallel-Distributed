import sys
import numpy as np
import random
import re
from time import time
import multiprocessing as mp
import heapq as hpq
from random import randint
from copy import deepcopy

output = mp.Queue()

from numpy.core.fromnumeric import cumprod

#openList = []

MAXVALUE = 5000
LIVE = "LIVE"
SOLVED = "SOLVED"
MAXNODE = "MAX"
MINNODE = "MIN"
LEAF = "LEAF"
BOARDSIZE = 9
whoseTurn = 0

listOne = []
listZero = []
listMinusOne = []

PRINTING_TRIADS = ((0, 1, 2), (3, 4, 5), (6, 7, 8))
WINNING_TRIADS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
    (2, 5, 8), (0, 4, 8), (2, 4, 6))
myBoard = [0,0,0,0,0,0,0,0,0]
MARKERS = ['_', 'O', 'X']
END_PHRASE = ('draw', 'win', 'loss')

class Node:

    board = []
    listChild = []
    type = ""
    status = ""
    eValue = 0
    isRoot = ""
    isExamined = ""
    parent = None

    def __init__(self):
        self.board = np.zeros((BOARDSIZE), dtype=int)
        self.listChild = []
        self.status = LIVE
        self.type = ""
        self.eValue = MAXVALUE
        self.isRoot = "N"
        self.isExamined = "N"

    def __lt__(self, other):
        return (self.eValue >= other.eValue)


def evaluateLeafNode(node):

    for triad in WINNING_TRIADS:
        triad_sum = node.board[triad[0]] + node.board[triad[1]] + node.board[triad[2]]
        if triad_sum == 3 or triad_sum == -3:
            #print("Value ======================",node.board[triad[0]])
             return node.board[triad[0]]  # Take advantage of "_token" values
    return 0

def checkIsLeaf(node):

    count = 0
    for i in range(0, BOARDSIZE):
        if node.board[i] == 0:
            count += 1
            #if count > 1:
                #return "N"

    if count == 0:
        return "Y"
    else :
        return "N"

def removeParentNode(node, openList):

    if openList.count(node) != 0:
        openList.remove(node)

    return

def minVal(a, b):

    if a < b:
        return a
    else:
        return b

def isWinner(tempBord):

     count = 0
     for triad in WINNING_TRIADS:
        triad_sum = tempBord[triad[0]] + tempBord[triad[1]] + tempBord[triad[2]]
        if triad_sum == 3 or triad_sum == -3:
            #print("Value ======================",node.board[triad[0]])
             return tempBord[triad[0]]  #Take advantage of "_token" values

     for i in range(0, BOARDSIZE):
         if tempBord[i] == 0:
             return 0

     return 10


def SSSStar(openList):

    while True :

        #print("Before printing" ,len(openList))
        current = hpq.heappop(openList)
        #print(current.type, current.board, current.status, current.eValue)
        #print(len(openList))

        if current.status == LIVE:
            if current.type == LEAF:

                parent = current.parent

                if parent.type == MAXNODE:
                    current.type = MINNODE
                else :
                    current.type = MAXNODE

                current.status = SOLVED
                val = evaluateLeafNode(current)
                current.eValue = val
                hpq.heappush(openList,current)

            elif current.type == MINNODE:
                allChilds = current.listChild
                if len(allChilds) > 0:
                    childNode = allChilds[0]
                    childNode.isExamed = "Y"
                    hpq.heappush(openList,childNode)

            elif current.type == MAXNODE:
                allChilds = current.listChild

                for i in range(0, len(allChilds)):
                    childNode = allChilds[i]
                    childNode.isExamed = "Y"
                    hpq.heappush(openList,childNode)

        elif current.status == SOLVED:

            if current.isRoot == "Y":
                return current.eValue

            elif current.type == MINNODE:
                myParent = current.parent
                removeParentNode(myParent, openList)

                myParent.status = SOLVED
                myParent.isExamined = "Y"
                #myParent.eValue = current.eValue
                myParent.eValue = minVal(myParent.eValue, current.eValue)
                if myParent.isRoot == "Y":
                    myParent.board = deepcopy(current.board)
                hpq.heappush(openList, myParent)

            elif current.type == MAXNODE:

                tempFlag = False
                allChilds = current.parent.listChild
                for i in range(0, len(allChilds)):

                    tempChild = allChilds[i]

                    if current is tempChild :#I should not be that child
                        continue

                    if tempChild.isExamined == "N":
                        #print("child to be added is ", tempChild.board)
                        tempChild.isExamined = "Y"
                        #tempChild.eValue = current.eValue
                        tempChild.eValue = minVal(current.eValue, tempChild.eValue)
                        #tempChild.type = MAXNODE
                        tempFlag = True
                        hpq.heappush(openList, tempChild)
                        break

                if not tempFlag :
                    myP = current.parent
                    myP.status = SOLVED
                    myP.isExamined = "Y"
                    #myP.eValue = current.eValue
                    myP.eValue = minVal(current.eValue, myP.eValue)

                    if myP.isRoot == "Y":
                        myP.board = deepcopy(current.board)

                    hpq.heappush(openList, myP)


    return

def print_board(board):
    
    '''for row in PRINTING_TRIADS:
        for hole in row:
            print(MARKERS[board[hole]])
        print()'''
    print("Current status of the board ")
    j = 0
    for i in range (0, 3):
            
        print(MARKERS[myBoard[j]],"|",MARKERS[myBoard[j+1]],"|",MARKERS[myBoard[j+2]])
        j += 3
            
    print('\n')

def recv_human_move(board):
    
    looping = True
    while looping:
        try:
            inp = input("Your move: ")
            yrmv = int(inp)
            if 0 <= yrmv <= 8:
                if board[yrmv] == 0:
                    looping = False
                else:
                    print("Spot already filled.")
            else:
                print("Bad move.")

        except EOFError:
            print('\n')
            sys.exit(0)
        except NameError:
            print("Not 0-9, try again.")
        except SyntaxError:
            print("Not 0-9, try again.")

        if looping:
            print_board(board)

    return yrmv

def addDetails(node):

    for i in range(0,BOARDSIZE):
        if node.board[i] == 0:
            tempNode = Node()

            if node.type == MAXNODE :
                tempNode.type = MINNODE
            else:
                tempNode.type = MAXNODE

            for j in range(0, BOARDSIZE):
                tempNode.board[j] = node.board[j]

            #tempNode.board = deepcopy(node.board)
            if node.type == MAXNODE:
                tempNode.board[i] =  1
            else :
                tempNode.board[i] =  -1

            #tempNode.board[i] =  1
            tempNode.parent = node

            tempStatus = checkIsLeaf(tempNode)

            if tempStatus == 'Y':
                tempNode.type = LEAF
                tempVal = evaluateLeafNode(tempNode)
                tempNode.eValue = tempVal

            listChild = node.listChild
            listChild.append(tempNode)
            node.listChild = listChild

            if tempStatus == 'N':
                addDetails(tempNode)

    return

def processNodes(newnode, output) :

    global listOne
    global listZero
    global listMinusOne
    global myBoard

    openList = []



    currentBoard = deepcopy(newnode.board)
    global MINNODE
    newnode.type = MINNODE
    newnode.isRoot = "Y"
    newnode.isExamined = "Y"

    addDetails(newnode)

    hpq.heappush(openList,newnode)

    dataVal = SSSStar(openList)
    #myBoard = deepcopy(tempMyBoard)

    dictResult = {}
    dictResult[dataVal] = currentBoard
    #print("Assigning board ", currentBoard)
    output.put(dictResult)
    #print("computed .......")
    

    global whoseTurn
    whoseTurn = 0

    #print(len(listMinusOne), len(listZero), len(listOne))

    return

####################### start main here ############################
if __name__ == '__main__':
    

    while(isWinner(myBoard) == 0):#do this while any one of them will win

        if whoseTurn == 0 :#humans turn

            choice = recv_human_move(myBoard)
            myBoard[choice] = -1
            whoseTurn = 1

            listOne.clear()
            listZero.clear()
            listMinusOne.clear()

        else:#computer turn

            print("Waiting for system to find its move ........")

            processes = []

            for i in range(0, BOARDSIZE):
                if myBoard[i] == 0:

                    newnode = Node()
                    newnode.board = deepcopy(myBoard)

                    newnode.board[i] = 1
                    tempProcess = mp.Process(target=processNodes, args=(newnode, output))
                    processes.append(tempProcess)
                    
            start = time()
            for p in processes:
                p.start()

            #wait for every process to end
            for p in processes:
                p.join()

            finish = time()
            for p in processes:
                dictData = output.get()
                if 1 in dictData.keys():
                    listOne.append(dictData[1])
                elif 0 in dictData.keys():
                    listZero.append(dictData[0])
                else :
                    listMinusOne.append(dictData[-1])

            if len(listOne) > 0:

                myBoard = deepcopy(random.choice(listOne))
            elif len(listZero) > 0:

                myBoard = deepcopy(random.choice(listZero))
            elif len(listMinusOne) > 0:

                myBoard = deepcopy(random.choice(listMinusOne))


            #print("============================ After comp turn ============================= ", myBoard)
            j=0
            print("Current status of the board ")
            for i in range (0, 3):
            
                print(MARKERS[myBoard[j]],"|",MARKERS[myBoard[j+1]],"|",MARKERS[myBoard[j+2]])
                j += 3
            
            print('\n')
            print("Time taken : ",finish-start)
            whoseTurn = 0

    #print(END_PHRASE[isWinner(myBoard)])
    finalDat = isWinner(myBoard)
    if finalDat == 10:
        finalDat = 0
    print(["Tie", "Computer Won", "You won"][finalDat])
