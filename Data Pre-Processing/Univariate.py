import pandas as pd
import numpy as np
class Univariate():

    #Find QualQuan
    def qualQuan(dataset):
        qual = []
        quan = []
        for columnName in dataset.columns:
            if (dataset[columnName].dtype == 'O'):
                qual.append(columnName)
            else:
                quan.append(columnName)
        return qual, quan

    # Generate univariate statistics
    def univariateTable(dataset, quan):
            descriptive = pd.DataFrame(index=["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%", "99%", "Q4:100%", "IQR", "1.5 rule", "Lesser", 
                                          "Greater", "Min", "Max", "Var", "STD"], columns=quan)
            for columnName in quan:
                descriptive.loc["Mean", columnName] = dataset[columnName].mean()
                descriptive.loc["Median", columnName] = dataset[columnName].median()
                descriptive.loc["Mode", columnName] = dataset[columnName].mode()[0]
                descriptive.loc["Q1:25%", columnName] = dataset.describe()[columnName]["25%"]
                descriptive.loc["Q2:50%", columnName] = dataset.describe()[columnName]["50%"]
                descriptive.loc["Q3:75%", columnName] = dataset.describe()[columnName]["75%"]
                descriptive.loc["99%", columnName] = np.percentile(dataset[columnName],99)
                descriptive.loc["Q4:100%", columnName] = dataset.describe()[columnName]["max"]
                descriptive.loc["IQR", columnName] = descriptive.loc["Q3:75%", columnName] - descriptive.loc["Q1:25%", columnName]
                descriptive.loc["1.5 rule", columnName] = 1.5 * descriptive.loc["IQR", columnName]
                descriptive.loc["Lesser", columnName] = descriptive.loc["Q1:25%", columnName] - descriptive.loc["1.5 rule", columnName]
                descriptive.loc["Greater", columnName] = descriptive.loc["Q3:75%", columnName] + descriptive.loc["1.5 rule", columnName]
                descriptive.loc["Min", columnName] = dataset[columnName].min()
                descriptive.loc["Max", columnName] = dataset[columnName].max()
                descriptive.loc["Var", columnName] = dataset[columnName].var()
                descriptive.loc["STD", columnName] = dataset[columnName].std()
            return descriptive

    #checkOutlier
    def checkOutlier(descriptive, quan):
        lesser = []
        greater = []
        for columnName in quan:
            if (descriptive[columnName]["Min"] < descriptive[columnName]["Lesser"]):
                lesser.append(columnName)
            if (descriptive[columnName]["Max"] > descriptive[columnName]["Greater"]):
                greater.append(columnName)
        return lesser, greater

    #Replacing Outlier
    def replaceOutlier(dataset, descriptive, lesser, greater):
        for columnName in lesser:
            dataset[columnName][dataset[columnName]<descriptive[columnName]["Lesser"]] = descriptive[columnName]["Lesser"]
        for columnName in greater:
            dataset[columnName][dataset[columnName]>descriptive[columnName]["Greater"]] = descriptive[columnName]["Greater"]
        return descriptive

    #Create Freqency Table
    def freqTable(dataset, columnName):
        freqTable = pd.DataFrame(columns=["Unique_Values", "Frequency", "Related_Freq", "Cumsum"])
        freqTable["Unique_Values"]=dataset[columnName].value_counts().index
        freqTable["Frequency"]=dataset[columnName].value_counts().values
        freqTable["Related_Freq"] = freqTable["Frequency"]/103
        freqTable["Cumsum"] = freqTable["Related_Freq"].cumsum()
        return freqTable


