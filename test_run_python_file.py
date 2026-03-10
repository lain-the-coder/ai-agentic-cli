from functions.run_python_file import run_python_file

# 1. Standard Usage (No args)
print('run_python_file("calculator", "main.py"):')
print(run_python_file("calculator", "main.py"))
print("-" * 30)

# 2. Passing Arguments (Running a calculation)
print('run_python_file("calculator", "main.py", ["3 + 5"]):')
print(run_python_file("calculator", "main.py", ["3 + 5"]))
print("-" * 30)

# 3. Running internal tests
print('run_python_file("calculator", "tests.py"):')
print(run_python_file("calculator", "tests.py"))
print("-" * 30)

# 4. Security Sandbox Check (Path Traversal)
print('run_python_file("calculator", "../main.py"):')
print(run_python_file("calculator", "../main.py"))
print("-" * 30)

# 5. Missing File Check
print('run_python_file("calculator", "nonexistent.py"):')
print(run_python_file("calculator", "nonexistent.py"))
print("-" * 30)

# 6. File Extension Check
print('run_python_file("calculator", "lorem.txt"):')
print(run_python_file("calculator", "lorem.txt"))
