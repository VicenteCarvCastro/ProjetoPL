program ArithmeticTest;
var
    a, b, c, d, e: integer;
    x, y: real;
begin
    a := 10;
    b := 5;
    c := a + b * 2;
    writeln('Integer arithmetic: ', c);
    
    x := 3.14;
    y := 2.0;
    x := x * y + 1.5;
    writeln('Real arithmetic: ', x);
    
    d := a div b;
    writeln('Division: ', a div b);
    writeln('Modulo: ', a mod b);
    writeln('Subtraction: ', a - b);
end.
