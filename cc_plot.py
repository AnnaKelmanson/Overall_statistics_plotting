import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('CC_plot.csv')

windows = ['Window 1', 'Window 2', 'Window 4', 'Window 5',
           'Window 6_1', 'Window 6_2', 'Window 9']

flags = ["no flag", 2500, 5000, 7500, 10000, 15000]

plt.figure(figsize=(12, 8))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

labels = set()
ymins = []

for i, window in enumerate(windows):
    plt.subplot(2, 4, i+1)
    plt.subplots_adjust(wspace=0.3)

    filtered = [col for col in df.columns if window in col]

    for j, fil in enumerate(filtered):
        plt.plot(df['flag'], df[fil], 'o', c=colors[j])

        label = fil.split('(')
        if len(label) > 1:
            label = label[1].split(')')[0]
        else:
            label = ''

        labels.add(label)

    ymins.append(df[filtered].min().min() * 0.95)
    plt.title(window)
    plt.xlabel('Flag_morethan')
    plt.ylabel('СС*')
    plt.xticks(df['flag'], flags)

plt.legend(labels, loc='lower right', bbox_to_anchor=(0.8, 0))

for i, ymin in enumerate(ymins):
    plt.subplot(2, 4, i+1)
    plt.ylim(ymin, 1)

plt.tight_layout()
plt.show()