program IfTest;
var
  x, y: integer;
begin
  x := 10;
  y := 0;
  if x > 5 then
    y := 1
  else
    y := 2;
    writeln('Value of y: ', y);
end.