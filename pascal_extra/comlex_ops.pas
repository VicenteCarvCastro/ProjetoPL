program ExpressionTest;
var
    a, b, c, d: integer;

    x: real;
begin
    a := 2;
    b := 3;
    c := 4;
    d := 5;

    { Mixed arithmetic }
    x := a / b + c;
    writeln('2 / 3 + 4 = ', x);
    
    { Boolean expressions }
    if (a < b) and (c > d) or (a = 2) then
        writeln('Complex boolean expression is true');
end.