num1 = 8
print ("input the number that will divide:")
num2 =  int(input())


try:


	result = num1 / num2
	print (result)
except ZeroDivisionError:
	print ("Do not divide by zero that is forbidden")
except ValueError:
	print ("Your input value must be an integer")



print ("The program keeps executing to do other stuff..")
