import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
file_path = 'data/rent.csv'  # Change this to your actual file path
df = pd.read_csv(file_path)

# Drop the unnecessary first row and reset the index
df_cleaned = df.drop(index=0).reset_index(drop=True)

# Rename the columns for better readability
df_cleaned.columns = [
    'Year', 'Moda_m2', 'Media_m2', 'Madrid_m2', 'Madrid_Price', 
    'Madrid_m2_max_FPU', 'Madrid_m2_max_PIF', 'Barcelona_m2', 'Barcelona_Price', 
    'Barcelona_m2_max_FPU', 'Barcelona_m2_max_PIF', 'Valencia_m2', 'Valencia_Price',
    'Valencia_m2_max_FPU', 'Valencia_m2_max_PIF', 'Unnamed_15', 'Sueldo_medio_FPU', 
    'Alquiler_x_mes_FPU', 'Sueldo_medio_PIF', 'Alquiler_x_mes_PIF'
]

# Dropping the unnamed column which seems to have irrelevant or missing data
df_cleaned = df_cleaned.drop(columns=['Unnamed_15'])

# Function to clean numeric columns by removing currency symbols and converting to numeric
def clean_numeric_column(column):
    return column.replace({'€': '', '\.': '', ',': '.'}, regex=True).str.strip().apply(pd.to_numeric, errors='coerce')

# Apply the cleaning function to the relevant columns
for column in ['Madrid_Price', 'Barcelona_Price', 'Valencia_Price', 
               'Alquiler_x_mes_FPU', 'Alquiler_x_mes_PIF', 'Sueldo_medio_FPU', 'Sueldo_medio_PIF']:
    df_cleaned[column] = clean_numeric_column(df_cleaned[column])

######## Plot 1: Madrid, Barcelna and Valencia max m2 prices by FPU
# Function to clean the m2 columns by removing non-numeric characters and converting to float
def clean_m2_column(column):
    # Ensure the column is treated as string, then clean it
    return column.astype(str).str.extract('(\d+,\d+)')[0].str.replace(',', '.').astype(float)

# Remove row for 2023 as it has missing data
df_cleaned = df_cleaned[df_cleaned['Year'] != 2023]

# Clean the m2 columns for Madrid, Barcelona, and Valencia
df_cleaned['Madrid_m2_max_FPU'] = clean_m2_column(df_cleaned['Madrid_m2_max_FPU'])
df_cleaned['Barcelona_m2_max_FPU'] = clean_m2_column(df_cleaned['Barcelona_m2_max_FPU'])
df_cleaned['Valencia_m2_max_FPU'] = clean_m2_column(df_cleaned['Valencia_m2_max_FPU'])

plt.figure(figsize=(10, 6))

plt.plot(df_cleaned['Year'], df_cleaned['Madrid_m2_max_FPU'], label='Madrid m2 max FPU', marker='o')
plt.plot(df_cleaned['Year'], df_cleaned['Barcelona_m2_max_FPU'], label='Barcelona m2 max FPU', marker='o')
plt.plot(df_cleaned['Year'], df_cleaned['Valencia_m2_max_FPU'], label='Valencia m2 max FPU', marker='o')

plt.ylim(0, 75)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Max m² affordable (FPU)')
plt.title('Maximum m² Affordable for FPU Scholarship Holders in Madrid, Barcelona, and Valencia')
plt.legend()

# Display the plot
plt.grid(True)
# Save plot in results
plt.savefig('results/rent-analysis-FPU.png')
plt.show()



########## Plot 2: Madrid, Barcelna and Valencia max m2 prices by PIF
# Clean the m2 columns for Madrid, Barcelona, and Valencia
df_cleaned['Madrid_m2_max_PIF'] = clean_m2_column(df_cleaned['Madrid_m2_max_PIF'])
df_cleaned['Barcelona_m2_max_PIF'] = clean_m2_column(df_cleaned['Barcelona_m2_max_PIF'])
df_cleaned['Valencia_m2_max_PIF'] = clean_m2_column(df_cleaned['Valencia_m2_max_PIF'])

plt.figure(figsize=(10, 6))

plt.plot(df_cleaned['Year'], df_cleaned['Madrid_m2_max_PIF'], label='Madrid m2 max PIF', marker='o')
plt.plot(df_cleaned['Year'], df_cleaned['Barcelona_m2_max_PIF'], label='Barcelona m2 max PIF', marker='o')
plt.plot(df_cleaned['Year'], df_cleaned['Valencia_m2_max_PIF'], label='Valencia m2 max PIF', marker='o')

plt.ylim(0, 75)

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Max m² affordable (PIF)')
plt.title('Maximum m² Affordable for PIF Scholarship Holders in Madrid, Barcelona, and Valencia')
plt.legend()

# Display the plot
plt.grid(True)

# Save plot in results
plt.savefig('results/rent-analysis-plot-PIF.png')
plt.show()



########## Plot 3: 30% of salary spent on rent by FPU and PIF
# Rename the columns related to salary and rent data
df_fpu_pif = df[['Unnamed: 0', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18', 'Unnamed: 19']].copy()

# Assign proper column names
df_fpu_pif.columns = ['Year', 'Sueldo medio FPU', '30% alquiler x mes - FPU', 'Sueldo medio PIF', '30% alquiler x mes - PIF']

# Filter the rows to keep only years from 2013 to 2022
df_fpu_pif = df_fpu_pif[df_fpu_pif['Year'].between(2013, 2022)]

# Clean the columns by removing non-numeric characters (like €) and converting commas to dots
for column in ['Sueldo medio FPU', '30% alquiler x mes - FPU', 'Sueldo medio PIF', '30% alquiler x mes - PIF']:
    df_fpu_pif[column] = pd.to_numeric(df_fpu_pif[column].replace({'€': '', ',': '.'}, regex=True), errors='coerce')

# Assuming df_fpu_pif already contains the relevant data and is cleaned
# Plotting the data
plt.figure(figsize=(10, 6))

# Plot the "30% alquiler x mes - FPU" line
plt.plot(df_fpu_pif['Year'], df_fpu_pif['30% alquiler x mes - FPU'], label='FPU', marker='o')

# Plot the "30% alquiler x mes - PIF" line
plt.plot(df_fpu_pif['Year'], df_fpu_pif['30% alquiler x mes - PIF'], color= 'pink' ,label='PIF', marker='o')

# Highlight the years where FPU and PIF values are the same
equal_values = df_fpu_pif[df_fpu_pif['30% alquiler x mes - FPU'] == df_fpu_pif['30% alquiler x mes - PIF']]

if not equal_values.empty:
    plt.scatter(equal_values['Year'], equal_values['30% alquiler x mes - FPU'], color='purple', label='FPU = PIF', zorder=5)

# Add scatter points to years 2019, 2020, and 2021
years = [2019, 2020, 2021]
plt.scatter(df_fpu_pif[df_fpu_pif['Year'].isin(years)]['Year'],
            df_fpu_pif[df_fpu_pif['Year'].isin(years)]['30% alquiler x mes - FPU'],
            color='purple', zorder=5)
            

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Money spent on rent (€)')
plt.title('30% of Salary Spent on Rent (FPU vs PIF)')
plt.legend()
# Display the plot
plt.grid(True)
plt.savefig('results/rent-analysis-30percent.png')
plt.show()

