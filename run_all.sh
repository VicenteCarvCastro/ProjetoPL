#!/usr/bin/env bash

# Script: run_all.sh
# Percorre todos os .pas do diretório, executa parser2.py e renomeia saida.asm

# Verifica se o parser2.py existe
if [ ! -f parser2.py ]; then
  echo "Erro: não encontrei parser2.py neste diretório."
  exit 1
fi

# Loop em cada arquivo .pas
for arquivo in *.pas; do
  # Verifica se existe ao menos um .pas
  if [ ! -e "$arquivo" ]; then
    echo "Não há arquivos .pas para processar."
    exit 0
  fi

  echo "=============================="
  echo "Processando $arquivo..."
  echo "=============================="

  # Executa o parser gerando saida.asm
  python3 parser2.py < "$arquivo"
  if [ $? -ne 0 ]; then
    echo "  → Erro ao rodar parser2.py sobre $arquivo"
    continue
  fi

  # Se saiu sem erro, renomeia saida.asm para <base>.asm
  base="${arquivo%.pas}"
  if [ -f saida.asm ]; then
    mv saida.asm "${base}.asm"
    echo "  → Gerado: ${base}.asm"
  else
    echo "  → Aviso: parser2.py não produziu saida.asm para $arquivo"
  fi
done

echo
echo "Processamento concluído."
