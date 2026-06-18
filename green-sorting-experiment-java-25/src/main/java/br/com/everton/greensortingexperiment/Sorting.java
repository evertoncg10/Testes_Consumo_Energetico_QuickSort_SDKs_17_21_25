package br.com.everton.greensortingexperiment;

import java.util.Arrays;
import java.util.Random;

public class Sorting {

    /**
     * Class responsible for executing the sorting experiment for energy consumption analysis.
     * <p>
     * This class implements the QuickSort algorithm to generate a consistent CPU and
     * memory workload, enabling energy profiling tools like JoularJX to measure
     * the efficiency of the Java Virtual Machine.
     * </p>
     *
     * @author Everton Cezar Gonçalves
     * @version 1.0
     */
    public static void execute(int iterations) {
        int arraySize = 100_000;
        int[] originalArray = new Random().ints(arraySize, 0, 1_000_000).toArray();

        for (int i = 0; i < iterations; i++) {
            // Efetua Copia do array original para garantir que cada iteração seja de dados desordenados
            int[] testArray = Arrays.copyOf(originalArray, originalArray.length);
            quickSort(testArray, 0, testArray.length - 1);
        }
    }

    /**
     * Implements the QuickSort algorithm using a recursive "Divide and Conquer" strategy.
     * <p>
     * This method serves as the primary computational engine for the experiment. By
     * recursively partitioning the array into smaller sub-arrays, it creates a
     * high-intensity workload that challenges the CPU's branch prediction and the
     * JVM's stack management. This level of activity is ideal for measuring
     * energy consumption stability across different Java versions.
     * </p>
     *
     * @param testArray  The integer array to be sorted (a copy of the original data).
     * @param startIndex The starting index of the sub-array currently being processed.
     * @param endIndex   The ending index of the sub-array currently being processed.
     */
    private static void quickSort(int[] testArray, int startIndex, int endIndex) {
        if (startIndex < endIndex) {
            int pi = partition(testArray, startIndex, endIndex);
            quickSort(testArray, startIndex, pi - 1);
            quickSort(testArray, pi + 1, endIndex);
        }
    }

    /**
     * Performs the array partitioning using the Lomuto partition scheme.
     * <p>
     * This method selects the last element of the range as the pivot, reorganizing
     * the array so that all elements smaller than the pivot are placed to its left
     * and larger elements to its right. This operation represents the core
     * computational effort measured during the experiment.
     * </p>
     *
     * @param testArray  The array being reorganized.
     * @param startIndex The starting index of the partition.
     * @param endIndex   The ending index (pivot position).
     * @return The final position index of the pivot after reorganization.
     */
    private static int partition(int[] testArray, int startIndex, int endIndex) {
        int pivot = testArray[endIndex];
        int i = (startIndex - 1);
        for (int j = startIndex; j < endIndex; j++) {
            if (testArray[j] < pivot) {
                i++;
                int temp = testArray[i];
                testArray[i] = testArray[j];
                testArray[j] = temp;
            }
        }
        int temp = testArray[i + 1];
        testArray[i + 1] = testArray[endIndex];
        testArray[endIndex] = temp;
        return i + 1;
    }
}