import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def perform_eda(file_path):
    df = pd.read_csv(file_path)
    print("Dataset Shape:", df.shape)
    print(df.info())
    print(df.describe())
    
    # Visualise missing values
    sns.heatmap(df.isnull(), cbar=False)
    plt.title("Missing Values Heatmap")
    plt.show()

    # Visualise class distribution
    sns.countplot(x="cancer_subtype", data=df)
    plt.xticks(rotation=45)
    plt.title("Class Distribution")
    plt.show()

    return df
