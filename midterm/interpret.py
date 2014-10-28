#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# interpret.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def evaluate(env, e):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            if label == 'Number':
                x = children[0]
                return x
            elif label == 'Plus':
                x = children[0]
                f1 = evaluate(env,x)
                x2 = children[1]
                f2 = evaluate(env, x2)
                return int(f1)+ int(f2)
            elif label == 'Array':
                var = children[0]['Variable'][0]
                i = children[1]
                index = evaluate(env,i)
                if int(index) >3 or int(index) < 0:
                    print("Index out of bounds")
                    exit()
                array = env[var]
                return int(array[index])
    elif type(e) == Leaf:
        if e == 'True':
            return True
        if e == 'False':
            return False
    # Complete for Problem #2.

def execute(env, s):
    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                f = children[0]
                p = children[1]
                v = evaluate(env, f)
                (env, o) = execute(env, p)
                return (env,[v] + o)
            if label == 'Assign':
                var = children[0]['Variable'][0]
                v1 = children[1]
                v2 = children[2]
                v3 = children[3]
                p = children[4]
                var1 = evaluate(env,v1)
                var2 = evaluate(env,v2)
                var3 = evaluate(env,v3)
                env[var] = [var1,var2,var3]
                (env1,o1) = execute(env, p)
                return (env1,o1)
            if label == 'For':
                var = children[0]['Variable'][0]
                body = children[1]
                rest = children[2]
                tmp = env.copy()
                tmp[var] = 0
                (env1,o1) = execute(tmp, body)
                tmp[var] = 1
                (env2,o2) = execute(tmp, body)
                tmp[var] = 2
                (env3,o3) = execute(tmp, body)
                (env4, o4) = execute(env, rest)
                return (env4, o1+o2+o3+o4)

    elif type(s) == Leaf:
        if s == 'End':
            return (env, [])
     # Complete for Problem #2.

def interpret(s):
    r = tokenizeAndParse(s)
    if not r is None:
        r = execute({}, r )
        if not r is None:
            (env, o) = r
            return o
    pass # Complete for Problem #2.

#eof
