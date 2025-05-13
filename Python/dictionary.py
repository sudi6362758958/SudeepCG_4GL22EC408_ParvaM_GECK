#tuples
vowels = ( "A","E","I","O","U","a","e","i","o","u")
print(vowels)   
print(type(vowels))


#count method is used to count the number of occurrences of the specified value in the tuple or used to count all the matching values
print(vowels.count("A"))
print(vowels.index("u"))

car = {
    "brand": "Tata",
    "model": "Curvv",
    "year": 2024,
    "variant": [ "Petrol", "Diesel", "EV"],
    "features" : ("A/C", "360 camera", "AB5", "4 Air bags", "Cruise control"),
    "price" : "10L + GST",
}
print(car)
print(type(car))

#get(key) method is used to get the value using key
print(car.get("brand"))
print(car.get("model"))

# keys method is used to list out all the keys used in dictionary
print(car.keys()) #default method will print all the keys within dict_key(
print(list(car.keys())) #specified to print the keys as a list
print(tuple(car.keys())) #specified to print the keys as a tuple

# values method is used to list out all the values used in dictionary
print(car.values()) #default method will print all the values within dict_key(
print(list(car.values())) #specified to print the values as a list
print(tuple(car.values())) #specified to print the values as a tuple

# items method is used to get the key value pairs
print(car.items()) #default method will print all the key value pairs within dict_items(

car.update({
    "colors": ["Red", "Blue", "Black"],
    "country": "India",
})
print(car)

#pop(key) method is used to remove the item using key
car.pop("year")
print(car)

#popitem() method is used to remove the last key value pair of the dictionary
car.popitem()   
print(car)

#copy() method is used to create a copy of the dictionary
new_car = car.copy()
print(new_car)
print("------------------")
new_car.popitem()
print(new_car)
print(car)

#clear() method is used to remove all the key value pair from the dictionary
car.clear()
print(car)
