program BinarioParaInteiro;

function BinToInt(bin: string): integer; 
var
i, valor, potencia: integer;
begin
valor := 0;
potencia := 1;
for i := length(bin) downto 1 do   {funcao length nao declarada}
begin
if bin[i] = '1' then
valor := valor + potencia;
potencia := potencia * 2;
end;
BinToInt := valor; {BinToInt recebe int em vez de string}
end;

var
bin: string;
valor: integer;
begin
writeln('Introduza uma string binária:');
readln(bin);
valor := BinToInt(123);           
resultado := BinToInt(bin);     {resultado nao declarado}    
bin[true] := '0';         { indice de bin deve ser inteiro mas e boolean}      
writeln('Resultado: ', resultado);
end.
