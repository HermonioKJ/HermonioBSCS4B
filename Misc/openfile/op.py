filepath = "openfile.txt"
i = 1

with open (filepath, 'r') as my_file:
	for line in my_file:
		print(i)
		print(line)
		i += 1
