JUMP MAIN  // Salta para o início do programa
MAIN:
START   // Início do programa
PUSHS "=== Teste de Números Reais ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHF 3.14159     // Push valor 3.14159
STOREG 0     // Armazena a no endereço 0
PUSHF 2.71828     // Push valor 2.71828
STOREG 1     // Armazena b no endereço 1
PUSHF 0.0     // Push valor 0.0
STOREG 2     // Armazena c no endereço 2
PUSHI 0     // Push zero
PUSHF 1.5     // Push valor 1.5
FSUB     // Subtração para negativo
STOREG 3     // Armazena d no endereço 3
PUSHS "Valores iniciais:"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHS "a = "     // Push String
WRITES     // Imprime string
PUSHG 0    // Empilha endereço de a
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHS "b = "     // Push String
WRITES     // Imprime string
PUSHG 1    // Empilha endereço de b
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHS "c = "     // Push String
WRITES     // Imprime string
PUSHG 2    // Empilha endereço de c
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHS "d = "     // Push String
WRITES     // Imprime string
PUSHG 3    // Empilha endereço de d
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
WRITELN     // Imprime nova linha
PUSHS "=== Operações Aritméticas ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHG 0     // Empilha endreço de a
PUSHG 1     // Empilha endreço de b
FADD     // Soma de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "Soma: "     // Push String
WRITES     // Imprime string
PUSHG 0    // Empilha endereço de a
WRITEF     // Imprime float
PUSHS " + "     // Push String
WRITES     // Imprime string
PUSHG 1    // Empilha endereço de b
WRITEF     // Imprime float
PUSHS " = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 0     // Empilha endreço de a
PUSHG 1     // Empilha endreço de b
FSUB     // Subtração de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "Subtração: "     // Push String
WRITES     // Imprime string
PUSHG 0    // Empilha endereço de a
WRITEF     // Imprime float
PUSHS " - "     // Push String
WRITES     // Imprime string
PUSHG 1    // Empilha endereço de b
WRITEF     // Imprime float
PUSHS " = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 0     // Empilha endreço de a
PUSHG 1     // Empilha endreço de b
FMUL     // Multiplicação de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "Multiplicação: "     // Push String
WRITES     // Imprime string
PUSHG 0    // Empilha endereço de a
WRITEF     // Imprime float
PUSHS " * "     // Push String
WRITES     // Imprime string
PUSHG 1    // Empilha endereço de b
WRITEF     // Imprime float
PUSHS " = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 0     // Empilha endreço de a
PUSHG 1     // Empilha endreço de b
FDIV     // Divisão real de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "Divisão: "     // Push String
WRITES     // Imprime string
PUSHG 0    // Empilha endereço de a
WRITEF     // Imprime float
PUSHS " / "     // Push String
WRITES     // Imprime string
PUSHG 1    // Empilha endereço de b
WRITEF     // Imprime float
PUSHS " = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
WRITELN     // Imprime nova linha
PUSHS "=== Números Pequenos ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHF 0.001     // Push valor 0.001
STOREG 4     // Armazena x no endereço 4
PUSHF 0.002     // Push valor 0.002
STOREG 5     // Armazena y no endereço 5
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FADD     // Soma de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "0.001 + 0.002 = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FMUL     // Multiplicação de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "0.001 * 0.002 = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
WRITELN     // Imprime nova linha
PUSHS "=== Números Grandes ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHF 12345.6789     // Push valor 12345.6789
STOREG 4     // Armazena x no endereço 4
PUSHF 98765.4321     // Push valor 98765.4321
STOREG 5     // Armazena y no endereço 5
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FADD     // Soma de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "Soma grande: "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FSUB     // Subtração de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "Subtração grande: "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
WRITELN     // Imprime nova linha
PUSHS "=== Operações Mistas ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHI 5     // Push valor 5
STOREG 8     // Armazena i no endereço 8
PUSHF 2.5     // Push valor 2.5
STOREG 4     // Armazena x no endereço 4
PUSHG 8     // Empilha endreço de i
PUSHG 4     // Empilha endreço de x
FADD     // Soma de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "Inteiro + Real: 5 + 2.5 = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 8     // Empilha endreço de i
PUSHG 4     // Empilha endreço de x
FMUL     // Multiplicação de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "Inteiro * Real: 5 * 2.5 = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 8     // Empilha endreço de i
PUSHG 4     // Empilha endreço de x
FDIV     // Divisão real de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "Inteiro / Real: 5 / 2.5 = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
WRITELN     // Imprime nova linha
PUSHS "=== Comparações ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHF 1.5     // Push valor 1.5
STOREG 0     // Armazena a no endereço 0
PUSHF 2.5     // Push valor 2.5
STOREG 1     // Armazena b no endereço 1
PUSHG 0     // Empilha endreço de a
PUSHG 1     // Empilha endreço de b
FINF     // Menor
JZ ELSE0  // Salta para a label de else
PUSHS "1.5 < 2.5 é verdadeiro"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
JUMP FIM1  // Salta para o final da Label
ELSE0:    // Label ELSE0
FIM1:    // Label FIM1
PUSHG 0     // Empilha endreço de a
PUSHF 1.0     // Push valor 1.0
FSUP     // Maior
JZ ELSE2  // Salta para a label de else
PUSHS "1.5 > 1.0 é verdadeiro"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
JUMP FIM3  // Salta para o final da Label
ELSE2:    // Label ELSE2
FIM3:    // Label FIM3
PUSHG 1     // Empilha endreço de b
PUSHF 2.5     // Push valor 2.5
FSUPEQ     // Maior ou Igual
JZ ELSE4  // Salta para a label de else
PUSHS "2.5 >= 2.5 é verdadeiro"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
JUMP FIM5  // Salta para o final da Label
ELSE4:    // Label ELSE4
FIM5:    // Label FIM5
PUSHF 1.5     // Push valor 1.5
STOREG 2     // Armazena c no endereço 2
PUSHG 0     // Empilha endreço de a
PUSHG 2     // Empilha endreço de c
EQUAL     // Igual
JZ ELSE6  // Salta para a label de else
PUSHS "1.5 = 1.5 é verdadeiro"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
JUMP FIM7  // Salta para o final da Label
ELSE6:    // Label ELSE6
FIM7:    // Label FIM7
WRITELN     // Imprime nova linha
PUSHS "=== Expressões Complexas ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHF 2.0     // Push valor 2.0
STOREG 0     // Armazena a no endereço 0
PUSHF 3.0     // Push valor 3.0
STOREG 1     // Armazena b no endereço 1
PUSHF 4.0     // Push valor 4.0
STOREG 2     // Armazena c no endereço 2
PUSHG 0     // Empilha endreço de a
PUSHG 1     // Empilha endreço de b
PUSHG 2     // Empilha endreço de c
FMUL     // Multiplicação de dois valores
FADD     // Soma de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "2.0 + 3.0 * 4.0 = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 0     // Empilha endreço de a
PUSHG 1     // Empilha endreço de b
FADD     // Soma de dois valores
PUSHG 2     // Empilha endreço de c
FMUL     // Multiplicação de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "(2.0 + 3.0) * 4.0 = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 0     // Empilha endreço de a
PUSHG 1     // Empilha endreço de b
FDIV     // Divisão real de dois valores
PUSHG 2     // Empilha endreço de c
FADD     // Soma de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "2.0 / 3.0 + 4.0 = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
WRITELN     // Imprime nova linha
PUSHS "=== Teste com Zero ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHF 0.0     // Push valor 0.0
STOREG 4     // Armazena x no endereço 4
PUSHF 5.5     // Push valor 5.5
STOREG 5     // Armazena y no endereço 5
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FADD     // Soma de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "0.0 + 5.5 = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FMUL     // Multiplicação de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "0.0 * 5.5 = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 5     // Empilha endreço de y
PUSHG 5     // Empilha endreço de y
FSUB     // Subtração de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "5.5 - 5.5 = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
WRITELN     // Imprime nova linha
PUSHS "=== Números Negativos ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHI 0     // Push zero
PUSHF 3.7     // Push valor 3.7
FSUB     // Subtração para negativo
STOREG 4     // Armazena x no endereço 4
PUSHF 2.3     // Push valor 2.3
STOREG 5     // Armazena y no endereço 5
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FADD     // Soma de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "-3.7 + 2.3 = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FMUL     // Multiplicação de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "-3.7 * 2.3 = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FDIV     // Divisão real de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "-3.7 / 2.3 = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
WRITELN     // Imprime nova linha
PUSHS "=== Acumulação em Loop ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHF 0.1     // Push valor 0.1
STOREG 4     // Armazena x no endereço 4
PUSHF 0.0     // Push valor 0.0
STOREG 7     // Armazena resultado no endereço 7
PUSHI 1     // Push valor 1
STOREG 8  // 2Armazena i no endereço 8
FORINICIO8:    // Label FORINICIO8
PUSHG 8    // Empilha indice
PUSHI 10     // Push valor 10
FSUP    // Verifica se o indice é maior que o limite superior
NOT   // Negação
JZ FORFIM9   // Se condição for falsa, salta para o fim do loop
PUSHG 7     // Empilha endreço de resultado
PUSHG 4     // Empilha endreço de x
FADD     // Soma de dois valores
STOREG 7     // Armazena resultado no endereço 7
PUSHS "Passo "     // Push String
WRITES     // Imprime string
PUSHG 8    // Empilha endereço de i
WRITEI     // Imprime inteiro
PUSHS ": soma = "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHG 8 // Empilha indice
PUSHI 1   // Empilha 1
FADD  // Incrementa indice
STOREG 8  // Armazena novo valor na variável
JUMP FORINICIO8   // Salta para o início do loop
FORFIM9:    // Label FORFIM9
PUSHS "Soma final (deve ser ~1.0): "     // Push String
WRITES     // Imprime string
PUSHG 7    // Empilha endereço de resultado
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
WRITELN     // Imprime nova linha
PUSHS "=== Divisões Específicas ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHF 22.0     // Push valor 22.0
STOREG 4     // Armazena x no endereço 4
PUSHF 7.0     // Push valor 7.0
STOREG 5     // Armazena y no endereço 5
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FDIV     // Divisão real de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "22.0 / 7.0 (aproximação de pi) = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHF 1.0     // Push valor 1.0
STOREG 4     // Armazena x no endereço 4
PUSHF 3.0     // Push valor 3.0
STOREG 5     // Armazena y no endereço 5
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FDIV     // Divisão real de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "1.0 / 3.0 = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHF 10.0     // Push valor 10.0
STOREG 4     // Armazena x no endereço 4
PUSHF 3.0     // Push valor 3.0
STOREG 5     // Armazena y no endereço 5
PUSHG 4     // Empilha endreço de x
PUSHG 5     // Empilha endreço de y
FDIV     // Divisão real de dois valores
STOREG 6     // Armazena z no endereço 6
PUSHS "10.0 / 3.0 = "     // Push String
WRITES     // Imprime string
PUSHG 6    // Empilha endereço de z
WRITEF     // Imprime float
WRITELN     // Imprime nova linha
PUSHS "=== Fim dos Testes ==="     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
STOP   // Fim do programa
