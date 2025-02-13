import streamlit as st
import pandas as pd

st.header("Incentive Calculator")

inputFile = st.file_uploader("Please Upload the file with renewal Data", type=["xlsx", "xls", "csv"])

if inputFile is not None:
    if inputFile.name.endswith(".csv):
        data = pd.read_csv(inputFile)
    else:
        data = pd.read_excel(inputFile, engine="openpyxl")

    persons = data[data.columns[2]].unique().tolist()
    
    assignedAmounts = []
    targetAchieved = []
    achievedAmounts = []
    
    for i in persons:
        tempDf = data[data[data.columns[2]] == i]
        assignedAmounts.append(tempDf[tempDf.columns[0]].sum())
        tempDf = tempDf[tempDf[tempDf.columns[3]] == "pass"]
        targetAchieved.append(tempDf[tempDf.columns[1]].count())
        achievedAmounts.append(tempDf[tempDf.columns[0]].sum())

    percAchieved = []
    
    for i in range(0, len(persons)):
        percAchieved.append(round(((achievedAmounts[i]/assignedAmounts[i])*100.00),3))
    
    incentiveLogic1 = []
    for i in range(0, len(persons)):
        incentiveLogic1.append(round(assignedAmounts[i] * (percAchieved[i]/100) * ((((percAchieved[i]/100)-0.7)/100) + 0.005)))

    incentiveData = pd.read_excel("incentiveData.xlsx")

    incentiveLogic2 = []
    for i in range(0, len(persons)):
        if percAchieved[i] >= 70.0:
            row = incentiveData[(incentiveData["start_range"] <= percAchieved[i]) & (percAchieved[i] <= incentiveData["end_range"])]
            incentiveLogic2.append(round(assignedAmounts[i] * (percAchieved[i]/100) * (row[row.columns[2]].iloc[0])))
        else:
            incentiveLogic2.append(0.0)

    finalData = pd.DataFrame({
                "Individuals" : persons,
                "incentiveLogic1" : incentiveLogic1,
                "incentiveLogic2" : incentiveLogic2
    })

    st.dataframe(finalData)

# Plot the bar chart
fig, ax = plt.subplots()
x = np.arange(len(df["Individuals"]))
width = 0.4  # Width of the bars

ax.bar(x - width/2, df["incentiveLogic1"], width, label="incentiveLogic1", color='blue')
ax.bar(x + width/2, df["incentiveLogic2"], width, label="incentiveLogic2", color='orange')

# Labels and titles
ax.set_xlabel("Individuals")
ax.set_ylabel("Incentives")
ax.set_title("Comparison of Incentive Logic")
ax.set_xticks(x)
ax.set_xticklabels(df["Individuals"])
ax.legend()

# Show the plot in Streamlit
st.pyplot(fig)











