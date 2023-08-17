import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_csv(file_path):
    return pd.read_csv(file_path)

def add_window_flag_rows(df):
    window_values = df.columns[1:]
    window_row = ['window'] + [col.split('_')[-2] for col in window_values]
    flag_row = ['flag'] + [col.split('_')[-1] for col in window_values]
    
    window_df = pd.DataFrame([window_row], columns=df.columns)
    flag_df = pd.DataFrame([flag_row], columns=df.columns)
    
    return pd.concat([window_df, df, flag_df], ignore_index=True)

def transpose_and_process(df):
    df_T = df.transpose()
    df_T.columns = df_T.iloc[0]
    df_T = df_T[1:]
    
    df_T['type'] = 'test'
    
    df_T['CC*'] = df_T['CC*'].str.replace(r'\s*\([^)]*\)', '', regex=True)
    
    return df_T

def filter_by_window(df, window):
    return df[df['window'] == window]

def plot_scatter(df):
    unique_flags = df['flag'].unique()

    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    plot = sns.scatterplot(x='flag', y='CC*', hue='type', data=df)

    plot.set_title(f"Window {df['window'].unique()[0]}")
    plt.xticks(unique_flags)
    plt.legend(title='type')
    
    plt.show()
    
def process_csv(file_path):
    df = load_csv(file_path)
    df = add_window_flag_rows(df)
    df_T = transpose_and_process(df)
    
    for window in df_T['window'].unique():
        df_window = filter_by_window(df_T, window)
        plot_scatter(df_window)

process_csv('2_flag.csv')