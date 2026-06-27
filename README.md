# Análise de Eficiência Energética de JVMs: JDK 17 vs 21 vs 25

[![Java Support](https://img.shields.io/badge/Java-17%20%7C%2021%20%7C%2025-orange?logo=openjdk)](https://github.com/features/actions)
[![Python Analysis](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Open Science](https://img.shields.io/badge/Open%20Science-Compliant-success)](#-ci%C3%AAncia-aberta)

Este repositório contém o ambiente experimental, os códigos-fonte e os scripts de análise estatística utilizados para avaliar a eficiência energética, o consumo de potência e o tempo de execução das versões da Virtual Machine Java (JVM) da iniciativa **Eclipse Temurin** nas versões **JDK 17, JDK 21 e JDK 25**.

O experimento foi desenvolvido como parte de um trabalho de pesquisa científica de mestrado na área de *Green Software* (Software Verde). Ele analisa o comportamento térmico, o ciclo de vida da JVM, técnicas de *warm-up* e o consumo dinâmico de recursos sob estresse contínuo utilizando o algoritmo de ordenação **QuickSort**.

---

## 📂 Estrutura do Repositório

O projeto é estruturado de forma modular para separar as baterias de testes em Java da inteligência analítica em Python. A estrutura de diretórios e arquivos principais está organizada da seguinte forma:

```text
├── Analise_Estatistica/
│   ├── dados/                         # Planilhas Excel com resultados consolidados de cada JDK
│   ├── resultados/                    # Relatório estatístico consolidado e gráficos exportados
│   │   └── graficos/                  # Boxplots, histogramas com KDE e QQ-Plots gerados
│   ├── analise_jdk17.py               # Análise estatística individual para o JDK 17
│   ├── analise_jdk21.py               # Análise estatística individual para o JDK 21
│   ├── analise_jdk25.py               # Análise estatística individual para o JDK 25
│   ├── comparacao_sdks.py             # Testes de hipóteses comparativos globais e pareados
│   ├── estatistica_utils.py           # Funções utilitárias de carregamento, cálculo e plotagem
│   └── main.py                        # Orquestrador do pipeline de análise em Python
│
├── green-sorting-experiment-java-17/  # Projeto Java instrumentado configurado para JDK 17
│   ├── run_experiment.sh              # Script Shell para rodar 40 execuções do experimento
│   └── src/                           # Código-fonte Java (App.java e Sorting.java)
│
├── green-sorting-experiment-java-21/  # Projeto Java instrumentado configurado para JDK 21
│   ├── run_experiment.sh              # Script Shell para rodar 40 execuções do experimento
│   └── src/                           # Código-fonte Java (App.java e Sorting.java)
│
├── green-sorting-experiment-java-25/  # Projeto Java instrumentado configurado para JDK 25
│   ├── run_experiment.sh              # Script Shell para rodar 40 execuções do experimento
│   └── src/                           # Código-fonte Java (App.java e Sorting.java)
└── README.md                          # Documentação principal do repositório
```

### Detalhes dos Componentes:

*   **Projetos Java (`green-sorting-experiment-java-*`):** Cada diretório contém um projeto Maven isolado com o código instrumentado para rodar a carga de trabalho de ordenação (QuickSort) na respectiva JVM. O script `run_experiment.sh` em cada pasta automatiza o processo de execução e coleta de dados pelo agente JoularJX.
*   **Módulo de Análise Estatística (`Analise_Estatistica`):** Centraliza os dados coletados em planilhas na pasta [dados/](./Analise_Estatistica/dados) e executa análises individuais e comparativas por meio do script orquestrador [main.py](./Analise_Estatistica/main.py), que automatiza testes de premissas (Shapiro-Wilk, Levene), testes de hipóteses (Kruskal-Wallis/ANOVA, Mann-Whitney U/Tukey HSD) e gera relatórios científicos em Markdown e gráficos estatísticos.

---

## 🔬 Metodologia de Teste e Instrumentação

A medição precisa do gasto energético de software depende do controle metodológico das cargas de trabalho e da infraestrutura de coleta. O fluxo experimental deste repositório foi construído a partir das seguintes diretrizes:

### 1. Algoritmo e Carga de Trabalho
*   **Algoritmo:** Utilização do algoritmo de ordenação **QuickSort** (implementado com o esquema de partição de **Lomuto**).
*   **Carga Útil:** Ordenação de um array contendo **100.000 números inteiros aleatórios** (variando na faixa de 0 a 1.000.000).
*   **Controle de Warm-up:** A aplicação foi instrumentada internamente para rodar **6.000 iterações do QuickSort** por execução. Essa estratégia força o processamento contínuo por uma janela temporal superior a 30 segundos, possibilitando:
    1.  O aquecimento (*warm-up*) do código pelo compilador **JIT (Just-In-Time)**.
    2.  A estabilização térmica do processador após o pico inicial do *Turbo Boost*.
    3.  Amostragem estatística robusta pela ferramenta de medição energética, minimizando ruídos do sistema operacional.
*   **Estabilização:** Implementação de tempos controlados de espera de estabilização inicial (3 segundos) e estabilização final (2 segundos) para garantir a consistência das leituras e logs de energia.

### 2. Monitoramento Energético (JoularJX)
*   **Agente de Coleta:** O monitoramento foi conduzido utilizando o **[JoularJX (Agent Version 3.1.0)](https://github.com/joular/joularjx)** (veja a [Documentação Oficial do JoularJX](https://www.noureddine.org/research/joular/joularjx)).
*   **Mecanismo:** A ferramenta baseia-se em software (`-javaagent`), coletando dados brutos de consumo de CPU por meio da interface **Intel RAPL** (Running Average Power Limit) e realizando amostragem periódica para cruzar o gasto energético com a pilha de chamadas (*call stack*) do programa.

### 3. Automação e Controle de Viés
*   A bateria de testes foi orquestrada por meio de um script Shell (`run_experiment.sh`) que realiza **40 execuções consecutivas** para cada JDK de maneira automatizada.
*   Entre cada rodada, o script insere pausas de resfriamento térmico e de finalização de escritas em disco (`sleep`), mitigando o efeito acumulado de calor (estrangulamento térmico/*thermal throttling*) e latências de I/O.
*   Os logs gerados na pasta de saída `joularjx-result/` são renomeados sistematicamente incluindo o índice da execução e o identificador do processo (`PID`), consolidando os outputs principais no arquivo `relatorio_final.txt`.

---

## 🧮 Métricas Analisadas

Três variáveis de resposta principais são avaliadas no experimento:

1.  **Tempo de Execução ($t$):** Medido em segundos ($s$), representa o tempo total para a conclusão da carga útil.
2.  **Gasto de Energia ($E$):** Medido em Joules ($J$), representa a energia total acumulada capturada pelo agente JoularJX.
3.  **Potência Média ($P$):** Medida em Watts ($W$), expressa a taxa de consumo de energia por unidade de tempo, calculada através da fórmula:

$$P = \frac{E}{t}$$

A potência média nos ajuda a decifrar a causa subjacente da eficiência energética de uma JVM: se uma versão do JDK consome menos energia porque executa mais rápido (mesma potência por menos tempo) ou se ela atua reduzindo a demanda térmica e elétrica instantânea do processador (menor potência em tempo similar).

---

## 🚀 Como Replicar os Experimentos

### 1. Execução dos Testes Java

#### Pré-requisitos
*   **Eclipse Temurin JDK** nas versões **17**, **21** e **25** instalados em sua máquina.
*   **Apache Maven** instalado e configurado nas variáveis de ambiente.
*   O arquivo JAR do agente **JoularJX** (`joularjx-3.1.0.jar`) baixado localmente.
*   Ambiente de terminal compatível com Shell Script (Linux, macOS ou Git Bash/WSL no Windows).

---

#### Passo 1: Configuração do JDK Ativo

Para executar cada bateria de testes, você precisa definir qual versão do Java estará ativa no seu terminal. Escolha uma das duas abordagens abaixo:

##### Opção A: Utilizando o SDKMAN! (Recomendado e Simplificado)
Se você gerencia suas versões do Java com o SDKMAN!, basta utilizar o comando `use` para mudar de versão em segundos na sua sessão atual do terminal:

```bash
# Para rodar os testes do JDK 17
sdk use java 17.x.x-tem

# Para rodar os testes do JDK 21
sdk use java 21.x.x-tem

# Para rodar os testes do JDK 25
sdk use java 25.x.x-tem
```

---

##### Opção B: Sem o SDKMAN! (Configuração Manual de Ambiente)
Caso não utilize o SDKMAN!, você deve apontar manualmente as variáveis `JAVA_HOME` e `PATH` do seu terminal para a pasta onde instalou o Eclipse Temurin correspondente. 

Veja como realizar essa configuração temporária (válida para a sessão atual do terminal) de acordo com o seu sistema operacional:

###### 💻 Windows
Se estiver utilizando o Windows, abra o console de sua preferência (CMD ou PowerShell) e execute os comandos abaixo (ajustando o caminho para o diretório de instalação do seu JDK):

*   **No PowerShell:**
    ```powershell
    # Exemplo para o JDK 17 (altere o caminho para a sua pasta real)
    $env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.x.x-hotspot"
    $env:Path = "$env:JAVA_HOME\bin;$env:Path"
    ```
*   **No Command Prompt (CMD):**
    ```cmd
    :: Exemplo para o JDK 17 (altere o caminho para a sua pasta real)
    set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.x.x-hotspot
    set Path=%JAVA_HOME%\bin;%Path%
    ```

###### 🐧 Linux
No Linux, exporte as variáveis diretamente na sua sessão do terminal. Você também pode utilizar o sistema de alternativas da distribuição:

*   **Exportação de Variável (Sessão Atual):**
    ```bash
    # Exemplo para o JDK 17 (altere o caminho para a sua pasta real)
    export JAVA_HOME=/usr/lib/jvm/java-17-temurin
    export PATH=$JAVA_HOME/bin:$PATH
    ```
*   **Via Alternativas do Sistema (Global):**
    Se os JDKs foram instalados via gerenciador de pacotes, use as ferramentas do sistema para alternar a versão padrão do terminal:
    ```bash
    sudo update-alternatives --config java
    sudo update-alternatives --config javac
    ```

###### 🍎 macOS
No macOS, você pode tirar proveito da ferramenta integrada `/usr/libexec/java_home` para resolver e apontar os caminhos das versões instaladas automaticamente:

```bash
# Apontar para o JDK 17
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export PATH=$JAVA_HOME/bin:$PATH

# Apontar para o JDK 21
export JAVA_HOME=$(/usr/libexec/java_home -v 21)
export PATH=$JAVA_HOME/bin:$PATH

# Apontar para o JDK 25
export JAVA_HOME=$(/usr/libexec/java_home -v 25)
export PATH=$JAVA_HOME/bin:$PATH
```

###### 🔍 Validação da Versão
Após realizar a troca utilizando qualquer um dos métodos manuais, valide se o terminal está respondendo com a versão correta do Java e do compilador:
```bash
java -version
javac -version
```

---

#### Passo 2: Compilação e Execução dos Experimentos

Com a versão correta do Java configurada e ativa no terminal, siga o fluxo de execução para a pasta do respectivo JDK (exemplo com o JDK 17):

1.  **Navegue até a pasta do projeto correspondente:**
    ```bash
    cd green-sorting-experiment-java-17
    ```
2.  **Compile e empacote a aplicação utilizando o Maven:**
    ```bash
    mvn clean package
    ```
3.  **Ajuste o caminho do agente JoularJX no script:**
    Abra o arquivo `run_experiment.sh` e atualize a variável `JOULAR_JAR` com o caminho absoluto para o arquivo JAR do seu agente local:
    ```bash
    JOULAR_JAR="/caminho/absoluto/para/seu/joularjx-3.1.0.jar=methods=all"
    ```
4.  **Dê permissão de execução e inicie a bateria de testes:**
    ```bash
    chmod +x run_experiment.sh
    ./run_experiment.sh
    ```
5.  Os resultados brutos de cada uma das 40 execuções serão organizados sob o diretório `joularjx-result/` e o consolidado final será salvo no arquivo `relatorio_final.txt`.

Repita este fluxo para as pastas `green-sorting-experiment-java-21` e `green-sorting-experiment-java-25`, lembrando sempre de **mudar a versão correspondente da JVM no terminal** antes de rodar os comandos do Maven e do Script.

---

### 2. Fluxo de Análise Estatística (Python)

Após a consolidação dos testes, as planilhas geradas (como as já presentes na pasta `Analise_Estatistica/dados/`) são submetidas ao pipeline estatístico em Python para validação e comparação científica das métricas.

#### Pré-requisitos
*   Python 3.10 ou superior.
*   Instalação dos pacotes de ciência de dados necessários:
    ```bash
    cd Analise_Estatistica
    python -m venv .venv
    source .venv/bin/activate  # No Windows: .venv\Scripts\activate
    pip install pandas numpy scipy matplotlib seaborn openpyxl
    ```

#### Execução
Execute o script orquestrador na raiz do módulo de estatística:
```bash
python main.py
```

#### Etapas da Análise Realizada:
1.  **Estatísticas Descritivas:** Cálculo de média, mediana, moda, quartis (Q1 e Q3), desvio padrão e coeficiente de variação (CV) para Energia, Tempo e Potência.
2.  **Ajuste de Distribuições Teóricas:** Ajuste de curvas de densidade de probabilidade (**Normal, Log-normal, Gama, Weibull**) nos dados empíricos de energia e geração de gráficos comparativos e **QQ-Plots** (salvos em `resultados/graficos/`).
3.  **Análise de Margem de Erro e Amostragem:** Avaliação de intervalos de confiança (95%) e cálculo do tamanho de amostra necessário para alcançar margens de erro teóricas de 1%, 2% e 5%.
4.  **Validação de Premissas Estatísticas:** Execução do teste de **Shapiro-Wilk** para normalidade das amostras e do teste de **Levene** para homocedasticidade (homogeneidade de variâncias).
5.  **Testes de Hipóteses Comparativos:**
    *   Caso as premissas paramétricas sejam atendidas, executa **ANOVA One-Way** com post-hoc de **Tukey HSD**.
    *   Caso haja violação de premissas (como a não-normalidade de algum grupo), executa o teste não-paramétrico de **Kruskal-Wallis** com testes pareados post-hoc de **Mann-Whitney U** aplicando ajuste de **Holm-Bonferroni**.
6.  **Análise de Warm-up:** Teste de hipótese unilateral focado nas 10 primeiras execuções comparando o JDK 17 com o JDK 25 para verificar o ganho de eficiência no curto prazo.
7.  **Relatório Unificado:** Geração automática do arquivo consolidado de resultados em formato acadêmico [relatorio_estatistico.md](./Analise_Estatistica/resultados/relatorio_estatistico.md).

---

## 📊 Ciência Aberta (Open Science)

Alinhado às diretrizes e boas práticas de **Ciência Aberta (Open Science)**, todos os recursos deste estudo são públicos e reprodutíveis:
*   Os códigos-fonte idênticos em Java para as três versões de JDK.
*   Os scripts shell orquestradores e utilitários.
*   As planilhas com os resultados empíricos das 40 execuções válidas de cada JDK na pasta [Analise_Estatistica/dados/](./Analise_Estatistica/dados).
*   Os códigos-fonte de análise estatística em Python e gráficos correspondentes.