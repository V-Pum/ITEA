file1 = open(input("Enter first file path: "), "r").read()
file2 = open(input("Enter second file path: "), "r").read()
file3 = open(input("Enter resulting file path: "), "w")
file3.write(file1 + "\n" + file2)