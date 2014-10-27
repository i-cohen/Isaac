import parse,interpret


print(parse.program(['if', 'true', '{', 'print', '1', ';', '}']))
print(parse.number('10', False))
print(interpret.interpret('assign x := true; assign y := true; assign z:= 10; assign a := -1; while x==y{ if z<1{assign y := false;} print z; assign z:= z + a ;} print x; print y;'))
print(interpret.interpret('assign x:= 0; while not(x < 1){print x; assign x:= x+0;} print false; '))
print(interpret.interpret('print 3 == 3;'))
