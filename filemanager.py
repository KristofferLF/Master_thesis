import csv
import json
import numpy as np

#region JSON
def readFromJSON(fileName):
    """Reads the input-values from a JSON-file.

    Args:
        fileName (string): Filename of the JSON-file.

    Raises:
        Exception: Could not open file. Ensure filename is correct.

    Returns:
        Dictionary: The input-values extracted from the JSON-file.
    """
    
    try:    
        jsonFile = open(fileName)
    except:
        raise Exception("Could not open file. Ensure filename is correct.")
    
    jsonData = json.load(jsonFile)
    
    values = {
        "gasconstant": jsonData['additional'][0]['gasconstant'],
        "mass": jsonData['additional'][1]['mass'],
        "tExpansion": jsonData['temperature'][0]['expansion'],
        "tRegenerator": jsonData['temperature'][1]['regenerator'],
        "tCompression": jsonData['temperature'][2]['compression'],
        "vSwept": jsonData['volume'][0]['swept'],
        "vRegenerator": jsonData['volume'][1]['regenerator'],
        "vAverage": jsonData['volume'][2]['average'],
        "aPiston": jsonData['area'][0]['piston'],
        "aCylinder": jsonData['area'][1]['cylinder'],
        "phaseangle": jsonData['additional'][2]['phaseangle']
    }
        
    jsonFile.close()
    
    return values

def writeToJSON(fileName, values):
    """Writes the values to a JSON-file.

    Args:
        fileName (string): Filename of the JSON-file to be created.
        values (Dictionary): Dictionary containing the values to be stored in a JSON-file.
    """
    
    gasConstant = str(values["gasconstant"])
    mass = str(values["mass"])
    tHot = str(values["tExpansion"])
    tReg = str(values["tRegenerator"])
    tCold = str(values["tCompression"])
    sweptVol = str(values["vSwept"])
    regVol = str(values["vRegenerator"])
    avgVol = str(values["vAverage"])
    rodArea = str(values["aPiston"])
    cylArea = str(values["aCylinder"])
    phaseAngle = str(values["phaseangle"])
    
    jsonString = ("{\"volume\":[{\"swept\":" + sweptVol + 
                  "},{\"regenerator\":" + regVol +
                  "},{\"average\":" + avgVol +
                  "}],\"area\":[{\"piston\":" + rodArea +
                  "},{\"cylinder\":" + cylArea + 
                  "}],\"temperature\":[{\"expansion\":" + tHot +
                  "},{\"regenerator\":" + tReg +
                  "},{\"compression\":" + tCold +
                  "}],\"additional\":[{\"gasconstant\":" + gasConstant +
                  "},{\"mass\":" + mass +
                  "},{\"phaseangle\":" + phaseAngle + "}]}")
    try:    
        with open("assets/" + fileName + ".json", 'w') as jsonFile:
            print(fileName)
            jsonFile.write(jsonString)
    except:
        print("Could not write to file. Ensure proper filename is given.")
#endregion

#region CSV
def readFromCSV(fileName):
    """Read values from a CSV-file and returns them as a list.

    Args:
        fileName (string): The filename of the CSV-file.

    Raises:
        Exception: Could not open file. Ensure filename is correct.
        Exception: Could not read values. Ensure the values are correct and correctly placed.

    Returns:
        List[float]: List of values.
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

def writeResultsToCSV(fileName, resultArray):
    """Write results of the analyses to a CSV-file.

    Args:
        fileName (string): The filename of the CSV-file.
        resultArray (NumPy.array[float]): NumPy-array containing the results of the analyses.

    Raises:
        Exception: Could not write to file. Ensure the file-name and array are correct.
    """
    
    filePath = "results/" + fileName + ".csv"
    try:
        np.savetxt(filePath, resultArray, delimiter=";")
        print("The results are saved in: " + filePath)
    except:
        raise Exception("Could not write to file. Ensure the file-name and array are correct.")
#endregion