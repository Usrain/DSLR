import pandas as pd
import matplotlib.pyplot as plt


def main():
    try:
        df = pd.read_csv("dataset/dataset_train.csv")
    except FileNotFoundError:
        print("Error: File not found.")
        return
    except pd.errors.EmptyDataError:
        print("Error: File is empty.")
        return
    houses = df['Hogwarts House'].unique()
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
    data_to_plot = []
    house_labels = []
    notes = []
    for numerical_column in numerical_columns:
        plt.figure(figsize=(10, 6))
        plt.title(f"Histogram of {numerical_column} by Hogwarts House")
        notes.clear()
        house_labels.clear()
        data_to_plot.clear()
        for house in houses:
            notes = df[df['Hogwarts House'] == house][numerical_column].dropna().tolist()
            data_to_plot.append(notes)
            house_labels.append(house)
        plt.hist(
            data_to_plot, 
            bins=15, 
            label=house_labels
        )
        plt.legend()
        plt.show()

    
if __name__ == "__main__":
    main()