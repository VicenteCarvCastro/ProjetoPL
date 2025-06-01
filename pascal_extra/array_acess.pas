program ArrayTest;
var
  a: array[1..5] of integer;
  i: integer;
begin
  for i := 1 to 5 do
    a[i] := i * i;
end.
