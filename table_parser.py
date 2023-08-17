import pandas as pd
from tkinter import filedialog

filenames = filedialog.askopenfilenames()

dfs = []

for f in filenames:

  df = pd.read_csv(f, sep=';', index_col=0)

  parts = df.columns[0].split('_')
  window = parts[4]
  df.loc['window'] = [window] * len(df.columns)


  dfs.append(df)


for df in dfs:
  
  print(df.to_string()) # Конверт в строку

  print('\n') # Пустая строка между DataFrame