# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tkinter import filedialog, Tk
import plotly.express as px

def add_window_and_flag_rows(df):
    df.columns = df.columns.str.replace('6_', '6.')
    new_cols = []
    for col in df.columns:
        if len(col) < 41:
            col += '_no-flag'
        new_cols.append(col)
    df.columns = new_cols
    window_values = df.columns[1:]
    window_row = ['window'] + [col.split('_')[-2] for col in window_values]
    flag_row = ['flag more than'] + [col.split('_')[-1] for col in window_values]
    window_df = pd.DataFrame([window_row], columns=df.columns)
    flag_df = pd.DataFrame([flag_row], columns=df.columns)
    
    return pd.concat([window_df, df, flag_df], ignore_index=True)

def open_csv_gui():
  root = Tk()
  root.withdraw()
  
  file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
  
  if not file_paths:
    print("Files are not selected.")
    return
  
  for file_path in file_paths:
    df = pd.read_csv(file_path)
    df_with_window_flag = add_window_and_flag_rows(df)
  return df_with_window_flag

def process_dataframe(df_with_window_flag):
  df_T = df_with_window_flag.transpose()
  df_T.columns = df_T.iloc[0]
  df_T = df_T[1:]
  new_type = input("Insert values for column 'type': ")
  df_T['type'] = new_type
  df_T['CC*'] = df_T['CC*'].str.replace(r'\s*\([^\)]*\)', '', regex=True)
  df_T['Multiplicity'] = df_T['Multiplicity'].str.replace(r'\s*\([^\)]*\)', '', regex=True)
  df_T['SNR'] = df_T['SNR'].str.replace(r'\s*\([^\)]*\)', '', regex=True)  
  df_T['Rsplit (%)'] = df_T['Rsplit (%)'].str.replace(r'\s*\([^\)]*\)', '', regex=True)
  df_T[['Indexed patterns', 'crystals']] = df_T['Indexed patterns/crystals'].str.split('/', expand=True)  
  df_T[['Rfree', 'Rwork']] = df_T['Rfree/Rwork'].str.split('/', expand=True)   
  df_T[['Num. patterns', 'hits']] = df_T['Num. patterns/hits'].str.split('/', expand=True)
  df_T['Indexed crystals/hits'] = df_T['crystals'].astype(float) / df_T['hits'].astype(float)
  return df_T

def plot_custom_scatter(df, chosen_window, y):

  df_T_win = df[df['window'] == chosen_window]
  df_T_win[y] = pd.to_numeric(df_T_win[y])
  desired_order = ['2500', '5000', '7500', '10000', '15000', 'no-flag']
  df_T_win = df_T_win.loc[df_T_win['flag more than'].isin(desired_order)]
  df_T_win = df_T_win.sort_index(key=lambda x: x.map(dict(zip(desired_order, range(len(desired_order))))))
  color_map = {'flag more than': 'red', 
              'static mask': 'forestgreen',
              'dynamic mask w/o non hr': 'navy', 
              'reference': 'plum',
              'dynamic mask with non hr 10': 'orange',
              'dynamic mask with non hr 15': 'royalblue',
              'dynamic mask with non hr 20': 'firebrick'}
              
  fig = px.strip(df_T_win, x='flag more than', y=y, color='type', 
                 color_discrete_map=color_map, orientation='v')
  fig.update_xaxes(categoryorder='array', categoryarray=desired_order)  
  fig.update_layout(title=f"Window {chosen_window}, high-resolution cutoff = 1.5")
  fig.update_traces(marker_size=15, marker_opacity=0.9)
  fig.update_traces(jitter=0)
  fig.update_layout(height = 450, width=950)
  fig.update_layout(showlegend=True)
  fig.update_yaxes(tickformat='.4f')
  #fig.show()
  fig.write_image("{}/{}_{}.png".format('/home/kelmanson/Desktop/test_of_script/', y, chosen_window)) # Change the output path
  #svg = fig.to_image(format="svg")
  #svg_str = svg.decode('utf-8') 

  #with open(f"{y}_{chosen_window}.svg", "w") as f:
  #  f.write(svg_str)

if __name__ == '__main__':
    df_1 = open_csv_gui() 
    df_2 = open_csv_gui()
    df_3 = open_csv_gui()
    df_4 = open_csv_gui()
    df_5 = open_csv_gui()
    df_6 = open_csv_gui()
    df_7 = open_csv_gui()
    df_1 = process_dataframe(df_1)
    df_2 = process_dataframe(df_2)
    df_3 = process_dataframe(df_3)
    df_4 = process_dataframe(df_4)
    df_5 = process_dataframe(df_5)
    df_6 = process_dataframe(df_6)
    df_7 = process_dataframe(df_7)
    df_concat = pd.concat([df_1,df_2,df_3,df_4,df_5,df_6,df_7])
    number = input('Choose the window: ')      # add more lines if more metrics are needed
    plot_custom_scatter(df_concat, f'{number}', 'CC*')
    plot_custom_scatter(df_concat, f'{number}', 'Rsplit (%)')
    plot_custom_scatter(df_concat, f'{number}', 'Rfree')
    plot_custom_scatter(df_concat, f'{number}', 'Rwork')
    plot_custom_scatter(df_concat, f'{number}', 'SNR')