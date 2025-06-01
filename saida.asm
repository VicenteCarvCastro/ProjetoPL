JUMP MAIN  // Salta para o início do programa
MAIN:
START   // Início do programa
PUSHS "Pascal"     // Push String Literal
STOREG 1     // Armazena name no endereço 1
PUSHS "Hello, "     // Push String Literal
STOREG 2     // Armazena greeting no endereço 2
PUSHG 2    // Empilha endereço de greeting
WRITES     // Imprime string
WRITELN     // Imprime nova linha
PUSHG 1     // Empilha endereço da string
STRLEN     // Calcula o tamanho da string
STOREG 0     // Armazena len no endereço 0
PUSHS "Length of name: "     // Push String
WRITES     // Imprime string
PUSHG 0    // Empilha endereço de len
WRITEI     // Imprime inteiro
WRITELN     // Imprime nova linha
PUSHS "First character: "     // Push String
WRITES     // Imprime string
PUSHG 1     // Empilha  endreço de name
PUSHI 1     // Push valor 1
PUSHI 1     // Offset
SUB     // Offset
CHARAT     // Valor Asccii do caractere
WRITEI     // Imprime inteiro
WRITELN     // Imprime nova linha
PUSHS "Last character: "     // Push String
WRITES     // Imprime string
PUSHG 1     // Empilha  endreço de name
PUSHG 0     // Empilha endreço de len
PUSHI 1     // Offset
SUB     // Offset
CHARAT     // Valor Asccii do caractere
WRITEI     // Imprime inteiro
WRITELN     // Imprime nova linha
STOP   // Fim do programa
