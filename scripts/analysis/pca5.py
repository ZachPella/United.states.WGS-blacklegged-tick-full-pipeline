# Install required packages in Colab if not already installed
# You can uncomment the line below to install them
# !pip install openpyxl seaborn

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set a style for better looking plots
plt.style.use('default')

# --- File Paths ---
# Update these paths if your files are in a different location
tick_file = "/content/tick.xlsx"
eigenval_file = "/content/eigenval.xlsx"
metadata_file = "/content/colors.xlsx"

def load_and_prepare_data(tick_path, eigenval_path, metadata_path):
    """
    Loads PCA data, eigenvalues, and metadata from Excel files,
    then merges and prepares the data for plotting.
    """
    # Load PCA scores and eigenvalues
    pca_scores = pd.read_excel(tick_path)
    eigenval_df = pd.read_excel(eigenval_path)
    eigenval = eigenval_df.iloc[:, 0].values
    pve = (eigenval / eigenval.sum()) * 100

    # Extract PC columns and rename 'Sample' to 'ind'
    pc_columns = [col for col in pca_scores.columns if col.startswith('PC')]
    pca_data = pca_scores[['Sample'] + pc_columns].rename(columns={'Sample': 'ind'})

    # Load and process metadata
    metadata = pd.read_excel(metadata_path)

    # The third column (index 2) contains North/South for Nebraska samples
    third_col_name = metadata.columns[2]
    metadata = metadata.rename(columns={third_col_name: 'North_South'})

    # For Nebraska, group by North/South using the third column
    def assign_group(row):
        if row['State'] == 'Iowa':
            return 'Iowa'
        if row['State'] == 'Kansas':
            return 'Kansas'
        if row['State'] == 'Nebraska':
            if pd.notna(row['North_South']):
                return 'Nebraska North' if row['North_South'] == 'North' else 'Nebraska South'
            else:
                return 'Nebraska'
        return row['State']

    metadata['Location_Group'] = metadata.apply(assign_group, axis=1)

    pca_with_meta = pca_data.merge(metadata[['Sample', 'Location_Group']],
                                   left_on='ind', right_on='Sample', how='left')
    return pca_with_meta, pve

def plot_pca(pca_data, pve, pc1=1, pc2=2):
    """
    Creates and displays a PCA plot for two specified principal components.
    """
    plt.figure(figsize=(14, 10))

    # Color mapping - keys match Location_Group values
    # Color mapping - keys match Location_Group values
    colors = {
        # Northeast / Upper Midwest (vibrant blues, purples, greens)
        "Massachusetts": "#240046",
        "Maryland": "#5a189a",
        "Michigan": "#9d4edd",
        "Wisconsin": "#0d47a1",
        "Minnesota": "#2196f3",
        "Iowa": "#bbdefb",
        # Nebraska
        "Nebraska North": "#ffdab9",
        "Nebraska South": "#95d5b2",
        # Central / Great Plains
        "Kansas": "#ffba08",
        "Oklahoma": "#f08080",
        "Tennessee": "#40916c",
        # Southern gradient
        "South Carolina": "#03071e",
        "Florida": "#6a040f",
        "North Carolina": "#9d0208",
        "Virginia": "#d00000",         # Burnt orange (was Alabama)
        "Alabama": "#e85d04",          # Red-orange (was Virginia)
        "Texas": "#f48c06",           # Sandy brown - lighter, distinct
        "Other": "#808080",
    }

    # Define custom labels for the legend
    label_map = {
        'Nebraska North': 'Nebraska (Thurston county)',
        'Nebraska South': 'Nebraska (Dodge, Douglas, Sarpy county)',
        'South Carolina': 'S. Carolina',
        'North Carolina': 'N. Carolina'
    }

    # Geographic ordering: Northeast on top -> contact zone middle -> Deep South bottom
    # Geographic ordering: Northeast on top -> contact zone middle -> Deep South bottom
    geographic_order = [
        "Maine",
        "Massachusetts",
        "Maryland",
        "Michigan",
        "Wisconsin",
        "Minnesota",
        "Iowa",
        "Nebraska North",
        "Nebraska South",
        "Oklahoma",
        "Tennessee",
        "Kansas",
        "Texas",
        "Alabama",
        # Bottom section
        "Virginia",
        "North Carolina",
        "Florida",
        "South Carolina",
    ]

    present_groups = pca_data['Location_Group'].dropna().unique()

    # Sort by geographic order
    ordered_groups = [g for g in geographic_order if g in present_groups]
    # Add any groups not in the predefined order
    ordered_groups += [g for g in present_groups if g not in ordered_groups]

    for group in ordered_groups:
        group_data = pca_data[pca_data['Location_Group'] == group]
        if not group_data.empty:
            color = colors.get(group, colors['Other'])
            label = label_map.get(group, group)
            label = f'{label} (n={len(group_data)})'

            plt.scatter(group_data[f'PC{pc1}'], group_data[f'PC{pc2}'],
                        c=color, label=label, s=80, alpha=0.85,
                        edgecolors='black', linewidth=0.5)

    plt.xlabel(f'PC{pc1} ({pve[pc1-1]:.1f}%)', fontsize=14, fontweight='bold')
    plt.ylabel(f'PC{pc2} ({pve[pc2-1]:.1f}%)', fontsize=14, fontweight='bold')
    plt.title('PCA Plot - I. scapularis Population Structure', fontsize=16, fontweight='bold')

    plt.legend(title='Location', title_fontsize=12, fontsize=10,
              bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    print("\nSample distribution by state:")
    print("-" * 30)
    for group in ordered_groups:
        count = len(pca_data[pca_data['Location_Group'] == group])
        print(f"{group}: {count} samples")
    print(f"\nTotal samples: {len(pca_data)}")

# --- Main execution block ---
if __name__ == "__main__":
    try:
        pca_with_meta, pve = load_and_prepare_data(tick_file, eigenval_file, metadata_file)
        plot_pca(pca_with_meta, pve)

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e.filename}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
