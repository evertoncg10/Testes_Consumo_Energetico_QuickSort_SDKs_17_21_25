package br.com.everton.greensortingexperiment;

/**
 * Main class responsible for coordinating the energy consumption measurement experiment.
 * <p>
 * The objective of this application is to generate a constant processing workload through the
 * QuickSort sorting algorithm, applying it to an integer array to allow monitoring
 * tools (such as JoularJX) to capture the energy efficiency of the Java Virtual Machine (JVM).
 * </p>
 *
 * <p>
 * The primary purpose of using multiple iterations is to ensure the stabilization
 * of the energy measurement environment.
 * This procedure is necessary for:
 * 1. JVM Warm-up: Ensuring the code is optimized by the JIT Compiler before final data collection.
 * 2. Robust Sampling: Providing an extensive time window (30s+) that allows JoularJX
 * to capture multiple energy samples, reducing the impact of operating system noise.
 * 3. Thermal Stability: Allowing the processor to stabilize its frequency and consumption
 * after the initial Turbo Boost peak.
 * </p>
 *
 * @author Everton Cezar Gonçalves
 * @version 1.0
 */
public class App {
    public static void main(String[] args) {
        // Estabilização inicial é necessário para o JoularJX detectar o "piso" de consumo de energia
        try {
            System.out.println("Aguardando estabilização do sistema...");
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        System.out.println("--- Iniciando Experimento Energético: Ordenação ---");

        long startTime = System.nanoTime();

        Sorting.execute(6000);

        long endTime = System.nanoTime();

        // Estabilização final para garantir a captura do log de energia
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        imprimirRelatorio(startTime, endTime);
    }

    private static void imprimirRelatorio(long start, long end) {
        long tempoNanos = end - start;

        // Conversão mantendo a precisão decimal
        double tempoMillis = tempoNanos / 1_000_000.0;
        double tempoSegundos = tempoNanos / 1_000_000_000.0;

        System.out.println("\n   RELATÓRIO DE TEMPO DE EXECUÇÃO");
        System.out.println("========================================");
        System.out.printf("Tempo em millis:    %.4f ms%n", tempoMillis);
        System.out.printf("Tempo em segundos:  %.6f s%n", tempoSegundos);
        System.out.println("========================================\n");
    }
}