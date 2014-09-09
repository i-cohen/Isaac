import re

def tokenize(terminals, str):
    string='('
    for x in terminals:
        string += x+'|'
    string = string[:(len(string)-1)]
    string+=')'
    tokens = [t for t in re.split(string, str)]
    for x in tokens:
        if (x=='' or x== ' '):
            tokens.remove(x)
    return (tokens)

def directions(str):
    if str[0]== 'stop' and str[1]==';':
        return ('Stop',str[2:])
    if str[0]== 'forward' and str[1]==';':
        (e1,str) = directions(str[2:])
        return ({'Forward':[e1]}, str[2:])
    if str[0]== 'reverse' and str[1]==';':
        (e1,str) = directions(str[2:])
        return ({'Reverse':[e1]}, str[2:])
    if str[0]== 'left' and str[1]=='turn' and str[2]== ';':
        (e1,str) = directions(str[3:])
        return ({'LeftTurn':[e1]}, str[3:])
    if str[0]== 'right' and str[1]=='turn' and str[2]== ';':
        (e1,str) = directions(str[3:])
        return ({'RightTurn':[e1]}, str[3:])

def number(tokens):
    if re.match(r"^([1-9][0-9]*)$", tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens):
    if re.match(r"([a-z][A-Z]*)", tokens[0]):
        return ({"Variable": [tokens[0]]}, tokens[1:])

