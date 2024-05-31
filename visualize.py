import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_csv(file_path):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def list_features(df):
    """List the features of the DataFrame."""
    return df.columns.tolist()

def visualize_dataset(file_path):
    """Visualize data from a CSV file by plotting two user-selected features using a chosen plot type."""
    df = load_csv(file_path)
    features = list_features(df)
    return features

def get_user_input(features):
    """Get two feature names from the user."""
    print("Available features:")
    for idx, feature in enumerate(features):
        print(f"{idx + 1}. {feature}")
    
    while True:
        try:
            x_idx = int(input("Choose the number for the first feature: ")) - 1
            y_idx = int(input("Choose the number for the second feature: ")) - 1
            if x_idx in range(len(features)) and y_idx in range(len(features)) and x_idx != y_idx:
                return features[x_idx], features[y_idx]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers corresponding to the features.")

def get_plot_choice():
    """Get the user's choice for the type of plot."""
    plot_types = {
        1: "Scatter Plot",
        2: "Line Plot",
        3: "Histogram",
        4: "Box Plot",
        5: "Pair Plot"
    }
    print("Available plot types:")
    for key, value in plot_types.items():
        print(f"{key}. {value}")
    
    while True:
        try:
            plot_choice = int(input("Choose the number for the type of plot: "))
            if plot_choice in plot_types:
                return plot_choice
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the plot type.")

def adjust_tick_labels(ax):
    """Adjust the distance between tick labels."""
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')
    ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=10))

def plot_features(df, x_feature, y_feature, plot_choice, file_path):
    """Plot the chosen features using the specified plot type."""
    sns.set_theme(style="whitegrid")
    sns.set_palette("muted")
    
    plt.figure(figsize=(10, 6))
    if plot_choice == 1:
        ax = sns.scatterplot(data=df, x=x_feature, y=y_feature)
        plt.title(f'Scatter Plot of {x_feature} vs {y_feature}')
    elif plot_choice == 2:
        ax = sns.lineplot(data=df, x=x_feature, y=y_feature)
        plt.title(f'Line Plot of {x_feature} vs {y_feature}')
    elif plot_choice == 3:
        plt.figure(figsize=(14, 6))
        plt.subplot(1, 2, 1)
        ax1 = sns.histplot(df[x_feature], kde=True)
        plt.title(f'Histogram of {x_feature}')
        adjust_tick_labels(ax1)
        plt.subplot(1, 2, 2)
        ax2 = sns.histplot(df[y_feature], kde=True)
        plt.title(f'Histogram of {y_feature}')
        adjust_tick_labels(ax2)
        return
    elif plot_choice == 4:
        plt.figure(figsize=(14, 6))
        plt.subplot(1, 2, 1)
        ax1 = sns.boxplot(y=df[x_feature])
        plt.title(f'Box Plot of {x_feature}')
        adjust_tick_labels(ax1)
        plt.subplot(1, 2, 2)
        ax2 = sns.boxplot(y=df[y_feature])
        plt.title(f'Box Plot of {y_feature}')
        adjust_tick_labels(ax2)
        return
    elif plot_choice == 5:
        ax = sns.pairplot(df[[x_feature, y_feature]])
        plt.title(f'Pair Plot of {x_feature} and {y_feature}')
    
    adjust_tick_labels(ax)
    plt.xlabel(x_feature)
    plt.ylabel(y_feature)
    
    # Save the plot as an image file with a unique name
    plot_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_{x_feature}_vs_{y_feature}_{plot_choice}.png"
    plt.savefig(plot_filename)
    print(f"Plot saved as '{plot_filename}' in the current directory.")
    
    plt.show()
