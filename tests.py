from functions.get_files_info import run_python_file

test_1 = run_python_file("calculator", "main.py")
print(test_1)

test_2 = run_python_file("calculator", "tests.py")
print(test_2)

test_3 = run_python_file("calculator", "../main.py")
print(test_3)

test_4 = run_python_file("calculator", "nonexistent.py")
print(test_4)
