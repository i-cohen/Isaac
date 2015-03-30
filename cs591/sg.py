__author__ = 'Isaac'

def nimAdd(x,y):
   return (x ^ y)

def mulNimAdd(list):
    last=0
    for x in list:
        x= int(x)
        last =nimAdd(last,x)
    return last

def mex (followers) :
    y=0
    while True:
        if y in followers:
            y+=1
        else:
            return y



def subGame(subtractionSet, upperbound = 100 ):
    sgValues= {}
    for x in range(0,upperbound+1):
        sgValues[x] = 0
    for x in range(0,upperbound+1):
        followers =[]
        for y in subtractionSet:
            if x-y>=0:
                followers.append(sgValues[x-y])
        sgValues[x] = mex(followers)
    return sgValues

def evenIfNotAll(upperbound = 100):
    sgValues={}
    sgValues[0] =0
    for x in range(1,upperbound+1):
        if x % 2 is 0:
            sgValues[x] = (x//2) -1
        else:
            sgValues[x] = (x)//2 +1
    return sgValues

def atLeastHalf(upperbound = 100):
    sgValues ={}
    for x in range(0,upperbound+1):
        counter =0
        found = False
        while not found:
            if pow(2,counter) > x:
                sgValues[x] = counter
                found = True
            else:
                counter +=1
    return sgValues

def allGames():
    choice = input('choose how many in each game with format as follows : subtraction game, even if not all, at least half ex: 4,5,12')
    choice = choice.split(',')
    sub = subGame([1,2,3], int(choice[0]))
    even = evenIfNotAll(int(choice[1]))
    atLeast = atLeastHalf(int(choice[2]))
    return mulNimAdd([sub[int(choice[0])], even[int(choice[1])], atLeast[int(choice[2])]])


def lasker(upperBound =10):
    sgValues = {}
    sgValues[0] = 0
    for x in range(1,upperBound+1):
        # if x % 4 is 1 or x % 4 is 2:
        #     sgValues[x] = x
        # if x % 4 is 3:
        #     sgValues[x]= x+1
        # if x % 4 is 0:
        #     sgValues[x] = x-1
        followers = []
        for y in range(0,x):
            followers.append(sgValues[y])
        if x>1:
            y = x//2
            z = x-y
            followers.append(nimAdd(z,y))
        sgValues[x] = mex(followers)
    return sgValues





print('subtraction game m=3 ' ,subGame(range(0,3)))
print('subtraction game m=20 ' , subGame(range(0,20)))
print('subtraction game m=45 ' , subGame(range(0,45)))
print('even if not all: ' , evenIfNotAll(100))
print('At LEast Half: ', atLeastHalf())
print('Lasker ' ,lasker(100))
print('sum of games')
print(allGames())
