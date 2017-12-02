import matplotlib.pyplot as plt
import pandas as pd

file = r'tst1BPM.csv'
df = pd.read_csv(file)
df.set_index("time", inplace=True)
print(df.head())
print('Max', df['bpm'].max())
print('Min', df['bpm'].min())
df.plot()
plt.show()
