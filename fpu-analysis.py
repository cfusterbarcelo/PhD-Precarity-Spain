# Importing necessary libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Load CSV files into DataFrames
fpu_df = pd.read_csv('data/fpu.csv')
mean_spain_df = pd.read_csv('data/mean-mode-spain-persex.csv', encoding='latin1', sep=';')

# Remove first row from the DataFrames
fpu_df = fpu_df.iloc[1:]
fpi_df = fpi_df.iloc[1:]
rent_df = rent_df.iloc[1:]

# Renaming the columns for better understanding (you can adjust these based on your actual data)
fpu_df.rename(columns={'Unnamed: 0': 'Government', 
                       'Unnamed: 1': 'Year', 
                       'Unnamed: 6': 'Mean_Salary'}, inplace=True)

# Drop rows with missing salary data, if any
fpu_df = fpu_df.dropna(subset=['Mean_Salary'])

# Convert columns to the correct data types
fpu_df['Year'] = fpu_df['Year'].astype(int)
# Sanitize the salary column by removing the € sign and converting it to float
fpu_df['Mean_Salary'] = fpu_df['Mean_Salary'].str.replace('€', '').str.replace(',', '').str.replace('.', '').astype(float)/100

# Handle the 'PP-PSOE' case by splitting it into two rows (you could adjust this logic if needed)
def split_government(row):
    if 'PP-PSOE' in row['Government']:
        return ['PP', 'PSOE']
    return [row['Government']]

# Apply the split and expand the DataFrame
expanded_rows = []
for _, row in fpu_df.iterrows():
    governments = split_government(row)
    # Half-year for each government
    for gov in governments:
        expanded_row = row.copy()
        expanded_row['Government'] = gov
        expanded_rows.append(expanded_row)

# Create new DataFrame from expanded rows
fpu_df_expanded = pd.DataFrame(expanded_rows)

# Sanitze the "Total" column by removing the € sign and converting it to float
mean_spain_df['Total'] = mean_spain_df['Total'].str.replace('€', '').str.replace(',', '').str.replace('.', '').astype(float)/100

# From mean_spain_df, groupby "Salario anual" and "Periodo" columns and get the mean of "Total"
mean_spain_df = mean_spain_df.groupby(['Salario anual', 'Periodo'])['Total'].mean().reset_index()

mean_spain_salary_df = mean_spain_df[mean_spain_df['Salario anual'] == 'Salario a tiempo completo'].copy()
mode_spain_salary_df = mean_spain_df[mean_spain_df['Salario anual'] == 'Salario más frecuente'].copy()

# Setting up the plot style
sns.set(style="whitegrid")

# Create the plot
plt.figure(figsize=(10, 6))

# Plot FPU Mean Salary
sns.lineplot(data=fpu_df_expanded, x='Year', y='Mean_Salary', marker="o", color='blue', label='FPU Salary', linewidth=2)

# Plot Mean Salary in Spain
sns.lineplot(data=mean_spain_salary_df, x='Periodo', y='Total', marker="o", color='red', label='Mean Salary Spain', linewidth=2)

# Plot Mode Salary in Spain
sns.lineplot(data=mode_spain_salary_df, x='Periodo', y='Total', marker="o", color='green', label='Mode Salary Spain', linewidth=2)

# Customize the plot
plt.title("FPU Salary vs. Spain's Mean and Mode Salaries", fontsize=14)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Annual Salary (€)', fontsize=12)

# Set the y-axis to show whole numbers (full salary values)
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('€%.0f'))

# Show all years in axis x
plt.xticks(fpu_df_expanded['Year'].unique())

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add grid for easier interpretation
plt.grid(True)

# The legend is automatically handled by sns.lineplot(label=...)
plt.legend()

# Show the plot
plt.tight_layout()
plt.savefig('results/fpu_salary_vs_spain_salaries.png')
plt.show()

