import pandas as pd

# Load the dataset
df = pd.read_csv(r"C:\Users\Lenovo\Desktop\Nethmi\Data Science\DSPL_Individual\social-protection-and-labor_lka.csv")
print(df.head())
print(df.shape)

# Drop the metadata row
df = df[1:]
# Reset index
df.reset_index(drop=True, inplace=True)

# Clean column names 
df.columns = df.columns.str.strip()
# Initial check
print("Initial Columns:", df.columns.tolist())
# Drop columns
df.drop(columns=['Country Name', 'Country ISO3'], inplace=True)
# Confirm update
print("Updated Columns:", df.columns.tolist())

print(df.head())
print(df.shape)

# Check for duplicates
print("Number of duplicate rows:", df.duplicated().sum())

# Convert Year to int and Value to float
df['Year'] = df['Year'].astype(int)
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

# Check missing values
print(df.isnull().sum())

# Show unique indicators
unique_indicators = df['Indicator Name'].unique()
print(f"\nNumber of unique indicators: {len(unique_indicators)}")
print("Sample indicators:")
print(unique_indicators[:10])  
# Show year range
min_year = df['Year'].min()
max_year = df['Year'].max()
print(f"\nTime range: {min_year} to {max_year}")

# Save cleaned data
df.to_csv(r"C:\Users\Lenovo\Desktop\Nethmi\Data Science\DSPL_Individual\cleaned_data.csv", index=False)
print("Preprocessing complete. Saved to cleaned_data.csv")
