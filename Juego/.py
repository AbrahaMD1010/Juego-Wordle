import os

archivo = open('lemarios/data4.txt', 'r', encoding="utf-8")

file = os.path.join("lemarios", "data4.txt")

archivo = open(file, 'r', encoding="utf-8")  

print(file)