import re


def variable(tokens, top = True):
    if re.match(r"([a-z][A-Z]*)", tokens[0]):
            if not top or len(tokens) == 1:
                return (tokens[0], tokens[1:])
    else: return None


def number(tokens, top = True):
    if re.match(r"^(-?[0-9]\d*)$", tokens[0]):
        if not top or len(tokens) == 1:
            return (int(tokens[0]), tokens[1:])
    else: return None

def expression(tmp, top = True):
    r = formula(tmp,False)
    if not r is None:
        (e1, tokens)= r
        if tokens[0]==';' or tokens[0]=='{':
            if not top or len(tokens) == 0:
                 return  (e1, tokens)
    r = term(tmp,False)
    if not r is None:
        (e1, tokens)= r
        if tokens[0]==';' or tokens[0]=='{' or tokens[0]== '}':
            if not top or len(tokens) == 0:
                 return  (e1, tokens)
    return None

def variableWithTree(tokens,top):
    r = variable(tokens, top)
    if not r is None:
        (e1, tokens)= r
        if not top or len(tokens) == 0:
            return ({'Variable':[e1]}, tokens)


def program (tmp, top = True):
    seqs = [\
        ('Print', [ 'print', expression,';', program]), \
        ('Assign', [ 'assign', variableWithTree ,':=',expression,';', program]), \
        ('If', ['if' ,expression,'{',program,'}',program]),\
        ('While',['while',expression,'{',program,'}',program]),\
        ('End',[])\
        ]
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.
        for x in seq:
            if len(tokens)==0:
                es = es + ['End']
                break
            elif type(x) == type(""): # Terminal.
                if tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)
    if len(tokens)==0:
        return ('', tokens[1:])
    return None

def leftTerm(tmp, top = True):
    r = term(tmp, False)
    if not r is None:
        (e1, tokens)=r
        if tokens[0]=='==' or tokens[0]=='<':
            if not top or len(tokens) == 0:
             return  (e1, tokens)

def formula(tmp, top = True):
    seqs = [\
        ('Xor', [ leftFormula, 'xor', formula]), \
        ('Equals', [leftFormula, '==', formula]),\
        ('Equals',[leftTerm, '==', factor]),\
        ('LessThan',[leftTerm, '<', factor])\
        ]
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.
        for x in seq:
            if len(tokens)== 0:
                break
            if type(x) == type(""): # Terminal.
                if tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)
    r = leftFormula(tmp,False)
    if not r is None:
        (e1, tokens)= r
        if not top or len(tokens) == 0:
             return  (e1, tokens)
    return None

def leftFactor (tmp, top= True):
    seqs = [\
        ('Log', [ 'log','(', term, ')']), \
        ('Parens', [ '(', term, ')']), \
        ('Variable', [variable]),\
        ('Number',[number])
        ]
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.
        for x in seq:
            if len(tokens)== 0:
                break
            if type(x) == type(""): # Terminal.
                if tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)
    return None





def factor(tmp, top = True):
    seqs = [\
        ('Mult', [ leftFactor, '*', factor]), \
        ]
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.
        for x in seq:
            if len(tokens)== 0:
                break
            if type(x) == type(""): # Terminal.
                if tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)
    r = leftFactor(tmp,False)
    if not r is None:
        (e1, tokens)= r
        if not top or len(tokens) == 0:
             return  (e1, tokens)
    return None


def term(tmp, top = True):
    seqs = [\
        ('Plus', [ factor, '+', term]), \
        ]
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.
        for x in seq:
            if len(tokens)== 0:
                break
            if type(x) == type(""): # Terminal.
                if tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.
            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)
    r = factor(tmp,False)
    if not r is None:
        (e1, tokens)= r
        if not top or len(tokens) == 0:
             return  (e1, tokens)
    return None


def leftFormula(tmp, top = True):
    seqs = [\
        ('True', ['true']), \
        ('False', ['false']), \
        ('Not', ['not', '(', formula, ')']), \
        ('Parens', ['(', formula, ')']), \
        ('Variable',[variable])
        ]

    # Try each choice sequence.
    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = [] # To store matched terminals.
        es = [] # To collect parse trees from recursive calls.

        for x in seq:
            if type(x) == type(""): # Terminal.

                if tokens[0] == x: # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                # Call parsing function recursively
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        # Check that we got either a matched token
        # or a parse tree for each sequence entry.
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)