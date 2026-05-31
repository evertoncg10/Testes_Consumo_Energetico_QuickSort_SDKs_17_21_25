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

## 2. Testes de Premissas Estatísticas

Para determinar se devemos utilizar testes paramétricos (ANOVA e Teste t) ou não-paramétricos (Kruskal-Wallis e Mann-Whitney U), avaliamos a normalidade e homocedasticidade dos dados.

### 2.1 Teste de Normalidade (Shapiro-Wilk)
- **H0**: A distribuição dos dados de consumo de energia é normal.
- **H1**: A distribuição não é normal.

| JDK | Estatística W | p-value | Distribuição |
| --- | --- | --- | --- |
| JDK 17 | 0.9602 | 0.1708 | Normal (p >= 0.05) |
| JDK 21 | 0.8689 | 0.0003 | Não Normal (p < 0.05) |
| JDK 25 | 0.9785 | 0.6342 | Normal (p >= 0.05) |

### 2.2 Teste de Homocedasticidade (Levene)
- **H0**: As variâncias de consumo de energia são iguais entre os grupos (homocedasticidade).
- **H1**: As variâncias são significativamente diferentes.

- **Estatística de Levene**: 1.8428
- **p-value**: 0.1629
- **Resultado**: Variâncias Iguais (p >= 0.05)

> [!WARNING]
> **Decisão Metodológica**: Como a normalidade foi rejeitada para pelo menos um dos grupos (JDK 21), a premissa para a ANOVA clássica foi violada. Portanto, os testes não-paramétricos (**Kruskal-Wallis** e **Mann-Whitney U**) são utilizados como os testes metodologicamente corretos para as análises globais e par a par.

## 3. Testes de Hipóteses e Comparações Estatísticas

### 3.1 Comparação Global de Eficiência Energética
**Teste Utilizado**: Kruskal-Wallis

- **H0**: $F_{Java17}(x) = F_{Java21}(x) = F_{Java25}(x)$ (As distribuições de consumo de energia são idênticas; as medianas são estatisticamente iguais).
- **H1**: Pelo menos uma das versões do JDK possui uma distribuição de consumo de energia diferente.

- **Estatística H (Kruskal-Wallis)**: 1.5472
- **p-value**: 4.6134e-01
- **Decisão**: Falha em rejeitar H0 (nível de significância 5%)
- **Conclusão**: Não há diferença estatisticamente significativa no consumo de energia entre as três versões do JDK no quadro global de 40 execuções.

#### Teste Post-Hoc: Mann-Whitney U Pareados com Ajuste Holm-Bonferroni

| Comparação | p-value Bruto | p-value Corrigido | Rejeita H0 (α=5%) |
| --- | --- | --- | --- |
| JDK 17 vs JDK 21 | 0.5540 | 1.0000 | Não |
| JDK 17 vs JDK 25 | 0.2092 | 0.6276 | Não |
| JDK 21 vs JDK 25 | 0.5476 | 1.0000 | Não |

### 3.2 Comparação Crítica A (Transição LTS: Java 17 vs Java 21)
**Teste Utilizado**: Mann-Whitney U

- **H0**: As distribuições de consumo de energia do Java 17 e do Java 21 são estatisticamente iguais.
- **H1**: As distribuições de consumo são estatisticamente diferentes.

- **Estatística do Teste**: 738.0000
- **p-value**: 0.5540
- **Decisão**: Falha em rejeitar H0
- **Conclusão**: Não há diferença estatisticamente significativa na transição LTS.
  - **Nota Analítica**: Estatisticamente, a versão 21 manteve a estabilidade de consumo e não gerou regressão energética em relação ao Java 17. As médias globais foram extremamente próximas (1491.19 J vs 1491.44 J).

### 3.3 Comparação Crítica B (O Salto Moderno: Java 17 vs Java 25)
**Teste Utilizado**: Teste t (Student, Variâncias Iguais)

- **H0**: $\mu_{Java17} = \mu_{Java25}$ (As médias de consumo de energia são iguais).
- **H1**: $\mu_{Java17} \neq \mu_{Java25}$ (As médias de consumo são diferentes).

- **Estatística do Teste**: -1.1131
- **p-value**: 0.2691
- **Decisão**: Falha em rejeitar H0
- **Conclusão**: Falha em rejeitar H0. Não há diferença estatisticamente significativa entre o consumo geral de energia do Java 17 e do Java 25 sob estresse contínuo de 40 execuções.

### 3.4 Avaliação de Ganho de Eficiência no Warm-up (Apenas Primeiras 10 Execuções: Java 17 vs Java 25)
**Teste Utilizado**: Teste t (Student, Unilateral, Variâncias Iguais)

- **H0**: $\mu_{Java25} \ge \mu_{Java17}$ (O Java 25 consome o mesmo ou mais que o Java 17 no início).
- **H1**: $\mu_{Java25} < \mu_{Java17}$ (O Java 25 consome significativamente menos energia, comprovando ganho de eficiência no tiro curto).

- **Estatística do Teste**: -4.8400
- **p-value**: 6.5713e-05
- **Decisão**: Rejeita-se H0
- **Conclusão**: Rejeita-se H0 em favor de H1 (p < 0.05). Existe ganho de eficiência estatisticamente comprovado para o Java 25 no início das execuções.
  - **Nota Analítica**: O Java 25 consumiu em média apenas **1444.90 J** no início (fase de warm-up) contra **1546.97 J** do Java 17. O p-value foi minúsculo (6.5713e-05), o que comprova estatisticamente com um teste unilateral que a evolução para o Java 25 trouxe um ganho expressivo de eficiência (redução de aproximadamente 6.6% no consumo energético) em execuções curtas.

## 4. Gráficos Gerados
Os gráficos foram salvos na pasta `resultados/graficos/`:
1. **Boxplot Comparativo**: `comparacao_consumo_boxplot.png`
2. **Média com Intervalo de Confiança (95%)**: `comparacao_consumo_barras_ci.png`
3. **Histogramas com KDE**: `comparacao_distribuicao_hist_kde.png`
4. **Ajuste de Distribuições Individuais (Densidade e QQ-Plot)**:
   - JDK 17: `distribuicoes_densidade_qq_jdk17.png`
   - JDK 21: `distribuicoes_densidade_qq_jdk21.png`
   - JDK 25: `distribuicoes_densidade_qq_jdk25.png`

