JUMP MAIN  // Salta para o início do programa
MAIN:
START   // Início do programa
PUSHS "Introduza o primeiro número: "     // Push String
WRITES     // Imprime string
READ  // Le string do input
ATOI     // Converte string para inteiro
STOREG 0     // Armazena num1 no endereço 0
PUSHS "Introduza o segundo número: "     // Push String
WRITES     // Imprime string
READ  // Le string do input
ATOI     // Converte string para inteiro
STOREG 1     // Armazena num2 no endereço 1
PUSHS "Introduza o terceiro número: "     // Push String
WRITES     // Imprime string
READ  // Le string do input
ATOI     // Converte string para inteiro
STOREG 2     // Armazena num3 no endereço 2
PUSHG 0     // Empilha endreço de num1
PUSHG 1     // Empilha endreço de num2
SUP     // Maior
JZ ELSE0  // Salta para a label de else
PUSHG 0     // Empilha endreço de num1
PUSHG 2     // Empilha endreço de num3
SUP     // Maior
JZ ELSE2  // Salta para a label de else
PUSHG 0     // Empilha endreço de num1
STOREG 3     // Armazena maior no endereço 3
JUMP FIM3  // Salta para o final da Label
ELSE2:    // Label ELSE2
PUSHG 2     // Empilha endreço de num3
STOREG 3     // Armazena maior no endereço 3
FIM3:    // Label FIM3
JUMP FIM1  // Salta para o final da Label
ELSE0:    // Label ELSE0
PUSHG 1     // Empilha endreço de num2
PUSHG 2     // Empilha endreço de num3
SUP     // Maior
JZ ELSE4  // Salta para a label de else
PUSHG 1     // Empilha endreço de num2
STOREG 3     // Armazena maior no endereço 3
JUMP FIM5  // Salta para o final da Label
ELSE4:    // Label ELSE4
PUSHG 2     // Empilha endreço de num3
STOREG 3     // Armazena maior no endereço 3
FIM5:    // Label FIM5
FIM1:    // Label FIM1
PUSHS "O maior é: "     // Push String
WRITES     // Imprime string
PUSHG 3    // Empilha endereço de maior
WRITEI     // Imprime inteiro
WRITELN     // Imprime nova linha
STOP   // Fim do programa
