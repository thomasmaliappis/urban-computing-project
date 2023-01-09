import matplotlib.pyplot as plt

# creating the dataset
city_data = {
    'e128Model': 0.656499379322575,
    'e256Model': 0.6258201808831353,
    'e512Model': 0.5917715907075722,
    'ensembleModel': 0.7996098599042383
}

class_data = {
    'e128Model': 0.39989359815570136,
    'e256Model': 0.29916651888632734,
    'e512Model': 0.4162085476148254,
    'ensembleModel': 0.4593012945557723
}

fig, axes = plt.subplots(2, sharex=True)
fig.suptitle('Models\' average f1-scores')
axes[0].bar(list(city_data.keys()), list(city_data.values()), color='#f8ab7d', width=0.4)
axes[0].set(ylabel='F1-score', title='City classification')
axes[0].set_ylim(0.5, 0.9)

axes[1].bar(list(class_data.keys()), list(class_data.values()), color='#f89c7d', width=0.4)
axes[1].set(ylabel='F1-score', title='Land use classification')
axes[1].set_ylim(0.25, 0.5)

plt.savefig('f1_scores.png')
plt.show()
