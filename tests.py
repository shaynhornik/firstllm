from functions.run_python import run_python_file

# Test 1
print("Result for main.py")
result1 = run_python_file("calculator", "main.py")
print(result1)

# Test 2
print("\nResult for tests.py")
result2 = run_python_file("calculator", "tests.py")
print(result2)

# Test 3
print("\nResult for ../main.py")
result3 = run_python_file("calculator", "../main.py")
print(result3)

# Test 4
print("\nResult for nonexistant.py")
result3 = run_python_file("calculator", "nonexistent.py")
print(result3)
