#!/usr/bin/env bash

if [ ! -f parser.py ]; then
  echo "Erro: não encontrei parser2.py neste diretório."
  exit 1
fi

shopt -s nullglob
pascal_files=(pascal/*.pas)
shopt -u nullglob

if [ ${#pascal_files[@]} -eq 0 ]; then
  echo "Não há arquivos .pas para processar."
  exit 0
fi

for arquivo in "${pascal_files[@]}"; do
  echo "=============================="
  echo "Processando $arquivo..."
  echo "=============================="

  python3 parser.py < "$arquivo"
  if [ $? -ne 0 ]; then
    echo "  → Erro ao rodar parser2.py sobre $arquivo"
    continue
  fi

  base="$(basename "${arquivo%.pas}")"
  if [ -f saida.asm ]; then
    mv saida.asm "pascal/${base}.asm"
    echo "  → Gerado: pascal/${base}.asm"
  else
    echo "  → Aviso: parser2.py não produziu saida.asm para $arquivo"
  fi
done

echo
echo "Processamento concluído."
