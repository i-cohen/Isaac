import re
import parse
from math import log,floor

Node = dict
Leaf = str


def evalTerm(env,t):
    if type(t)== Node:
        for label in t:
            children = t[label]
            if label == 'Number':
                x = children[0]
                return x
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Parens':
                x = children[0]
                f= evalTerm(env,x)
                return   f
            elif label == 'Log':
                x = children[0]
                f = evalTerm(env,x)
                v = log(int(f), 2)
                return v
            elif label == 'Plus':
                x = children[0]
                f1 = evalTerm(env,x)
                x2 = children[1]
                f2 = evalTerm(env, x2)
                return int(f1)+ int(f2)
            elif label == 'Mult':
                x = children[0]
                f1 = evalTerm(env,x)
                x2 = children[1]
                f2 = evalTerm(env, x2)
                return int(f1) * int(f2)

def evalFormula(env, t):
    if type(t)== Node:
        for label in t:
            children = t[label]
            if label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Parens':
                x = children[0]
                f = evalFormula(env,x)
                return f
            elif label == 'Not':
                x = children[0]
                f = evalFormula(env,x)
                return not f
            elif label == 'Xor':
                x = children[0]
                f1 = evalFormula(env,x)
                x2 = children[1]
                f2 = evalFormula(env, x2)
                return bool(f1) != bool(f2)
            elif label == 'Equals':
                x = children[0]
                f1 = evalFormula(env,x)
                if not f1 is None:
                    x2 = children[1]
                    f2 = evalFormula(env, x2)
                    return bool(f1) == bool(f2)
                else:
                    f1 = evalTerm(env,x)
                    x2 = children[1]
                    f2 = evalTerm(env, x2)
                    return int(f1) == int(f2)
            elif label == 'LessThan':
                x = children[0]
                f1 = evalTerm(env,x)
                x2 = children[1]
                f2 = evalTerm(env, x2)
                return int(f1) < int(f2)
    elif type(t) == Leaf:
        if t == 'True':
            return True
        if t == 'False':
            return False
def execProgram(env, s):
    if type(s) == Node:
        for label in s:
            if label == 'Print':
                children = s[label]
                f = children[0]
                p = children[1]
                v = evalTerm(env, f)
                if v is None:
                    v = evalFormula(env, f)
                (env, o) = execProgram(env, p)
                return (env,[v] + o)
            if label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                f = children[1]
                p = children[2]
                v = evalTerm(env, f)
                if v is None:
                    v = evalFormula(env, f)
                env[x] = v
                (env1,o1) = execProgram(env, p)
                return (env1,o1)
            if label == 'If':
                children = s[label]
                x = children[0]
                f = children[1]
                p = children[2]
                v = evalTerm(env, x)
                if v is None:
                    v = evalFormula(env, x)
                if v == True:
                    (env1, o1) = execProgram(env, f)
                    (env2, o2) = execProgram(env1, p)
                    return  (env2, o1+o2)
                else:
                    return execProgram(env, p)
            if label == 'While':
                children = s[label]
                x = children[0]
                f = children[1]
                p = children[2]
                v = evalTerm(env, x)
                if v is None:
                    v = evalFormula(env, x)
                if v == False:
                    return execProgram(env, p)
                else:
                    (env1, o1) = execProgram(env , f)
                    (env2, o2) = execProgram(env1, s)
                    return (env2, o1+o2)
    elif type(s) == Leaf:
        if s == 'End':
            return (env, [])

def interpret(s):
    tokens = tokenize(['true', 'false','(',')','not','xor','log', '+','*','print','assign', 'if', 'while',';', ':=','{','}','==','<'], s)
    if not tokens is None:
        r = parse.program(tokens)
        if not r is None:
            (parsedTokens,tmp) =r
            r = execProgram({}, parsedTokens)
            if not r is None:
                (env, output)= r
                return output




def tokenize(terminals, str):
    string='(\s+|'
    for x in terminals:
        if x=="+" or x=="(" or x==")" or x=="*" or x==';' or x=='{' or x=='}':
            string += '\\'
        string += x+'|'
    string = string[:(len(string)-1)]
    string+=')'
    tokens = [t for t in re.split(string, str)]
    return [t for t in tokens if not t.isspace() and not t == ""]

