import hw1
import json
import re

hw1.tokenize(["red", "blue", "#"], "red#red blue# red#blue")
(tree,tokens)= hw1.directions(hw1.tokenize(
               ["forward","reverse","left","right","turn","stop",";"],
               "forward; forward; forward; right turn; reverse; forward; stop;"
              ))
print(tree, tokens)

print(hw1.variable(['123', 'foo', 'bar']))

print ([t for t in re.split(r"(\s+|token)", "tokentoken")])

print (hw1.formula(['less','than','(','log', '(', 'mult', '(', '#', '2', ',', '#', '3', ')', ')', ',','#','3',')']))

print(hw1.complete("end ;"))

print(hw1.complete("assign @y := #100; assign @x := plus(mult(log(@y),#20),#30); print and(less than(@x, @y), or(equal(@y, #200), false)); end;"))
print(hw1.complete("print ( # 2 + @ x ) ; end ;"))
print(hw1.complete("print (#2 * @x) ; end ;"))
print(hw1.complete('print not(true); assign @y := #10; print (log(#4) + @y); assign @x := #123; print (@x == @y); end;'))