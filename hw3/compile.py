import random
exec(open("parse.py").read())
Node = dict
Leaf = str

def fresh():
    return str(random.randint(0,10000))

def compileTerm(env, t, heap):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Plus':
                 f1 = children[0]
                 f2 = children[1]
                 (insts1, resultAddr1, heap2) = compileTerm(env, f1, heap)
                 (insts2, resultAddr2, heap3) = compileTerm(env, f2, heap2)
                 inst = \
                        copy(resultAddr1,1)\
                        + copy(resultAddr2,2)\
                        +[\
                        'add']\
                        + copy(0, heap3)
                 heap3 = heap3 + 1
                 return (insts1 + insts2 + inst, heap3-1, heap3)
            if label == 'Number':
                f1 = children[0]
                inst = ['set ' + str(heap) + ' ' + str(f1)]
                heap = heap + 1
                return (inst, heap-1, heap)
            if label == 'Variable':
                f1 = children[0]
                address = env[f1]
                #inst = copy(address, heap)
               # heap = heap + 1
                return ([], address, heap)

def compileExpression(env,t,heap):
    r = compileFormula(env,t,heap)
    if not r is None:
        return r
    return compileTerm(env,t,heap)


def compileFormula(env, t, heap):
    if type(t) == Leaf:
        if t == 'True':
            inst = ['set ' + str(heap) + ' 1']
            heap = heap + 1
            return (inst, heap -1, heap)
        if t == 'False':
            inst = ['set ' + str(heap) + ' 0']
            heap = heap + 1
            return (inst, heap -1, heap)
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Variable':
                    f1 = children[0]
                    address = env[f1]
                    #inst = copy(address, heap)
                    #heap = heap + 1
                    return ([], address, heap)
            if label == 'Or':
                f1 = children[0]
                f2 = children[1]
                (insts1, resultAddr1, heap2) = compileFormula(env, f1, heap)
                (insts2, resultAddr2, heap3) = compileFormula(env, f2, heap2)
                fresh1 = fresh()
                fresh2 = fresh()
                inst = copy(str(resultAddr1),1)\
                    + copy(str(resultAddr2),2)\
                    +[\
                    "add",\
                    "branch setOneOr" + fresh1 + " 0",\
                    "goto finishOr" + fresh2 ,\
                    "label setOneOr" + fresh1,\
                    "set 0 1",\
                    "label finishOr" + fresh2,\
                    "set " +  str(heap3) + ' 0'\
                   ]\
                   + copy(0,str(heap3))
                heap3 = heap3 + 1
                return (insts1 + insts2 + inst, heap3-1, heap3)
            if label == 'Not':
                f = children[0]
                (insts1, resultAddr1, heap2) = compileFormula(env, f, heap)
                fresh1 = fresh()
                fresh2 = fresh()
                instsNot = \
                   ["branch setZeroNot" + fresh1 + " " + str(resultAddr1),\
                    "set " + str(resultAddr1) + " 1",\
                    "goto finishNot" + fresh2,\
                    "label setZeroNot" + fresh1 ,\
                    "set " + str(resultAddr1) + " 0",\
                    "label finishNot" + fresh2\
                   ]
                return (insts1 + instsNot, resultAddr1,heap2 )
            if label == 'And':
                f1 = children[0]
                f2 = children[1]
                (insts1, resultAddr1, heap2) = compileFormula(env, f1, heap)
                (insts2, resultAddr2, heap3) = compileFormula(env, f2, heap2)
                fresh1 = fresh()
                inst = copy(str(resultAddr1),0)\
                + copy(str(resultAddr2),1)\
                +[\
                'branch checkAnd' + fresh1 + ' 0',\
                'goto setAndZero'+fresh1,\
                'label checkAnd' + fresh1,\
                'branch setAndOne' + fresh1 + ' 1',\
                'label setAndZero'+fresh1,\
                'set ' + str(heap3) + ' 0',\
                'goto finishAnd'+ fresh1,\
                'label setAndOne' + fresh1,\
                'set ' + str(heap3) + ' 1',\
                'label finishAnd' + fresh1\
                ]
                heap = heap3 + 1
                return (insts1+insts2+inst,heap-1, heap)


def compileProgram(env,t,heap):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Print':
                exp = children[0]
                p = children[1]
                r = compileExpression(env,exp,heap)
                if r is None:
                    return
                (insts1, resultAddr1, heap2) = r
                inst = copy(str(resultAddr1),5)\

                k = compileProgram(env, p, heap2)
                if not k is None:
                    (env2,insts2, heap3) = k
                    return (env2,insts1+inst+insts2,heap3)
                return (env,insts1+inst,heap2)
            if label == 'Assign':
                var = children[0]['Variable'][0]
                exp = children[1]
                p = children[2]
                r = compileExpression(env,exp,heap)
                if r is None:
                    return
                (insts1, resultAddr1, heap2) = r
                if var not in env :
                    env[var] = resultAddr1
                else:
                    insts1+= copy(resultAddr1,env[var])
                k = compileProgram(env, p, heap2)
                if not k is None:
                    (env2,insts2, heap3) = k
                    return (env2,insts1+insts2,heap3)
                return (env,insts1,heap2)
            if label == 'If' :
                exp = children[0]
                p = children[1]
                rest = children[2]
                r = compileExpression(env,exp,heap)
                if r is None:
                    return
                (insts1, resultAddr1, heap2) = r
                k = compileProgram(env,p,heap2)
                if k is None:
                    return
                (env2,insts2, heap3)= k
                fresh1 = fresh()
                inst=[\
                    'branch checkIf' + fresh1 +' ' + str(resultAddr1),\
                    'goto finishIf' + fresh1,\
                    'label checkIf' + fresh1\
                    ]\
                    +insts2\
                    +['label finishIf' + fresh1]
                k = compileProgram(env2, rest, heap3)
                if not k is None:
                    (env3,insts3, heap4) = k
                    return (env3,insts1+inst+insts3,heap4)
                return (env2,insts1+inst,heap3)
            if label == 'While' :
                exp = children[0]
                p = children[1]
                rest = children[2]
                r = compileExpression(env,exp,heap)
                if r is None:
                    return
                (insts1, resultAddr1, heap2) = r
                k = compileProgram(env,p,heap2)
                if k is None:
                    return
                (env2,insts2, heap3)= k
                fresh1 = fresh()
                inst=[\
                    'label startWhile' +fresh1, \
                    'branch checkWhile' + fresh1 +' ' + str(resultAddr1),\
                    'goto finishWhile' + fresh1,\
                    'label checkWhile' + fresh1\
                    ]\
                    +insts2\
                    +[\
                    'goto startWhile' +fresh1, \
                    'label finishWhile' + fresh1\
                    ]
                k = compileProgram(env2, rest, heap3)
                if not k is None:
                    (env3,insts3, heap4) = k
                    return (env3,insts1+inst+insts3,heap4)
                return (env2,insts1+inst,heap3)
            if label == 'Procedure':
                var = children[0]['Variable'][0]
                body = children[1]
                rest = children[2]
                r = compileProgram(env,body,heap)
                if r is None:
                    insts1 = []
                    heap2 = heap
                else:
                    (env, insts1, heap2) = r
                inst = procedure(var,insts1)
                k = compileProgram(env, rest, heap2)
                if not k is None:
                    (env2,insts2, heap3) = k
                    return (env2,inst+insts2,heap3)
                return (env,inst,heap2)
            if label == 'Call':
                var = children[0]['Variable'][0]
                rest = children[1]
                inst = call(var)
                k = compileProgram(env, rest, heap)
                if not k is None:
                    (env2,insts2, heap2) = k
                    return (env2,inst+insts2,heap2)
                return (env,inst,heap)


def compile(s):
    global mem7Initialized
    mem7Initialized = False
    r = compileProgram({},tokenizeAndParse(s),8)
    if not r is None:
        (env, insts,heap) =r
        return insts