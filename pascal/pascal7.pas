program TesteReais;
var
    a, b, c, d: real;
    x, y, z: real;
    resultado: real;
    i: integer;
begin
    writeln('=== Teste de Números Reais ===');
    
    { Teste de atribuições básicas }
    a := 3.14159;
    b := 2.71828;
    c := 0.0;
    d := -1.5;
    
    writeln('Valores iniciais:');
    writeln('a = ', a);
    writeln('b = ', b);
    writeln('c = ', c);
    writeln('d = ', d);
    writeln;
    
    { Teste de operações aritméticas básicas }
    writeln('=== Operações Aritméticas ===');
    
    resultado := a + b;
    writeln('Soma: ', a, ' + ', b, ' = ', resultado);
    
    resultado := a - b;
    writeln('Subtração: ', a, ' - ', b, ' = ', resultado);
    
    resultado := a * b;
    writeln('Multiplicação: ', a, ' * ', b, ' = ', resultado);
    
    resultado := a / b;
    writeln('Divisão: ', a, ' / ', b, ' = ', resultado);
    writeln;
    
    { Teste com números pequenos }
    writeln('=== Números Pequenos ===');
    x := 0.001;
    y := 0.002;
    z := x + y;
    writeln('0.001 + 0.002 = ', z);
    
    z := x * y;
    writeln('0.001 * 0.002 = ', z);
    writeln;
    
    { Teste com números grandes }
    writeln('=== Números Grandes ===');
    x := 12345.6789;
    y := 98765.4321;
    z := x + y;
    writeln('Soma grande: ', z);
    
    z := x - y;
    writeln('Subtração grande: ', z);
    writeln;
    
    { Teste de operações mistas (inteiro + real) }
    writeln('=== Operações Mistas ===');
    i := 5;
    x := 2.5;
    
    { Nota: Assumindo que seu compilador suporta conversão implícita }
    resultado := i + x;
    writeln('Inteiro + Real: 5 + 2.5 = ', resultado);
    
    resultado := i * x;
    writeln('Inteiro * Real: 5 * 2.5 = ', resultado);
    
    resultado := i / x;
    writeln('Inteiro / Real: 5 / 2.5 = ', resultado);
    writeln;
    
    { Teste de comparações }
    writeln('=== Comparações ===');
    
    a := 1.5;
    b := 2.5;
    
    if a < b then
        writeln('1.5 < 2.5 é verdadeiro');
    
    if a > 1.0 then
        writeln('1.5 > 1.0 é verdadeiro');
    
    if b >= 2.5 then
        writeln('2.5 >= 2.5 é verdadeiro');
    
    c := 1.5;
    if a = c then
        writeln('1.5 = 1.5 é verdadeiro');
    writeln;
    
    { Teste de expressões complexas }
    writeln('=== Expressões Complexas ===');
    
    a := 2.0;
    b := 3.0;
    c := 4.0;
    
    resultado := a + b * c;
    writeln('2.0 + 3.0 * 4.0 = ', resultado);
    
    resultado := (a + b) * c;
    writeln('(2.0 + 3.0) * 4.0 = ', resultado);
    
    resultado := a / b + c;
    writeln('2.0 / 3.0 + 4.0 = ', resultado);
    writeln;
    
    { Teste com zero }
    writeln('=== Teste com Zero ===');
    
    x := 0.0;
    y := 5.5;
    
    z := x + y;
    writeln('0.0 + 5.5 = ', z);
    
    z := x * y;
    writeln('0.0 * 5.5 = ', z);
    
    z := y - y;
    writeln('5.5 - 5.5 = ', z);
    writeln;
    
    { Teste com números negativos }
    writeln('=== Números Negativos ===');
    
    x := -3.7;
    y := 2.3;
    
    z := x + y;
    writeln('-3.7 + 2.3 = ', z);
    
    z := x * y;
    writeln('-3.7 * 2.3 = ', z);
    
    z := x / y;
    writeln('-3.7 / 2.3 = ', z);
    writeln;
    
    { Teste de acumulação em loop }
    writeln('=== Acumulação em Loop ===');
    
    x := 0.1;
    resultado := 0.0;
    
    for i := 1 to 10 do
    begin
        resultado := resultado + x;
        writeln('Passo ', i, ': soma = ', resultado);
    end;
    
    writeln('Soma final (deve ser ~1.0): ', resultado);
    writeln;
    
    { Teste de divisões específicas }
    writeln('=== Divisões Específicas ===');
    
    x := 22.0;
    y := 7.0;
    z := x / y;
    writeln('22.0 / 7.0 (aproximação de pi) = ', z);
    
    x := 1.0;
    y := 3.0;
    z := x / y;
    writeln('1.0 / 3.0 = ', z);
    
    x := 10.0;
    y := 3.0;
    z := x / y;
    writeln('10.0 / 3.0 = ', z);
    
    writeln('=== Fim dos Testes ===');
end.