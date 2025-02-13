import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.header("Incentive Calculator")

# File upload for renewal data
inputFile = st.file_uploader("Please Upload the file with renewal Data", type=["xlsx", "xls", "csv"])

if inputFile is not None:
    # Read the uploaded file based on format
    if inputFile.name.endswith(".csv"):
        data = pd.read_csv(inputFile)
    else:
        data = pd.read_excel(inputFile, engine="openpyxl")

    # Extract unique individuals from the dataset
    persons = data[data.columns[2]].unique().tolist()

    assignedAmounts = []
    targetAchieved = []
    achievedAmounts = []

    for i in persons:
        tempDf = data[data[data.columns[2]] == i].copy()  # Ensure proper filtering
        assignedAmounts.append(tempDf[tempDf.columns[0]].sum())

        tempDf_pass = tempDf[tempDf[tempDf.columns[3]] == "pass"].copy()
        targetAchieved.append(tempDf_pass[tempDf_pass.columns[1]].count())
        achievedAmounts.append(tempDf_pass[tempDf_pass.columns[0]].sum())

    # Calculate percentage achieved
    percAchieved = []
    for i in range(len(persons)):
        if assignedAmounts[i] == 0:
            percAchieved.append(0.0)
        else:
            percAchieved.append(round((achievedAmounts[i] / assignedAmounts[i]) * 100.00, 3))

    # Incentive calculation logic 1
    incentiveLogic1 = []
    for i in range(len(persons)):
        incentive = assignedAmounts[i] * (percAchieved[i] / 100) * ((((percAchieved[i] / 100) - 0.7) / 100) + 0.005)
        incentiveLogic1.append(round(incentive))

    # File upload for incentive data
    incentiveFile = st.file_uploader("Upload Incentive Data", type=["xlsx", "xls"])
    
    if incentiveFile is not None:
        incentiveData = pd.read_excel(incentiveFile, engine="openpyxl")

        # Incentive calculation logic 2
        incentiveLogic2 = []
        for i in range(len(persons)):
            if percAchieved[i] >= 70.0:
                row = incentiveData[(incentiveData["start_range"] <= percAchieved[i]) & 
                                    (percAchieved[i] <= incentiveData["end_range"])]
                
                if not row.empty:
                    incentive = assignedAmounts[i] * (percAchieved[i] / 100) * row[row.columns[2]].iloc[0]
                    incentiveLogic2.append(round(incentive))
                else:
                    incentiveLogic2.append(0.0)
            else:
                incentiveLogic2.append(0.0)

        # Prepare final DataFrame
        finalData = pd.DataFrame({
            "Individuals": persons,
            "incentiveLogic1": incentiveLogic1,
            "incentiveLogic2": incentiveLogic2
        })

        # Display final data
        st.dataframe(finalData)

        # Bar chart visualization
        fig, ax = plt.subplots()
        x = np.arange(len(finalData["Individuals"]))
        width = 0.4

        ax.bar(x - width / 2, finalData["incentiveLogic1"], width, label="Incentive Logic 1", color='blue')
        ax.bar(x + width / 2, finalData["incentiveLogic2"], width, label="Incentive Logic 2", color='orange')

        ax.set_xlabel("Individuals")
        ax.set_ylabel("Incentives")
        ax.set_title("Comparison of Incentive Logic")
        ax.set_xticks(x)
        ax.set_xticklabels(finalData["Individuals"], rotation=45)
        ax.legend()

        st.pyplot(fig)
    else:
        st.warning("Please upload the incentive data file to calculate incentive logic 2.")

