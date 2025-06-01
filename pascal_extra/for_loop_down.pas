program ForLoopDesc;
var
  i, sum: integer;
begin
  sum := 0;
  for i := 5 downto 1 do
    sum := sum + i;
    writeln('Sum from 5 to 1 is: ', sum);
end.
