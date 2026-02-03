import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import java.util.Date;

/**
 * Tests unitaires générés automatiquement pour Calculator.java
 * Utilise Mockito pour mocker les dépendances
 */
@ExtendWith(MockitoExtension.class)
public class CalculatorTest {
    
    @InjectMocks
    private Calculator instance;

    @BeforeEach
    public void setUp() {
        // Mocks automatically injected by Mockito
    }
    
    @Test
    public void testInstantiation() {
        assertNotNull(instance, "L'instance ne doit pas être null");
    }

    @Test
    public void testAdd() {
        assertDoesNotThrow(() -> {
            instance.add(1, 1);
        });
    }

    @Test
    public void testSubtract() {
        assertDoesNotThrow(() -> {
            instance.subtract(1, 1);
        });
    }

    @Test
    public void testDivide() {
        assertDoesNotThrow(() -> {
            instance.divide(1, 1);
        });
    }

}
