from functions.get_files_info import get_file_content

test_1 = get_file_content("calculator", "main.py")
print(test_1)

test_2 = get_file_content("calculator", "pkg/calculator.py")
print(test_2)

test_3 = get_file_content("calculator", "/bin/cat")
print(test_3)
