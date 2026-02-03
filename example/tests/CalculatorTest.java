package com.example.calculator;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    
    private Calculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    // Tests for add()
    @Test
    void testAddTwoPositiveNumbers() {
        assertEquals(8, calculator.add(5, 3));
    }

    @Test
    void testAddNegativeNumbers() {
        assertEquals(-8, calculator.add(-5, -3));
    }

    @Test
    void testAddWithZero() {
        assertEquals(5, calculator.add(5, 0));
    }

    // Tests for subtract()
    @Test
    void testSubtractTwoNumbers() {
        assertEquals(7, calculator.subtract(10, 3));
    }

    @Test
    void testSubtractNegativeResult() {
        assertEquals(-7, calculator.subtract(3, 10));
    }

    // Tests for multiply()
    @Test
    void testMultiplyTwoNumbers() {
        assertEquals(15, calculator.multiply(5, 3));
    }

    @Test
    void testMultiplyByZero() {
        assertEquals(0, calculator.multiply(5, 0));
    }

    @Test
    void testMultiplyNegativeNumbers() {
        assertEquals(15, calculator.multiply(-5, -3));
    }

    // Tests for divide()
    @Test
    void testDivideTwoNumbers() {
        assertEquals(5.0, calculator.divide(10, 2), 0.001);
    }

    @Test
    void testDivideByZeroThrowsException() {
        assertThrows(ArithmeticException.class, () -> calculator.divide(10, 0));
    }

    @Test
    void testDivideWithDecimalResult() {
        assertEquals(3.333, calculator.divide(10, 3), 0.001);
    }

    // Tests for power()
    @Test
    void testPowerCalculation() {
        assertEquals(8.0, calculator.power(2, 3), 0.001);
    }

    @Test
    void testPowerOfZero() {
        assertEquals(1.0, calculator.power(5, 0), 0.001);
    }

    @Test
    void testNegativeExponent() {
        assertEquals(0.25, calculator.power(2, -2), 0.001);
    }

    // Tests for squareRoot()
    @Test
    void testSquareRoot() {
        assertEquals(4.0, calculator.squareRoot(16), 0.001);
    }

    @Test
    void testSquareRootOfNegativeThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> calculator.squareRoot(-4));
    }

    @Test
    void testSquareRootOfZero() {
        assertEquals(0.0, calculator.squareRoot(0), 0.001);
    }

    // Tests for factorial()
    @Test
    void testFactorial() {
        assertEquals(120, calculator.factorial(5));
    }

    @Test
    void testFactorialOfZero() {
        assertEquals(1, calculator.factorial(0));
    }

    @Test
    void testFactorialOfOne() {
        assertEquals(1, calculator.factorial(1));
    }

    @Test
    void testFactorialOfNegativeThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> calculator.factorial(-5));
    }
}
