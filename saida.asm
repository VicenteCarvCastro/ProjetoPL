START   // Início do programa
PUSHS "Introduza um número inteiro positivo:"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
READ  // Le string do input
ATOI     // Converte string para inteiro
STOREG 0     // Armazena num no endereço 0
PUSHI 1     // Push True
STOREG 2     // Armazena primo no endereço 2
PUSHI 2     // Push valor 2
STOREG 1     // Armazena i no endereço 1
WHILEINICIO0:    // Label WHILEINICIO0
PUSHG 1     // Empilha endreço de i
PUSHG 0     // Empilha endreço de num
PUSHI 2     // Push valor 2
DIV     // Divisão de dois valores
INFEQ     // Menor ou Igual
PUSHG 2     // Empilha endreço de primo
AND     // E lógico
JZ WHILEFIM1     // Se condição for falsa, salta para o fim do loop
PUSHG 0     // Empilha endreço de num
PUSHG 1     // Empilha endreço de i
MOD     // Módulo de dois valores
PUSHI 0     // Push valor 0
EQUAL     // Igual
JZ ELSE2  // Salta para a label de else
PUSHI 0     // Push False
STOREG 2     // Armazena primo no endereço 2
JUMP FIM3  // Salta para o final da Label
ELSE2:    // Label ELSE2
FIM3:    // Label FIM3
PUSHG 1     // Empilha endreço de i
PUSHI 1     // Push valor 1
ADD     // Soma de dois valores
STOREG 1     // Armazena i no endereço 1
JUMP WHILEINICIO0     // Jump para WHILEINICIO0
WHILEFIM1:    // Label WHILEFIM1
PUSHG 2     // Empilha endreço de primo
JZ ELSE4  // Salta para a label de else
PUSHG 0    // Empilha endereço de num
WRITEI     // Imprime inteiro
PUSHS " é um número primo"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
JUMP FIM5  // Salta para o final da Label
ELSE4:    // Label ELSE4
PUSHG 0    // Empilha endereço de num
WRITEI     // Imprime inteiro
PUSHS " não é um número primo"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
FIM5:    // Label FIM5
STOP   // Fim do programa
