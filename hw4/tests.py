import interpret
import parse

print(interpret.subst({'x': {'Number': [5]}},{'Variable': ['x']}))
print(interpret.subst({"y":{"Number":[2]}}, {"Plus":[{"Variable":['y']}, {"Variable":['y']}]}))
print(interpret.subst({"a":{"Number":[1]}, "b":{"Number":[2]}}, {"Mult":[{"Variable":['y']}, {"Variable":['y']}]}))



constantParserd= parse.parser(parse.grammar,"declaration")
m=constantParserd("new(Node t1 t2) = NewNode new(t1) new(t2); new(Leaf) = NewLeaf;")
print(m)
constantParsers= parse.parser(parse.grammar,"expression")
e= constantParsers("new(Node Leaf Leaf)")
print(e)
print(interpret.evaluate(interpret.build({},m),{},e))

#interpret.interact("new(Node t1 t2) = NewNode new(t1) new(t2); new(Leaf) = NewLeaf; new(Tree) = NewNode NewLeaf NewLeaf;f(x) = x+x;")


count=0
for x in range(0,10000):
    if (x % 3 is 0) or (x % 5 is 0) or (x % 7 is 0):
        count+=1
print(count)