import csv
import json
import numpy as np

def readFromJSON(fileName):
    """
    Reads files from a JSON-file and returns the values read from the files.
    Input: 'fileName' String Filename (must be '.csv')
    Output: 'values' List of values read from the csv-file
    """
    
    try:    
        jsonFile = open(fileName)
    except:
        raise Exception("Could not open file. Ensure filename is correct.")
    
    jsonData = json.load(jsonFile)
    
    values = []
    
    values.append(jsonData['additional'][0]['gasconstant'])
    values.append(jsonData['additional'][1]['mass'])
    values.append(jsonData['temperature'][0]['hot'])
    values.append(jsonData['temperature'][1]['regenerator'])
    values.append(jsonData['temperature'][2]['cold'])
    values.append(jsonData['volume'][0]['swept'])
    values.append(jsonData['volume'][1]['regenerator'])
    values.append(jsonData['volume'][2]['average'])
    values.append(jsonData['area'][0]['piston'])
    values.append(jsonData['area'][1]['cylinder'])
    values.append(jsonData['additional'][2]['phaseangle'])
        
    jsonFile.close()
    
    print(values)
    
    return values

# Remove the possibility to remove 'readFromCSV'?

def writeToJSON(fileName, values):
    """
    Writes a matrix to a JSON-file with the fiven filename.
    Input: 'fileName' String Filename (does not include '.json')
    'values' List containing string values from GUI-input
    """
    try:
        # Convert to dict?
        gasConstant = str(values[0])
        mass = str(values[1])
        tHot = str(values[2])
        tReg = str(values[3])
        tCold = str(values[4])
        sweptVol = str(values[5])
        regVol = str(values[6])
        avgVol = str(values[7])
        rodArea = str(values[8])
        cylArea = str(values[9])
        phaseAngle = str(values[10])
    except:
        print("Missing required values.")
    
    jsonString = ("{\"volume\":[{\"swept\":" + sweptVol + 
                  "},{\"regenerator\":" + regVol +
                  "},{\"average\":" + avgVol +
                  "}],\"area\":[{\"piston\":" + rodArea +
                  "},{\"cylinder\":" + cylArea + 
                  "}],\"temperature\":[{\"hot\":" + tHot +
                  "},{\"regenerator\":" + tReg +
                  "},{\"cold\":" + tCold +
                  "}],\"additional\":[{\"gasconstant\":" + gasConstant +
                  "},{\"mass\":" + mass +
                  "},{\"phaseangle\":" + phaseAngle + "}]}")
    try:    
        with open("assets/" + fileName + ".json", 'w') as jsonFile:
            print(fileName)
            jsonFile.write(jsonString)
    except:
        print("Could not write to file. Ensure proper filename is given.")

def readFromCSV(fileName):
    """
    Reads files from a CSV-file and returns the values read from the files.
    Input: 'fileName' String Filename (must be '.csv')
    Output: 'values' List of values read from the csv-file
    """

    try:
        name = open(fileName)
    except:
        raise Exception("Could not open file. Ensure filename is correct.")
   
    csvReader = csv.reader(name)
    values = []
    
    try:
        for line in csvReader:
            readLine = line[0].split(";")
            values.append(float(readLine[1]))
    except:
        raise Exception("Could not read values. Ensure the values are correct and correctly placed.")
    
    return values

def writeToCSV(fileName, values):
    """
    Writes a matrix to a csv-file with the fiven filename.
    Input: 'fileName' String Filename (does not include '.csv')
    'values' List containing string values from GUI-input
    """

    valueArray = np.array(values)
    titleArray = np.array(["m", "Th", "Tr", "Tc", "V_cyl", "V_reg", "V_c_avg", "piston_rod_area", "piston_cyl_area", "beta"])

    writeArray = np.zeros((10,2), dtype='U20')

    for i in range(len(titleArray)):
        writeArray[i,0] = titleArray[i]
        writeArray[i,1] = str(valueArray[i])
    
    filePath = "assets/" + fileName + ".csv"
    
    try:
        np.savetxt(filePath, writeArray, delimiter=";", fmt='%s')
    except:
        raise Exception("Could not write to file. Ensure the file-name and list of values are correct.")

def writeResultsToCSV(fileName, resultMatrix):
    """
    Writes a matrix to a csv-file with the given filename.
    Input: 'fileName' String containing desired filename for CSV-file containing results from a Schmidt-analysis. Must not include path or '.csv'.
    'resultMatrix' Numpy array containing results from a Schmidt-analysis
    """
    
    filePath = "results/" + fileName + ".csv"
    try:
        np.savetxt(filePath, resultMatrix, delimiter=";")
        print("The results are saved in: " + filePath)
    except:
        raise Exception("Could not write to file. Ensure the file-name and matrix are correct.")