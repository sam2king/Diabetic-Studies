# Diabetic Clinical Studies

## Introduction
As a Clinical Research Coordinator, I have always had a fascination with clinical research and so I have decided to make that the focus of my project. The research in question will be on a series of over 20,000 clinical studies. The goal of my project will be to examine the relationship between the year a study was conducted and the conditions that were explored.
Diabetes is a significant global health concern affecting millions of people worldwide. Understanding the trends and patterns in diabetic clinical trials is crucial for advancing treatment options and improving patient outcomes. This analysis will provide valuable insights into how research priorities have evolved over time and help identify potential gaps in diabetes research.

## Research Questions
1.	What overall percentage of the studies were diabetic studies?
2.	How did the concentration of diabetic studies change over the years?

## Methods
1. Import CSVs from clinicaltrials.gov
2. Generate a pandas dataframe
3. Generate visual representations of data to answer research

## Key Finding
1. Diabetes made up 19.9% of all clinical trials making it the most researched medical condition.
2. There has been a gradual downward trend in clinical trials for diabetes research since 2000.

# Limitations
Using such simple terms like diabetes to find research descriptions has very likely left out swaths of information. It is very unlikely that cancer makes up less than 2% of clinical trials. Having over half of the clinical trials falling under other means my filtering methods are too limited. Also a lack of count with the scatter plot means there is little to reflect on the percentage of diabetic studies on for that year.

# Future Work
1. Developing another bar chart using matplotlib based on the count of the overall diabetic studies. This should help round out the gaps left by the scatter plot.
2. Add a bar chart showing count would better round out the data. For my pie chart I will use AI to assist in generating a script that can account for all the different names for cancer and improve my filtering process.
