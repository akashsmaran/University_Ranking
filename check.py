import pandas as pd
df = pd.read_csv("CS.csv",delimiter=',')
y = df.loc[df[' Institution'] == " carnegie mellon university"]
print(y)