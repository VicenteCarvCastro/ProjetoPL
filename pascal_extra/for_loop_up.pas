program ForLoopAsc;
var
  i, product: integer;
begin
  product := 1;
  for i := 1 to 4 do product := product * i;
  writeln('Product of numbers from 1 to 4 is: ', product);
end.
