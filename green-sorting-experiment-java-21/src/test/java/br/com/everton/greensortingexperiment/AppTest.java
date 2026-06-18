package br.com.everton.greensortingexperiment;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.assertEquals;

@DisplayName("Testes de Cobertura para a Classe Principal (App)")
class AppTest {

    private final PrintStream standardOut = System.out;
    private final ByteArrayOutputStream outputStreamCaptor = new ByteArrayOutputStream();

    @BeforeEach
    void setUp() {
        System.setOut(new PrintStream(outputStreamCaptor));
    }

    @AfterEach
    void tearDown() {
        System.setOut(standardOut);
    }

    @Test
    @Timeout(value = 60, unit = TimeUnit.SECONDS) // Limite de 10s (já que há 5s de sleep no código)
    @DisplayName("Deve executar o método main do experimento com sucesso e imprimir o relatório")
    void deveExecutarMainComSucesso() {
        String[] args = {};

        assertDoesNotThrow(() -> App.main(args),
                "O método main do experimento deve ser executado completamente de ponta a ponta.");

        String output = outputStreamCaptor.toString();

        assertTrue(output.contains("Aguardando estabilização do sistema..."));
        assertTrue(output.contains("--- Iniciando Experimento Energético: Ordenação ---"));
        assertTrue(output.contains("RELATÓRIO DE TEMPO DE EXECUÇÃO"));
        assertTrue(output.contains("Tempo em millis:"));
        assertTrue(output.contains("Tempo em segundos:"));
    }

    @Test
    @Timeout(value = 60, unit = TimeUnit.SECONDS)
    @DisplayName("Deve capturar e tratar InterruptedException corretamente durante a estabilização")
    void deveTratarInterrupcaoDaThread() throws InterruptedException {
        Thread appThread = new Thread(() -> App.main(new String[]{}));
        appThread.start();
        Thread.sleep(500);
        appThread.interrupt();
        appThread.join();

        String output = outputStreamCaptor.toString();

        assertTrue(output.contains("--- Iniciando Experimento Energético: Ordenação ---"));
        assertEquals(Thread.State.TERMINATED, appThread.getState());
    }
}