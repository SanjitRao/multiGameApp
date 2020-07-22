import random
import os
class Simpledb:

    def __init__(self,fileName):
        
        self.fileName = fileName
        

    def __repr__(self):
        return  ("<Simpledb file=" + str(self.fileName) + ">")
    
    #datafile = open('datafile.txt')
        
    #This code will check if the key already exists in the database, but will not
    #check keys with SPACES properly.
    def insert(self, key, value):
        
        f = open(self.fileName, 'r')
        row = f.readlines()
        for item in row:
            indivEntry = item.split() 
            while indivEntry[0] == key:
                key = input("This key already exists. Please enter a new key. ")
                value = input("Please enter a phone number. ")    
            
        f = open(self.fileName, 'a')
        f.write(key + '\t' + value + '\n')
        f.close()
        return True


    def select_one(self, key):
        
        listEntries = 0
        returnList = [True]
        f = open(self.fileName, 'r+')
        for row in f:
            row = row[:-1]
            (k, v) = row.split('\t', 1)
            if k == key:
                listEntries +=1
                returnList.append(v)
                return returnList
        if listEntries == 0:
            returnList[0] = False
            return returnList
    #This is dodgy... I wanna see what happens if there are two Johns...
        f.close()

    def delete(self, key):
        f = open(self.fileName, 'r')
        result = open('result.txt', 'w')
        for row in f:
            row = row[:-1]
            (k, v) = row.split('\t', 1)
            if k != key:
                result.write(row)
                
        f.close()
        result.close()
        
        os.replace('result.txt', self.fileName)###
        return True

    def update(self, key, value):
        f = open(self.fileName, 'r')
        result = open('result.txt', 'w')
        for row in f:
            (k, v) = row.split('\t', 1)
            if k == key:
                result.write(key + '\t' + value + '\n')
            else:
                result.write(row)
        f.close()
        result.close()
        
        os.replace('result.txt', self.fileName)###
        return True

    #I don't know if this one will work...
    '''def update(datafile, key, value): 
        f = open(datafile, 'r+')
        for row in f:
            (k, v) = row.split('\t', 1)
            if k == key:
                v = value
        f.close()'''











    
