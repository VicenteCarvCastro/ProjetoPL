JUMP MAIN  // Salta para o início do programa
MAIN:
START   // Início do programa
PUSHS "Introduza um número inteiro positivo:"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
READ  // Le string do input
ATOI     // Converte string para inteiro
STOREG 0     // Armazena n no endereço 0
PUSHI 1     // Push valor 1
STOREG 2     // Armazena fat no endereço 2
PUSHI 1     // Push valor 1
STOREG 1  // 2Armazena i no endereço 1
FORINICIO0:    // Label FORINICIO0
PUSHG 1    // Empilha indice
PUSHG 0     // Empilha endreço de n
SUP    // Verifica se o indice é maior que o limite superior
NOT   // Negação
JZ FORFIM1   // Se condição for falsa, salta para o fim do loop
PUSHG 2     // Empilha endreço de fat
PUSHG 1     // Empilha endreço de i
FMUL     // Multiplicação de dois valores
STOREG 2     // Armazena fat no endereço 2
PUSHG 1 // Empilha indice
PUSHI 1   // Empilha 1
ADD  // Incrementa indice
STOREG 1  // Armazena novo valor na variável
JUMP FORINICIO0   // Salta para o início do loop
FORFIM1:    // Label FORFIM1
PUSHS "Fatorial de "     // Push String
WRITES     // Imprime string
PUSHG 0    // Empilha endereço de n
WRITEI     // Imprime inteiro
PUSHS ": "     // Push String
WRITES     // Imprime string
PUSHG 2    // Empilha endereço de fat
WRITEI     // Imprime inteiro
WRITELN     // Imprime nova linha
STOP   // Fim do programa
