#Arthmatic Operaters
num1 = 5
num2 = 10
print("sum: ", num1 + num2)
print("difference: ", num1 - num2)
print("Product: ", num1 * num2)
print("Quotient: ", num1 / num2)
print("Remainder/Modulus: ", num1 % num2)
print("Exponent: ", num1 ** 3)
print("normal division: ", num2 / 3)
print("Floor Division: ", num2 // 3)

# Relational Operaters
print(num1 > num2)
print(num1 < num2)
print(num1 >= num2)
print(num1 <= num2)
print(num1 == num2)
print(num1 != num2)

num3 = "10"
print(num2 == num3)

# Assignment Operaters
num1+= 5        # num1 = num1 + 5
print(num1) 
num1-= 5        # num1 = num1 - 5
print(num1) 
num1*= 5    # num1 = num1 * 5
print(num1)
num1/= 5    
print(num1)
num1%= 5    # num1 = num1 % 5
print(num1)
num1**= 5   # num1 = num1 ** 5
print(num1)
num1//= 5   # num1 = num1 // 5
print(num1)

# Logical Operaters
num1 = 5
print(num1)
print(num1 > 2 and num1 < 6)
print(num1 > 2 or num1 < 6)
print(not(num1 > 2 and num1 < 6))

# Identity Operaters
list1 = [2, 4, 6, 8, 10]
list2 = [2, 4, 6, 8, 10]
list3 = list1
print("----------")
print(list1 is list2)  # False
print(list1 is list3)  # True
print(list1 is not list2)  # True
print(list1 == list2)  # True

# Membership Operaters
print("----------")
print(6 in list1)   # True
print(5 in list2)   # False
print(5 not in list2) # True
