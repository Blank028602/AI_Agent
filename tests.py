from functions.get_files_info import write_file

test_1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
print(test_1)

test_2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
print(test_2)

test_3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
print(test_3)
