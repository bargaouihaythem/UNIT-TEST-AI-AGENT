import { TestBed } from '@angular/core/testing';
import { CalculatorService } from './calculator.service';

describe('CalculatorService', () => {
  let service: CalculatorService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CalculatorService]
    });
    service = TestBed.inject(CalculatorService);
  });

  // Tests for add()
  it('should add two positive numbers', () => {
    expect(service.add(5, 3)).toBe(8);
  });

  it('should add negative numbers', () => {
    expect(service.add(-5, -3)).toBe(-8);
  });

  it('should add zero', () => {
    expect(service.add(5, 0)).toBe(5);
  });

  // Tests for subtract()
  it('should subtract two numbers', () => {
    expect(service.subtract(10, 3)).toBe(7);
  });

  it('should subtract negative result', () => {
    expect(service.subtract(3, 10)).toBe(-7);
  });

  // Tests for multiply()
  it('should multiply two numbers', () => {
    expect(service.multiply(5, 3)).toBe(15);
  });

  it('should multiply by zero', () => {
    expect(service.multiply(5, 0)).toBe(0);
  });

  it('should multiply negative numbers', () => {
    expect(service.multiply(-5, -3)).toBe(15);
  });

  // Tests for divide()
  it('should divide two numbers', () => {
    expect(service.divide(10, 2)).toBe(5);
  });

  it('should throw error when dividing by zero', () => {
    expect(() => service.divide(10, 0)).toThrowError('Division by zero');
  });

  it('should handle decimal division', () => {
    expect(service.divide(10, 3)).toBeCloseTo(3.333, 2);
  });

  // Tests for power()
  it('should calculate power', () => {
    expect(service.power(2, 3)).toBe(8);
  });

  it('should handle power of zero', () => {
    expect(service.power(5, 0)).toBe(1);
  });

  it('should handle negative exponent', () => {
    expect(service.power(2, -2)).toBe(0.25);
  });

  // Tests for squareRoot()
  it('should calculate square root', () => {
    expect(service.squareRoot(16)).toBe(4);
  });

  it('should throw error for negative number', () => {
    expect(() => service.squareRoot(-4)).toThrowError('Cannot calculate square root of negative number');
  });

  it('should handle square root of zero', () => {
    expect(service.squareRoot(0)).toBe(0);
  });

  // Tests for percentage()
  it('should calculate percentage', () => {
    expect(service.percentage(200, 10)).toBe(20);
  });

  it('should handle zero percentage', () => {
    expect(service.percentage(100, 0)).toBe(0);
  });

  // Tests for factorial()
  it('should calculate factorial', () => {
    expect(service.factorial(5)).toBe(120);
  });

  it('should return 1 for factorial of 0', () => {
    expect(service.factorial(0)).toBe(1);
  });

  it('should return 1 for factorial of 1', () => {
    expect(service.factorial(1)).toBe(1);
  });

  it('should throw error for negative factorial', () => {
    expect(() => service.factorial(-5)).toThrowError('Factorial of negative number is undefined');
  });
});
