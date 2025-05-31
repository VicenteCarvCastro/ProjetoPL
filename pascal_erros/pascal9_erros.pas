program Exemplo9;
function Dobro(n: integer): integer;
begin
Dobro := n * 2;
end;

var
res: integer;
begin
res := Dobro('dez');  { argumento inválido }
end.
