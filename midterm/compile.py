#####################################################################
#
# CAS CS 320, Fall 2014
# Midterm (skeleton code)
# compile.py
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
#

from random import randint
exec(open('parse.py').read())
exec(open('analyze.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())

Leaf = str
Node = dict

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                n = children[0]
                return (['set ' + str(heap) + ' ' + str(n)], heap, heap+1)
            if label == 'Variable':
                x = children[0]
                address = env[x]
                return ([], address, heap)
            if label == 'Plus':
                x1 = children[0]
                x2 = children[1]
                (insts1, resultAddr1, heap2) = compileExpression(env, x1, heap)
                (insts2, resultAddr2, heap3) = compileExpression(env, x2, heap2)
                inst =  copy(resultAddr1,1)\
                        + copy(resultAddr2,2)\
                        +[\
                        'add']\
                       + copy(0, heap3)
                heap3 = heap3 + 1
                return (insts1 + insts2 + inst, heap3-1, heap3)
            if label == 'Array':
                x = children[0]['Variable'][0]
                e = children[1]
                (insts1, indexAddr, heap2) = compileExpression(env, e, heap)
                arrayAddr = env[x]
                insts = copy(indexAddr, 2)\
                     +['set 1 '+ str(arrayAddr),\
                       'add'\
                        ]\
                     + copyFromRef(0,heap2)
                return  (insts1 + insts, heap2, heap2+1)
    if type(e) == Leaf:
        if e == 'True':
            inst = ['set ' + str(heap) + ' 1']
            heap = heap + 1
            return (inst, heap -1, heap)
        if e == 'False':
            inst = ['set ' + str(heap) + ' 0']
            heap = heap + 1
            return (inst, heap -1, heap)


def compileProgram(env, s, heap = 8): # Set initial heap default address.
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e, p] = children
                (instsE, addr, heap) = compileExpression(env, e, heap)
                (env, instsP, heap) = compileProgram(env, p, heap)
                return (env, instsE + copy(addr, 5) + instsP, heap)
            if label == 'Assign':
                [v,e1,e2,e3,p] = children
                v = v['Variable'][0]
                (instsE1, addr1, heap1) = compileExpression(env, e1, heap)
                (instsE2, addr2, heap2) = compileExpression(env, e2, heap1)
                (instsE3, addr3, heap3) = compileExpression(env, e3, heap2)
                env[v] = heap3
                insts = copy(addr1, heap3)\
                    + copy(addr2, heap3+1)\
                    + copy(addr3, heap3+2)
                (env, instsP, heap4) = compileProgram(env, p, heap3+3)
                return (env, instsE1+ instsE2 +instsE3 + insts + instsP, heap4)


def compile(s):
    p = tokenizeAndParse(s)


    # Add call to type checking algorithm for Problem #4.
    r = typeProgram({},p)
    if r is None:
        return

    # Add calls to optimization algorithms for Problem #3.
    p2 = foldConstants(p)
    p3 = unrollLoops(p2)


    (env, insts, heap) = compileProgram({}, p3)
    return insts

def compileAndSimulate(s):
    return simulate(compile(s))

#eof
