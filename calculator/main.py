
import sys
from pkg.calculator import Calculator

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py '<expression>'")
        sys.exit(1)
    
    expression = sys.argv[1]
    calculator = Calculator()
    
    try:
        result = calculator.evaluate(expression)
        # Display the result in a nice format
        print(f"┌─────────────┐")
        print(f"│  {expression}  │")
        print(f"│             │")
        print(f"│  =          │")
        print(f"│             │")
        print(f"│  {result}         │")
        print(f"└─────────────┘")
    except Exception as e:
        print(f"Error: {e}")
