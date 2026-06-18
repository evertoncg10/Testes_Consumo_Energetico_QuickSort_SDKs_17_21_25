package br.com.everton.greensortingexperiment;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

import java.lang.reflect.Method;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

@DisplayName("Testes de Cobertura e Lógica para a Classe Sorting")
class SortingTest {

    @Test
    @Timeout(value = 15, unit = TimeUnit.SECONDS)
    @DisplayName("Deve executar a carga de trabalho de ordenação sem lançar exceções")
    void deveExecutarCargaSemErros() {
        // Foi passado um número baixo de iterações (ex: 5) apenas para validar
        // a alocação de memória e o fluxo de execução no ambiente de testes (CI).
        assertDoesNotThrow(() -> Sorting.execute(5),
                "O método execute deve processar as iterações sem falhas de alocação ou exceções.");
    }

    @Test
    @DisplayName("Deve ordenar corretamente um array desordenado usando o método privado quickSort")
    void deveOrdenarArrayDesordenado() throws Exception {
        int[] arrayDesordenado = {9, 2, 7, 4, 1, 8, 3, 6, 5};
        int[] arrayEsperado = {1, 2, 3, 4, 5, 6, 7, 8, 9};

        invocarQuickSortPrivado(arrayDesordenado);

        assertArrayEquals(arrayEsperado, arrayDesordenado, "O array não foi ordenado corretamente.");
    }

    @Test
    @DisplayName("Deve manter o array intacto se ele já estiver ordenado")
    void deveLidarComArrayJaOrdenado() throws Exception {
        int[] arrayOrdenado = {1, 2, 3, 4, 5};
        int[] arrayEsperado = {1, 2, 3, 4, 5};

        invocarQuickSortPrivado(arrayOrdenado);

        assertArrayEquals(arrayEsperado, arrayOrdenado, "O algoritmo modificou um array que já estava ordenado.");
    }

    @Test
    @DisplayName("Deve ordenar corretamente um array que contenha elementos duplicados")
    void deveLidarComElementosDuplicados() throws Exception {
        int[] arrayComDuplicatas = {4, 2, 4, 1, 2, 9, 1};
        int[] arrayEsperado = {1, 1, 2, 2, 4, 4, 9};

        invocarQuickSortPrivado(arrayComDuplicatas);

        assertArrayEquals(arrayEsperado, arrayComDuplicatas, "O algoritmo falhou ao ordenar elementos duplicados.");
    }

    /**
     * Método utilitário para invocar o método privado quickSort via Reflection.
     * Isso permite validar a regra de negócio sem precisar alterar a visibilidade
     * dos métodos na classe principal.
     */
    private void invocarQuickSortPrivado(int[] array) throws Exception {
        Method metodoQuickSort = Sorting.class.getDeclaredMethod("quickSort", int[].class, int.class, int.class);
        metodoQuickSort.setAccessible(true); // Quebra o encapsulamento apenas para o teste
        metodoQuickSort.invoke(null, array, 0, array.length - 1);
    }
}