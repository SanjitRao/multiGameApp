import cs043_lesson2_2
from cs043_lesson2_2.database import Simpledb

db = Simpledb('datafile.txt') #todo FIx somehow
print(db.select_one('Sanjit'))
print("Hello World")
for i in range(5):
    print(i)
    print(i)

run = True

print(str(run) + ' dat.')
