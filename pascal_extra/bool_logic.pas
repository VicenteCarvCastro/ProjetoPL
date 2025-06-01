program BooleanLogic;
var
  a, b, c: boolean;
begin
  a := true;
  b := false;
  c := (a or b) and not (a and b);
end.
