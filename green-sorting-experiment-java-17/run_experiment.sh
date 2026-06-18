#!/bin/bash

# Configurações
JAR_FILE="target/green-sorting-experiment-java-17-1.0-SNAPSHOT.jar"
JOULAR_JAR="/home/everton/Documentos/joularjx/target/joularjx-3.1.0.jar=methods=all"
OUTPUT_FILE="relatorio_final.txt"
RESULT_DIR="joularjx-result"

> $OUTPUT_FILE

echo "Iniciando 40 execuções no Predator..."

for i in {1..40}
do
    echo "----------------------------------------"
    echo "Executando $i de 40..."

    echo "Execução $i" >> $OUTPUT_FILE

    SAIDA_COMPLETA=$(java -javaagent:$JOULAR_JAR -jar $JAR_FILE 2>&1)

    echo "$SAIDA_COMPLETA" | tee -a $OUTPUT_FILE

    echo -e "\n" >> $OUTPUT_FILE

    # Espera para garantir escrita em disco
    sleep 2

    LATEST_FOLDER=$(ls -td ${RESULT_DIR}/[0-9]* 2>/dev/null | head -1)
    if [ -n "$LATEST_FOLDER" ]; then
        FOLDER_NAME=$(basename "$LATEST_FOLDER")
        NEW_FOLDER_NAME="${RESULT_DIR}/Execucao_${i}_PID_${FOLDER_NAME}"
        mv "$LATEST_FOLDER" "$NEW_FOLDER_NAME"
        echo "Pasta $NEW_FOLDER_NAME organizada."
    fi

    sleep 2
done

echo "Concluído! O relatório completo está em: $OUTPUT_FILE"