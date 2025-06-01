program ArrayTest;
var
  a: array[1..5] of integer;
  i: integer;
begin
  for i := 1 to 5 do
  begin
    a[i] := i * 10; 
  end;
  writeln('Array elements:');
  for i := 1 to 5 do
  begin
    writeln('Element ', i, ': ', a[i]); 
  end;

end.
