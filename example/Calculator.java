package com.example.calculator;

/**
 * Simple calculator class with basic arithmetic operations.
 */
public class Calculator {

    /**
     * Adds two numbers.
     */
    public int add(int a, int b) {
        return a + b;
    }

    /**
     * Subtracts b from a.
     */
    public int subtract(int a, int b) {
        return a - b;
    }

    /**
     * Multiplies two numbers.
     */
    public int multiply(int a, int b) {
        return a * b;
    }

    /**
     * Divides a by b.
     * @throws ArithmeticException if b is zero
     */
    public double divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Division by zero");
        }
        return (double) a / b;
    }

    /**
     * Calculates power.
     */
    public double power(double base, int exponent) {
        return Math.pow(base, exponent);
    }

    /**
     * Calculates square root.
     * @throws IllegalArgumentException if n is negative
     */
    public double squareRoot(double n) {
        if (n < 0) {
            throw new IllegalArgumentException("Cannot calculate square root of negative number");
        }
        return Math.sqrt(n);
    }

    /**
     * Calculates factorial.
     * @throws IllegalArgumentException if n is negative
     */
    public long factorial(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("Factorial of negative number is undefined");
        }
        if (n == 0 || n == 1) {
            return 1;
        }
        return n * factorial(n - 1);
    }
}
