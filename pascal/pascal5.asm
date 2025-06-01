ALLOC 5 // Aloca espaço para o array numeros com tamanho 5
STOREG 0 // Armazena o o array numeros no endereço 0
JUMP MAIN  // Salta para o início do programa
MAIN:
START   // Início do programa
PUSHI 0     // Push valor 0
STOREG 2     // Armazena soma no endereço 2
PUSHS "Introduza 5 numeros inteiros:"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHI 1     // Push valor 1
STOREG 1  // 2Armazena i no endereço 1
FORINICIO0:    // Label FORINICIO0
PUSHG 1    // Empilha indice
PUSHI 5     // Push valor 5
SUP    // Verifica se o indice é maior que o limite superior
NOT   // Negação
JZ FORFIM1   // Se condição for falsa, salta para o fim do loop
PUSHG 0     // Empilha endereço base do array numeros
PUSHG 1     // Empilha endreço de i
PUSHI 1     // Offset
SUB     // Offset
READ     // lê string do input
ATOI     // Converte string para inteiro
STOREN     // Armazena o valor lido no array
PUSHG 2     // Empilha endreço de soma
PUSHG 0     // Empilha endereço base do array numeros
PUSHG 1     // Empilha endreço de i
PUSHI 1     // Offset
SUB     // Offset
LOADN     // Carrega valor do array
FADD     // Soma de dois valores
STOREG 2     // Armazena soma no endereço 2
PUSHG 1 // Empilha indice
PUSHI 1   // Empilha 1
ADD  // Incrementa indice
STOREG 1  // Armazena novo valor na variável
JUMP FORINICIO0   // Salta para o início do loop
FORFIM1:    // Label FORFIM1
PUSHS "A soma dos números é: "     // Push String
WRITES     // Imprime string
PUSHG 2    // Empilha endereço de soma
WRITEI     // Imprime inteiro
WRITELN     // Imprime nova linha
STOP   // Fim do programa
