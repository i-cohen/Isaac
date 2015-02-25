import parse, interpret, compile, analyze

def check(name, function, inputs_result_pairs):
    def str_(s): return '"'+str(s)+'"' if type(s) == str else str(s)
    if type(name) == tuple:
        prefix = name[0]
        suffix = name[1]
    if type(name) == str:
        prefix = name + '('
        suffix = ')'

    passed = 0
    for (inputs, result) in inputs_result_pairs:
        try:
            if len(inputs) == 1:
                output = function(inputs[0])
            if len(inputs) == 2:
                output = function(inputs[0], inputs[1])
            if len(inputs) == 3:
                output = function(inputs[0], inputs[1], inputs[2])
        except:
            output = None

        if output == result: passed = passed + 1
        else: print("\n  Failed on:\n    "+prefix+', '.join([str_(i) for i in inputs])+suffix+"\n\n"+"  Should be:\n    "+str(result)+"\n\n"+"  Returned:\n    "+str(output)+"\n")
    print("Passed " + str(passed) + " of " + str(len(inputs_result_pairs)) + " tests.")
    print("")

print("Problem #1, tokenizeAndParse()...")
try: parse.tokenizeAndParse
except: print("The tokenizeAndParse() function is not defined.")
else: check('program', parse.tokenizeAndParse, [\
    (["print true ;"], ({'Print': ['True', 'End']})),\
    (["print 5 ;"], ({'Print': [{'Number': [5]}, 'End']})),\
    (['assign a := [1+2,4,6]; print @ a [ 0 ] ; for a {print true ;}'], ({'Assign':[{'Variable':['a']}, {'Plus':[{'Number':[1]},{'Number':[2]}]}, {'Number':[4]}, {'Number':[6]},{'Print': [{'Array': [{'Variable':['a']},{'Number':[0]}]}, {'For': [{'Variable':['a']},{'Print': ['True', 'End']},'End']} ]} ]}))
    ])

print("Problem #2, interpret...")
try: interpret.interpret
except: print("The interpret() function is not defined.")
else: check('interpret', interpret.interpret, [\
    (["print 123;"], [123]),\
    (["print false; print true; print 4;"], [False, True, 4]),\
    (["assign a := [1+2,4,6]; print @ a [0]; print @ a[1]; print @ a[2] ;"], [3,4,6]),\
    (["for x {print true;}"], [True, True, True]),\
    (["for x {print x;}"], [0, 1, 2]),\
    (["assign a := [1+2,4,6]; for x { print @ a[x] + @ a[x] ;}"], [6,8,12]),\
    (["assign x := [3,4,5]; assign y := [10,11,12]; for z {print @ x[z] + @ y[z]; print 2;} print true; print false;"], [13,2,15,2,17,2,True,False]),\
    (["for a {print true; for b{print false;}}"],[True,False,False,False,True,False,False,False,True,False,False,False]),\
    (["assign a := [1,2,true]; print @ a[1];"], None )
    ])

print("Problem #3, compile...")
try: compile.compileAndSimulate
except: print("The compile() function is not defined.")
else: check('compile', compile.compileAndSimulate, [\
    (["print 123;"], [123]),\
    (["print false; print true; print 4;"], [False, True, 4]),\
    (["assign a := [1+2,4,6]; print @ a [0]; print @ a[1]; print @ a[2] ;"], [3,4,6]),\
    (["for x {print true;}"], [1, True, True]),\
    (["for x {print x;}"], [0, 1, 2]),\
    (["assign a := [1+2,4,6]; for x { print @ a[x] + @ a[x] ;}"], [6,8,12]),\
    (["assign x := [3,4,5]; assign y := [10,11,12]; for z {print @ x[z] + @ y[z]; print 2;} print true; print false;"], [13,2,15,2,17,2,1,False]),\
    (["for a {print true; for b{print false;}}"],[True,False,False,False,True,False,False,False,True,False,False,False]),\
    (["assign a:= [4,5,6]; for b {print @ a[0]; assign a := [8,5,6];} print @ a[0];print @ a[1];"],[4,8,8,8,5]),\
    #(["assign a := [2,2,2]; for c { print @ a[2]; assign a [false, false, false];} print @ a[2]; "],[2,False, False, False]),\
    (["assign a := [1,2,true];"], None)
    ])

print("Problem #4, Analyze...")
try: analyze.helper
except: print("The compile() function is not defined.")
else: check('analyze', analyze.helper, [\
    (["print 123;"], 'Void'),\
    (["print false; print true; print 4;"], 'Void'),\
    (["assign a := [1+2,4,6]; print @ a [0]; print @ a[1]; print @ a[2] ;"], 'Void'),\
    (["for x {print true;}"], 'Void'),\
    (["for x {print x;}"], 'Void'),\
    (["assign a := [1+2,4,6]; for x { print @ a[x] + @ a[x] ;}"], 'Void'),\
    (["assign x := [3,4,5]; assign y := [10,11,12]; for z {print @ x[z] + @ y[z];} print true; print false;"], 'Void'),\
    (["assign a := [1,2,true];"], None),\
    (["print true + true;"], None),\
    (["assign a := [1,2,3]; print @ a[true];"], None),\
    ])
