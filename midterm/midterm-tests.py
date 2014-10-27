import parse

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
    (["print true ;"], ({'Print': ['True', 'End']}, [])),\
    ])

