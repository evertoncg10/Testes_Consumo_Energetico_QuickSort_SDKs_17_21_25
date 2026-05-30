# Relatório Estatístico Consolidado: Consumo Energético e Eficiência de JDKs

Este relatório apresenta a análise estatística dos testes do algoritmo QuickSort executados nos JDKs 17, 21 e 25. Foram realizadas 40 execuções válidas para cada versão do SDK.

## 1. Estatísticas Descritivas e Variabilidade

### 1.1 Consumo de Energia (Joules)

| JDK | Média (J) | Mediana (J) | Moda (J) | Q1 (25%) | Q3 (75%) | Desvio Padrão (J) | CV (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JDK 17 | 1491.195 | 1486.375 | 1396.940 | 1444.678 | 1533.078 | 57.228 | 3.838% |
| JDK 21 | 1491.439 | 1508.095 | 1321.800 | 1480.670 | 1534.645 | 68.362 | 4.584% |
| JDK 25 | 1508.037 | 1510.975 | 1319.890 | 1461.585 | 1569.610 | 76.700 | 5.086% |

### 1.2 Tempo de Execução (Segundos)

| JDK | Média (s) | Mediana (s) | Moda (s) | Q1 (25%) | Q3 (75%) | Desvio Padrão (s) | CV (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JDK 17 | 33.188 | 33.269 | 31.281 | 32.658 | 33.809 | 0.767 | 2.312% |
| JDK 21 | 33.490 | 33.415 | 32.740 | 32.977 | 33.815 | 0.782 | 2.336% |
| JDK 25 | 33.302 | 33.235 | 32.810 | 32.870 | 33.742 | 0.580 | 1.741% |

### 1.3 Potência (Watts)

| JDK | Média (W) | Mediana (W) | Moda (W) | Q1 (25%) | Q3 (75%) | Desvio Padrão (W) | CV (%) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| JDK 17 | 44.978 | 44.565 | 48.930 | 42.877 | 47.080 | 2.482 | 5.519% |
| JDK 21 | 44.573 | 45.285 | 45.070 | 44.093 | 45.977 | 2.557 | 5.738% |
| JDK 25 | 45.302 | 45.190 | 46.190 | 43.843 | 47.065 | 2.490 | 5.496% |

## 2. Testes de Hipóteses e Comparações Estatísticas

### 2.1 Análise de Variância (ANOVA One-way)
- **Estatística F**: 0.8087
- **p-value**: 4.4793e-01
- **Decisão**: Falha em rejeitar H0 (nível de significância 5%)
- **Conclusão**: Não há diferença estatisticamente significativa nas médias de consumo de energia entre as três versões do JDK.

### 2.2 Comparação Crítica A (Transição LTS: Java 17 vs Java 21) - Teste t
- **p-value**: 0.9862
- **Decisão**: Falha em rejeitar H0
- **Conclusão**: As médias de consumo são estatisticamente equivalentes. Estatisticamente, a versão 21 manteve a estabilidade de consumo e não gerou regressão energética em relação ao Java 17.

### 2.3 Comparação Crítica B (O Salto Moderno: Java 17 vs Java 25) - Teste t
- **p-value**: 0.2694
- **Decisão**: Falha em rejeitar H0
- **Conclusão**: Falha em rejeitar H0. Não há diferença estatisticamente significativa entre o consumo do Java 17 e do Java 25.

## 3. Gráficos Gerados
Os gráficos foram salvos na pasta `resultados/graficos/`:
1. **Boxplot Comparativo**: `comparacao_consumo_boxplot.png`
2. **Média com Intervalo de Confiança (95%)**: `comparacao_consumo_barras_ci.png`
3. **Histogramas com KDE**: `comparacao_distribuicao_hist_kde.png`
4. **Ajuste de Distribuições Individuais (Densidade e QQ-Plot)**:
   - JDK 17: `distribuicoes_densidade_qq_jdk17.png`
   - JDK 21: `distribuicoes_densidade_qq_jdk21.png`
   - JDK 25: `distribuicoes_densidade_qq_jdk25.png`

