import re

def tokenize(terminals, str):
    string='(\s+|'
    for x in terminals:
        if x=="+" or x=="(" or x==")" or x=="*":
            string += '\\'
        string += x+'|'
    string = string[:(len(string)-1)]
    string+=')'
    tokens = [t for t in re.split(string, str)]
    return [t for t in tokens if not t.isspace() and not t == ""]

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

def term(tokens):
    if tokens[0]== '#':
        (e1,tokens)=number(tokens[1:])
        return (e1,tokens)
    if tokens[0]=='@':
        (e1,tokens)=variable(tokens[1:])
        return (e1,tokens)
    if tokens[0] == 'plus' and tokens[1]== '(':
        (e1,tokens)= term(tokens[2:])
        if tokens[0] == ',':
            (e2,tokens)= term(tokens[1:])
            if tokens[0] == ')':
                return ({'Plus':[e1,e2]}, tokens[1:])
    if tokens[0] == 'mult' and tokens[1]== '(':
        (e1,tokens)= term(tokens[2:])
        if tokens[0] == ',':
            (e2,tokens)= term(tokens[1:])
            if tokens[0] == ')':
                return ({'Mult':[e1,e2]}, tokens[1:])
    if tokens[0] == 'log' and tokens[1]== '(':
        (e1,tokens) = term(tokens[2:])
        if tokens[0]==')':
            return ({'Log':[e1]},tokens[1:])
def formula(tokens):
    if tokens[0]=='true':
       return ('True', tokens[1:])
    if tokens[0]=='false':
        return ('False', tokens[1:])
    if tokens[0] == 'not' and tokens[1]== '(':
        (e1,tokens) = formula(tokens[2:])
        if tokens[0]==')':
            return ({'Not':[e1]},tokens[1:])
    if tokens[0] == 'and' and tokens[1]== '(':
        (e1,tokens)= formula(tokens[2:])
        if tokens[0] == ',':
            (e2,tokens)= formula(tokens[1:])
            if tokens[0] == ')':
                return ({'And':[e1,e2]}, tokens[1:])
    if tokens[0] == 'and' and tokens[1]== '(':
        (e1,tokens)= formula(tokens[2:])
        if tokens[0] == ',':
            (e2,tokens)= formula(tokens[1:])
            if tokens[0] == ')':
                return ({'And':[e1,e2]}, tokens[1:])
    if tokens[0] == 'or' and tokens[1]== '(':
        (e1,tokens)= formula(tokens[2:])
        if tokens[0] == ',':
            (e2,tokens)= formula(tokens[1:])
            if tokens[0] == ')':
                return ({'Or':[e1,e2]}, tokens[1:])
    if tokens[0] == 'or' and tokens[1]== '(':
        (e1,tokens)= formula(tokens[2:])
        if tokens[0] == ',':
            (e2,tokens)= formula(tokens[1:])
            if tokens[0] == ')':
                return ({'Or':[e1,e2]}, tokens[1:])
    if tokens[0] == 'equal' and tokens[1]== '(':
        (e1,tokens)= term(tokens[2:])
        if tokens[0] == ',':
            (e2,tokens)= term(tokens[1:])
            if tokens[0] == ')':
                return ({'Equal':[e1,e2]}, tokens[1:])
    if tokens[0] == 'greater' and tokens[1]== 'than' and tokens[2]==('('):
        (e1,tokens)= term(tokens[3:])
        if tokens[0] == ',':
            (e2,tokens)= term(tokens[1:])
            if tokens[0] == ')':
                return ({'GreaterThan':[e1,e2]}, tokens[1:])
    if tokens[0] == 'less' and tokens[1]== 'than' and tokens[2]==('('):
        (e1,tokens)= term(tokens[3:])
        if tokens[0] == ',':
            (e2,tokens)= term(tokens[1:])
            if tokens[0] == ')':
                return ({'LessThan':[e1,e2]}, tokens[1:])

def program(tokens):
    tmp= tokens[0:]
    if tmp[0]== 'print':
       r = formula(tmp[1:])
       if not r is None:
            (e1, tmp)=r
            if tmp[0]==';':
                (e2, tmp)= program(tmp[1:])
                return ({'Print':[e1,e2]}, tmp)
    tmp= tokens[0:]
    if tmp[0]== 'print':
       r = term(tmp[1:])
       if not r is None:
            (e1, tmp)=r
            if tmp[0]==';':
                (e2, tmp)= program(tmp[1:])
                return ({'Print':[e1,e2]}, tmp)
    tmp = tokens[0:]
    if tmp[0] == 'assign' and tmp[1]== '@':
        r= variable(tmp[2:])
        if not r is None:
            (e1, tmp) = r
            if tmp[0] == ':=':
                r=term(tmp[1:])
                if not r is None:
                    (e2,tmp)=r
                    if tmp[0] == ';':
                        r= program((tmp[1:]))
                        if not r is None:
                            (e3, tmp )=r
                            return ({'Assign': [e1,e2,e3]}, tmp)
    tmp = tokens[0:]
    if tmp[0]== 'end' and tmp[1]==';':
        return ('End',tmp[2:])

def complete(tokens):
    #tokens =tokenize(['print', 'assign', '@', 'end', 'true', 'false', 'not', 'and', 'or', 'equal', 'less', 'than', 'greater', ',', 'plus', 'mult', 'log', '#',':=',';' ,'([1-9][0-9]*)', '([a-z][A-Z]*)','(',')' ], tokens)
    tokens = tokenize(['end', ';','print','true', 'assign', '@', ':=', '#', 'not','plus','log','(',')','equal',',','less','than','greater', 'mult','false', 'and', 'or'], tokens)
    r = program(tokens)
    if r is None:
        r= term(tokens)
        if r is None:
            r=formula(tokens)
            if r is None:
                if tokens[0]=='@':
                    r=variable(tokens)
                if tokens[0]=='#':
                  r= number(tokens)
    if r is not None:
        return r