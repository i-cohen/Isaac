import re

def tokenize(terminals, str):
    string='(\s+|'
    for x in terminals:
        if x=="+" or x=="(" or x==")" or x=="*" or x=='|' or x=='&':
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

def term(tmp, top):
    tokens = tmp[0:]
    if tokens[0]== '#':
        r = number(tokens[1:])
        if not r is None:
            (e1,tokens)=r
            if not top or len(tokens) == 0:
                return (e1,tokens)
    tokens = tmp[0:]
    if tokens[0]=='@':
        r=variable(tokens[1:])
        if not r is None:
            (e1,tokens)= r
            if not top or len(tokens) == 0:
                return (e1,tokens)
    tokens = tmp[0:]
    if tokens[0] == 'plus' and tokens[1]== '(':
        r = term(tokens[2:], False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                r = term(tokens[1:], False)
                if not r is None:
                    (e2,tokens) =r
                    if tokens[0] == ')':
                        if not top or len(tokens) == 0:
                            return ({'Plus':[e1,e2]}, tokens[1:])
    tokens = tmp[0:]
    if tokens[0] == 'mult' and tokens[1]== '(':
        r = term(tokens[2:], False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                r = term(tokens[1:], False)
                if not r is None:
                    (e2,tokens) =r
                    if tokens[0] == ')':
                        if not top or len(tokens) == 0:
                            return ({'Mult':[e1,e2]}, tokens[1:])
    tokens = tmp[0:]
    if tokens[0] == 'log' and tokens[1]== '(':
        r = term(tokens[2:], False)
        if not r is None:
            (e1,tokens) = r
            if tokens[0]==')':
                if not top or len(tokens) == 0:
                    return ({'Log':[e1]},tokens[1:])
    tokens = tmp[0:]
    if tokens[0]== '(':
        r = term(tokens[1:], False)
        if not r is None:
            (e1,tokens)= r
            if tokens[0]=='+':
                r=term(tokens[1:], False)
                if not r is None:
                    (e2,tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Plus':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0]== '(':
        r = term(tmp[1:], False)
        if not r is None:
            (e1,tokens)= r
            if tokens[0]=='*':
                r=term(tokens[1:], False)
                if not r is None:
                    (e2,tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Mult':[e1,e2]}, tokens)
def formula(tmp, top):
    tokens = tmp[0:]
    if tokens[0]=='true':
        tokens = tokens[1:]
        if not top or len(tokens)==0:
            return ('True', tokens)
    tokens = tmp[0:]
    if tokens[0]=='false':
        tokens = tokens[1:]
        if not top or len(tokens)==0:
            return ('False', tokens)
    tokens = tmp[0:]
    if tokens[0] == 'not' and tokens[1]== '(':
        r = formula(tokens[2:], False)
        if not r is None:
            (e1,tokens) = r
            if tokens[0]==')':
                tokens = tokens[1:]
                if not top or len(tokens):
                    return ({'Not':[e1]},tokens)
    tokens = tmp[0:]
    if tokens[0] == 'and' and tokens[1]== '(':
        r = formula(tokens[2:], False)
        if not r is None:
            (e1,tokens) = r
            if tokens[0] == ',':
                r= formula(tokens[1:], False)
                if not r is None:
                    (e2,tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens)==0:
                            return ({'And':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == 'or' and tokens[1]== '(':
        r = formula(tokens[2:], False)
        if not r is None:
            (e1,tokens) =r
            if tokens[0] == ',':
                r = formula(tokens[1:], False)
                if not r is None:
                    (e2,tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens)==0:
                            return ({'Or':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == 'equal' and tokens[1]== '(':
        r= term(tokens[2:], False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ',':
                r = term(tokens[1:], False)
                if not r is None:
                    (e2,tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens)==0:
                            return ({'Equal':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == 'greater' and tokens[1]== 'than' and tokens[2]==('('):
        r = term(tokens[3:], False)
        if not r is None:
            (e1,tokens)= r
            if tokens[0] == ',':
                r = term(tokens[1:], False)
                if not r is None:
                    (e2,tokens)=r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens)==0:
                            return ({'GreaterThan':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == 'less' and tokens[1]== 'than' and tokens[2]==('('):
        r=  term(tokens[3:], False)
        if not r is None:
            (e1,tokens)= r
            if tokens[0] == ',':
                r = term(tokens[1:], False)
                if not r is None:
                    (e2,tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens)==0:
                            return ({'LessThan':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == '(':
        r = term(tokens[1:], False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0]=='==':
                r = term(tokens[1:], False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Equal':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == '(':
        r = term(tokens[1:], False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0]=='<':
                r = term(tokens[1:], False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'LessThan':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == '(':
        r = term(tokens[1:], False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0]=='>':
                r = term(tokens[1:], False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'GreaterThan':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == '(':
        r = formula(tokens[1:], False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0]=='&' and tokens[1] == '&':
                r = formula(tokens[2:], False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'And':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == '(':
        r = formula(tokens[1:], False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0]=='|' and tokens[1] == '|':
                r = formula(tokens[2:], False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ')':
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return ({'Or':[e1,e2]}, tokens)

def program(tmp, top):
    tokens= tmp[0:]
    if tokens[0]== 'print':
       r = formula(tokens[1:], False)
       if not r is None:
            (e1, tokens)=r
            if tokens[0]==';':
                r= program(tokens[1:], False)
                if not r is None:
                    (e2, tokens) = r
                    tokens = tokens[1:]
                    if not top or len(tokens) == 0:
                        return ({'Print':[e1,e2]}, tokens)
    tokens= tmp[0:]
    if tokens[0]== 'print':
       r = term(tokens[1:], False)
       if not r is None:
            (e1, tokens)=r
            if tokens[0]==';':
                r = program(tokens[1:], False)
                if not r is None:
                    (e2, tokens) = r
                    tokens = tokens[1:]
                    if not top or len(tokens) == 0:
                        return ({'Print':[e1,e2]}, tokens)
    tokens = tmp[0:]
    if tokens[0] == 'assign' and tokens[1]== '@':
        r= variable(tokens[2:])
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ':=':
                r=term(tokens[1:], False)
                if not r is None:
                    (e2,tokens)=r
                    if tokens[0] == ';':
                        r= program((tokens[1:]),False)
                        if not r is None:
                            (e3, tokens )=r
                            if not top or len(tokens) == 0:
                                return ({'Assign': [e1,e2,e3]}, tokens)
    tokens = tmp[0:]
    if tokens[0]== 'end' and tokens[1]==';':
        tokens = tokens[2:]
        if not top or len(tokens) == 0:
            return ('End',tokens)

def complete(tokens):
    #tokens =tokenize(['print', 'assign', '@', 'end', 'true', 'false', 'not', 'and', 'or', 'equal', 'less', 'than', 'greater', ',', 'plus', 'mult', 'log', '#',':=',';' ,'([1-9][0-9]*)', '([a-z][A-Z]*)','(',')' ], tokens)
    tokens = tokenize(['end', ';','print','true', 'assign', '@', ':=', '#', 'not','plus','log','(',')','equal',',','less','than','greater', 'mult','false', 'and', 'or', '+','*','&','|'], tokens)
    r = program(tokens, True)
    if r is None:
        r= term(tokens, True)
        if r is None:
            r=formula(tokens, True)
            if r is None:
                if tokens[0]=='@':
                    r=variable(tokens)
                if tokens[0]=='#':
                  r= number(tokens)
    if r is not None:
        return r







