import interpret, machine,parse
import os



print(machine.fresh())
print(machine.fresh())
print(interpret.interpret("procedure g {print 2;} procedure f {if true and true { call g; }} call g; call f;"))
print(machine.simulate([\
    'set 10 4',\
    'set 3 6',\
    'set 4 2',\
    'copy']))
# print(simulate(
#     [\
#     'label name',\
#     'set 20 35'\
#     ]\
#     +call('name')\
#     +call('name')))

body ="procedure h {print 3;} procedure g {print 2; call h; call h;} procedure f {call g; print 1; call g;} call f;"
x=parse.tokenizeAndParse(body)
print (x)
insts = machine.compile(body)
print(insts)
print(machine.simulate(insts))