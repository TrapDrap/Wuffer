import json

#
# JSON LOADERS

def loadJson(fileName):
    with open(fileName,'r') as f:
        fileData=json.load(f)
        f.close()
        return fileData

def saveJson(fileName,newData):
    with open(fileName,'w') as f:
        json.dump(newData,f,indent=2)
        f.close()