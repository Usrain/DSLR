import pandas as pd
import seaborn as sns
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
    if "Index" in df.columns:
        df = df.drop(columns=["Index"])
    house_col = df["Hogwarts House"]
    df_numeric = df.select_dtypes(include=["float64", "int64"])
    df_numeric["Hogwarts House"] = house_col
    sns.pairplot(
        df_numeric, 
        hue="Hogwarts House",
        diag_kind="kde",
        plot_kws={'alpha': 0.5, 's': 20}
    )
    plt.show()

if __name__ == "__main__":
    main()