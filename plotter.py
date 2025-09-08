import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")


# shows how attempts changed overtime
def plotAttemptsTimeline(data):
    plt.figure(figsize=(12, 6))  # width=12in, height=6in

    plt.plot(data['year'], data['attemptsPerGame'],
             linewidth=2, color='blue', marker='o', markersize=4)

    # add colored backgrounds for diff eras - alpha=transparency level
    plt.axvspan(1984, 1997, alpha=0.2, color='red', label='Old School')
    plt.axvspan(1997, 2014, alpha=0.2, color='orange', label='Growing Up')
    plt.axvspan(2014, 2023, alpha=0.2, color='green', label='Analytics Era')

    plt.title('3-Point Attempts Have Gone Absolutely Crazy', fontsize=14)
    plt.xlabel('Year')
    plt.ylabel('Attempts Per Game')
    plt.legend()
    plt.grid(True, alpha=0.3)  # alpha makes grid lines semi-transparent
    plt.show()


# compares the diff time periods using boxplots
def plotEraBoxplots(data):
    plt.figure(figsize=(10, 6))

    sns.boxplot(data=data, x='era', y='attemptsPerGame', hue='era', palette='viridis', legend=False)
    plt.title('How Different Eras Compare')
    plt.ylabel('Attempts Per Game')
    plt.xlabel('Basketball Era')
    plt.xticks(rotation=15)  # rotates labels 15 degrees
    plt.show()