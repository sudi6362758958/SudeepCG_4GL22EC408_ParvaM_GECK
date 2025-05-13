multiples = {3, 6, 9, 12, 15}
print(multiples)    
print(type(multiples)) # set

multiples.add(18) # add an element
print(multiples) 

# multiples.update(21, 24) it will give error
multiples.update([21, 24]) # upading the values using list # add multiple elements
multiples.update((27, 30)) # upading the values using tuple # add multiple elements
print(multiples)

#remove() method is used to remove the specified item
multiples.remove(24) # remove an element
# multiples.remove(22) 
#trying to remove an element which is not present in the set will give error
print(multiples)

#discard() method is used to remove the specified item
multiples.discard(27) # remove an element
multiples.discard(28)  # trying to remove an element which is not present in the set will not give error
print(multiples)

#pop() method is used to remove the First element
multiples.pop() # remove the first element
multiples.pop() 
print(multiples) 

#copy() method is used to create a copy of the set
multiples_of_3 = multiples.copy()
print(multiples_of_3)

# union() method is used to combine two elements of both sets
multiples2 = {2, 4, 6, 8, 10}
multiples3 = {3, 6, 9, 12, 15}
print(multiples2.union(multiples3)) # union of two sets

# intersection() method is used to get the common elements from both sets
multiples2 = {2, 4, 6, 8, 10}
multiples3 = {3, 6, 9, 12, 15}
print(multiples2.intersection(multiples3)) # intersection of two sets
