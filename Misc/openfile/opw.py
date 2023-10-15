filepath_read = "openfile.txt"
filepath_write = "output.txt"
i = 1

with open (filepath_read, "r") as file_read:
	with open(filepath_write, "w") as file_write:
		for line in file_read:
			file_write.write(str(i) + "\n")
			file_write.write(line + "\n")
			i += 1
print ("look inside your folder...")


