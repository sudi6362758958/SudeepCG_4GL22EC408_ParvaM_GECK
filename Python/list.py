Vegetables = ["carrot","Beetroot", "potato", "cabbage", "onion"]
print(Vegetables)
print(type(Vegetables))

#Append Method
# The append() method adds an item to the end of the list.
Vegetables.append("Tomato")  
print(Vegetables)

#Insert Method
# The insert() method inserts an item at the specified index.
Vegetables.insert(2, "Brinjal")  
print(Vegetables)

#Remove Method
# The remove() method can be used to remove an item from the list.
Vegetables.remove("onion")  
print(Vegetables)

# The pop() method removes the item at the specified index.
# If no index is specified, the pop() method removes the last item in the list.
Vegetables.pop(2)
print(Vegetables)

# The index() method is used to find the index of the current item.
print(Vegetables.index("Tomato"))  # Output: 4

# The clear() method removes all the items from the list.
Vegetables.clear()
print(Vegetables)

# The count() method is used to count all matching items in the list.
Vegetables = ["carrot","Beetroot", "potato", "cabbage", "onion", "carrot"]    
print(Vegetables.count("carrot"))  # Output: 

# The sort() method sorts the list Ascending to Desecendin order.
Vegetables.sort()
print(Vegetables)  # Output: ['Beetroot', 'Brinjal', 'cabbage', 'carrot', 'onion', 'potato']

# The reverse() method reverses the order of the list.(not sorted)
Vegetables.reverse()    
print(Vegetables)  # Output: ['potato', 'onion', 'carrot', 'cabbage', 'Brinjal', 'Beetroot']

# The copy() method returns a copy of the list.
basket = Vegetables.copy()
print(basket) 
basket.append("cauliflowe")
print("------------------")
print(Vegetables)
print(basket)

