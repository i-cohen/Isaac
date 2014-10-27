######################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3 (skeleton code)
# interpret.py
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def evalTerm(env, e):
    if type(e)== Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                x = children[0]
                return x
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return evalTerm(env,env[x])
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Plus':
                x = children[0]
                f1 = evalTerm(env,x)
                x2 = children[1]
                f2 = evalTerm(env, x2)
                return int(f1)+ int(f2)



def evalFormula(env, e):
    if type(e)== Node:
        for label in e:
            children = e[label]
            if label == 'Variable':
                x = children[0]
                if x in env:
                    r = evalFormula(env,env[x])
                    if not r is None:
                        return r
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Not':
                x = children[0]
                f = evalFormula(env,x)
                return not f
            elif label == 'Or':
                x = children[0]
                f = evalFormula(env,x)
                if f:
                    return True
                else:
                    x2 = children[1]
                    f2 = evalFormula(env,x2)
                    return f2
            elif label == 'And':
                x = children[0]
                f = evalFormula(env,x)
                if not f:
                    return False
                else:
                    x2 = children[1]
                    f2 = evalFormula(env,x2)
                    return f2
    elif type(e) == Leaf:
        if e == 'True':
            return True
        if e == 'False':
            return False

def evalExpression(env, e): # Useful helper function.
    r = evalTerm(env,e)
    if not r is None:
        return r
    r = evalFormula(env,e)
    if not r is None:
        return r

def execProgram(env, s):
    if type(s) == Node:
        for label in s:
            if label == 'Print':
                children = s[label]
                f = children[0]
                p = children[1]
                v = evalExpression(env, f)
                (env, o) = execProgram(env, p)
                return (env,[v] + o)
            elif label == 'If':
                children = s[label]
                x = children[0]
                f = children[1]
                p = children[2]
                v = evalExpression(env, x)
                if v == True:
                    (env1, o1) = execProgram(env, f)
                    (env2, o2) = execProgram(env1, p)
                    return  (env2, o1+o2)
                else:
                    return execProgram(env, p)
            elif label == 'While':
                children = s[label]
                x = children[0]
                f = children[1]
                p = children[2]
                v = evalExpression(env, x)
                if v == False:
                    return execProgram(env, p)
                else:
                    (env1, o1) = execProgram(env , f)
                    (env2, o2) = execProgram(env1, s)
                    return (env2, o1+o2)
            elif label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                p1 = children[1]
                p2 = children[2]
                env[x] = p1
                (env2,o2) = execProgram(env, p2)
                return (env2,o2)
            elif label == 'Procedure':
                children = s[label]
                x = children[0]['Variable'][0]
                p1 = children[1]
                p2 = children[2]
                env[x] = p1
                (env2,o2) = execProgram(env, p2)
                return (env2,o2)
            elif label == 'Call':
                children = s[label]
                x = children[0]['Variable'][0]
                p2 = children[1]
                if not x in env:
                    print(x + " is unbound.")
                    exit()
                else:
                    p1 = env[x]
                    (env2, o1) = execProgram(env,p1)
                    (env3, o2) = execProgram(env2,p2)
                    return (env3, o1+o2)
    elif type(s) == Leaf:
        if s == 'End':
            return (env, [])
def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof
