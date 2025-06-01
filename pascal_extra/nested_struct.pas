program NestedControl;
var
  i, j, count: integer;
begin
  count := 0;
  for i := 1 to 3 do
    for j := 1 to 2 do
      if (i + j) mod 2 = 0 then
        count := count + 1;
    writeln('Count of even sums: ', count);
end.
