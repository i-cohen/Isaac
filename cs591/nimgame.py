__author__ = 'Isaac'
import random

numPiles= random.randint(2, 100)
counter = 0
nimGame =[]

def nimAdd(x,y):
   return (x ^ y)


def findNim(list):
    result =0
    for x in list:
        result = nimAdd(result, x)
    return result
def findNimSumPile(chips, totalOtherNim):
    counter = 0
    while counter < chips:
        if( nimAdd(counter, totalOtherNim)==0):
            return chips - counter
        counter+=1
    return -1


def printGame(list):
    string = str(0) + ":" + str(list[0])
    for x in range(1,len(list)):
        string += "," + str(x) + ":" + str(list[x])
    print (string)



while counter < numPiles:
    nimGame+= [random.randint(1, 100)]
    counter+=1

totalChips = sum(nimGame)

def ai(nimGame):
    if(findNim(nimGame) == 0):
        pile = 0
        while nimGame[pile] < 1:
            pile +=1
        chips =  random.randint(1, nimGame[pile])
        nimGame[pile] -= chips
        print ('I took random' + str(chips) + ' from ' + str(pile) )
        return nimGame
    else:
        maxChips = (-1,-1)
        index = 0
        for x in nimGame:
            if(x > 0 ):
                chips = findNimSumPile(x, findNim( nimGame[0:index] + nimGame[index+1: len(nimGame)]))
                if (chips > maxChips[1]):
                    maxChips = ( index , chips)
            index +=1
        print ('I took ' + str(maxChips[1]) + ' from ' + str(maxChips[0]) )
        nimGame[maxChips[0]] = nimGame[maxChips[0]] - maxChips[1]
        return nimGame






while totalChips > 0:
    printGame(nimGame)
    print(findNim(nimGame))
    choice = input('please choose pile and amount (format pile:amount)')
    choice = choice.split(':')
    choice[0] = int(choice[0])
    choice[1] = int(choice[1])
    nimGame[choice[0]] -= choice[1]
    totalChips = sum(nimGame)
    if totalChips <1:
        print( 'you win')
        break
    nimGame = ai(nimGame)
    totalChips = sum(nimGame)
    #printGame(nimGame)
    if totalChips <1:
        print( 'I win')
        break







