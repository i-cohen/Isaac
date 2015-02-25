#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 4 (skeleton code)
# interpret.py
#

exec(open("parse.py").read())

def subst(s, a ):
    if type(a) == dict:
        for label in a:
            children = a[label]
            if label == 'Variable':
                var = children[0]
                if var in s:
                    sub = s[var]
                    return sub
                return {'Variable': [var]}

            else:
                newChildren = []
                for x in children:
                    newChildren +=[subst(s,x)]
                return {label: newChildren}


    pass # Complete for Problem #1, part (a).

def unify(a, b):
    if(type(a) == dict):
        for label in a:
                children = a[label]
                if label== 'Variable':
                    var = children[0]
                    return {var: b}
    if(type(b) == dict):
        for label in b:
                children = b[label]
                if label== 'Variable':
                    var = children[0]
                    return {var: a}
    if type(a) == type(b):
        if type(a) == dict:
            for label in a:
                children = a[label]
                if label== 'Variable':
                    var = children[0]
                    return {var: b}
                elif label in b:
                    bchildren = b[label]
                    if len(bchildren) != len(children):
                        return None
                    s={}
                    for x in range(0,len(children)):
                        result =unify(children[x], bchildren[x])
                        if result == None:
                            return None
                        s.update(result)
                    return s
                else:
                    return None
        if a == b:
            return {}
        else:
             return None

    else:
        return None
    pass # Complete for Problem #1, part (b).

def build(m, d):
    if type(d)== dict:
        for label in d:
            children = d[label]
            if label == 'Function':
                var = children[0]['Variable'][0]
                p = children[1]
                e = children[2]
                d2 = children[3]
                if var in m:
                    m[var] += [(p,e)]
                    return build(m,d2)
                else:
                    m[var] = [(p,e)]
                    return build(m,d2)
    if type(d) == str:
        if d == 'End':
            return m

    pass # Complete for Problem #2, part (a).

def evaluate(m, env, e):
    if type(e) == dict:
        for label in e:
            children = e[label]
            if label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == 'Number':
                x = children[0]
                return int(x)
            elif label == 'Plus':
                x = children[0]
                f1 = evaluate(m,env,x)
                x2 = children[1]
                f2 = evaluate(m,env, x2)
                return int(f1)+ int(f2)
            elif label == 'Apply':
                var = children[0]['Variable'][0]
                e1 = evaluate(m,env,children[1])
                for (p,e2) in m[var]:
                    u =  unify(p,e1)
                    if u is not None :
                        if u == {}:
                            return evaluate(m,env,e2)
                        else:
                            env.update(u)
                            return evaluate(m,env,e2)
            elif label == "ConBase":
                return e
            elif label == "ConInd":
                tmp =[]
                for x in children:
                    tmp+= [evaluate(m,env,x)]
                return {label: tmp}
    if type(e) == str:
        return e
    # Complete for Problem #2, part (b).

def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))
    print(m)
    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ')
        if s == ':quit':
            break

        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

#eof