JUMP MAIN  // Salta para o início do programa
BinToInt:    // Label BinToInt
PUSHI 0     // Push valor 0
STOREG 2     // 1Armazena valor no endereço 2
PUSHI 1     // Push valor 1
STOREG 3     // 1Armazena potencia no endereço 3
PUSHG 0     // Empilha endereço da string
STRLEN     // Calcula o tamanho da string
STOREG 1   // Armazena valor inicial na variável
FORINICIO0:    // Label FORINICIO0
PUSHG 1   // Empilha indice
PUSHI 1     // Push valor 1
INF  // Verifica se é inferior
NOT // Negação
JZ FORFIM1   // Se condição for falsa, salta para o fim do loop
PUSHG 0     // Empilha  endreço de bin
PUSHG 1     // Empilha endreço de i
PUSHI 1     // Offset
SUB     // Offset
CHARAT     // Valor Asccii do caractere
PUSHI 49     // Push Char Ascii Value
EQUAL     // Igual
JZ ELSE2  // Salta para a label de else
PUSHG 2     // Empilha endreço de valor
PUSHG 3     // Empilha endreço de potencia
ADD     // Soma de dois valores
STOREG 2     // 1Armazena valor no endereço 2
JUMP FIM3  // Salta para o final da Label
ELSE2:    // Label ELSE2
FIM3:    // Label FIM3
PUSHG 3     // Empilha endreço de potencia
PUSHI 2     // Push valor 2
MUL     // Multiplicação de dois valores
STOREG 3     // 1Armazena potencia no endereço 3
PUSHG 1  // Empilha indice
PUSHI 1  // Empilha 1
SUB  // Decrementa indice
STOREG 1  // Armazena novo valor na variável
JUMP FORINICIO0  // Salta para o início do loop
FORFIM1:    // Label FORFIM1
PUSHG 2     // Empilha endreço de valor
RETURN
MAIN:
START   // Início do programa
PUSHS "Introduza uma string binária:"     // Push String
WRITES     // Imprime string
WRITELN     // Imprime nova linha
READ  // Le string do input
STOREG 0     // Armazena bin no endereço 0
PUSHG 0     // Empilha endreço de bin
PUSHA BinToInt     // Empilha endereço da função BinToInt
CALL    // Invoca Função
STOREG 1     // 1Armazena valor no endereço 1
PUSHS "O valor inteiro correspondente é: "     // Push String
WRITES     // Imprime string
PUSHG 1    // Empilha endereço de valor
WRITEI     // Imprime inteiro
WRITELN     // Imprime nova linha
STOP   // Fim do programa
