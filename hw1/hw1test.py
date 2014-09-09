import hw1
import json

hw1.tokenize(["red", "blue", "#"], "red#red blue# red#blue")
(tree,tokens)= hw1.directions(hw1.tokenize(
               ["forward","reverse","left","right","turn","stop",";"],
               "forward; forward; forward; right turn; reverse; forward; stop;"
              ))
print(tree, tokens)

print(hw1.variable(['123', 'foo', 'bar']))