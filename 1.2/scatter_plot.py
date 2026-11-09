import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    try:
        df = pd.read_csv("dataset/dataset_train.csv")
    except FileNotFoundError:
        print("Error: File not found.")
        return
    except pd.errors.EmptyDataError:
        print("Error: File is empty.")
        return
    subjects = ["Arithmancy", "Astronomy", "Herbology", "Defense Against the Dark Arts", "Divination", "Muggle Studies", "Ancient Runes", "History of Magic", "Transfiguration", "Potions", "Care of Magical Creatures", "Charms","Flying"]
    plt.figure(figsize=(10, 6))
    for subject in subjects:
        for second_subject in subjects:
            if subject != second_subject:
                plt.figure(figsize=(10, 6))
                sns.scatterplot(
                    data=df, 
                    x=subject, 
                    y=second_subject, 
                    hue="Hogwarts House", 
                    alpha=0.7
                )
                plt.title(f"Scatter Plot of {subject} vs {second_subject}")
                plt.legend()
                plt.show()

    
if __name__ == "__main__":
    main()