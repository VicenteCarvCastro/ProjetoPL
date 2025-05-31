program Exemplo11;
function Dobro(n: integer): integer;
begin
x := 5;         {x nao declarado}
Dobro := n * 2;
end;

var
res: integer;
begin
res := Dobro(x);  {aqui trata x como string}
end.
