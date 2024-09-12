import streamlit as st
import pandas as pd

# Load the data from the Excel file located in the 'data' folder
file_path = './data/salary_data.xlsx'  # Adjust the file path if necessary

# Read the specific sheets for US and Global salaries
us_processed_df = pd.read_excel(file_path, sheet_name=0)
global_processed_df = pd.read_excel(file_path, sheet_name=1)

conversion_dict = {
    'argentina': 0.00105,
    'australia': 0.65,
    'austria': 1.06,  # Austria uses the Euro
    'bahamas': 1.00,  # Bahamas uses Bahamian dollar pegged to USD
    'belgium': 1.06,  # Belgium uses the Euro
    'brazil': 0.21,
    'bulgaria': 0.55,
    'canada': 0.73,
    'chile': 0.00109,
    'china': 0.14,  # Approximate value for Chinese Yuan to USD
    'colombia': 0.00025,  # Approximate value for Colombian Peso to USD
    'czech republic': 0.046,  # Approximate value for Czech Koruna to USD
    'denmark': 0.14,  # Danish Krone to USD
    'england': 1.31,  # British Pound to USD
    'finland': 1.06,  # Finland uses the Euro
    'france': 1.06,  # France uses the Euro
    'germany': 1.06,  # Germany uses the Euro
    'iceland': 0.007,  # Approximate value for Icelandic Krona to USD
    'india': 0.012,  # Indian Rupee to USD
    'indonesia': 0.000066,  # Indonesian Rupiah to USD
    'iran': 0.000024,  # Iranian Rial to USD
    'ireland': 1.06,  # Ireland uses the Euro
    'italy': 1.06,  # Italy uses the Euro
    'japan': 0.0068,  # Japanese Yen to USD
    'malaysia': 0.23,  # Malaysian Ringgit to USD
    'malta': 1.06,  # Malta uses the Euro
    'mexico': 0.059,  # Mexican Peso to USD
    'morocco': 0.098,  # Moroccan Dirham to USD
    'nepal': 0.0076,  # Nepalese Rupee to USD
    'netherlands': 1.06,  # Netherlands uses the Euro
    'new zealand': 0.59,  # New Zealand Dollar to USD
    'norway': 0.093,  # Norwegian Krone to USD
    'philippines': 0.018,  # Philippine Peso to USD
    'poland': 0.25,  # Polish Zloty to USD
    'portugal': 1.06,  # Portugal uses the Euro
    'puerto rico': 1.00,  # Puerto Rico uses USD
    'russia': 0.011,  # Russian Ruble to USD
    'scotland': 1.31,  # Scotland uses British Pound
    'serbia': 0.0086,  # Serbian Dinar to USD
    'singapore': 0.73,  # Singapore Dollar to USD
    'south africa': 0.052,  # South African Rand to USD
    'spain': 1.06,  # Spain uses the Euro
    'sri lanka': 0.0031,  # Sri Lankan Rupee to USD
    'sweden': 0.093,  # Swedish Krona to USD
    'taiwan': 0.031,  # Taiwanese Dollar to USD
    'thailand': 0.028,  # Thai Baht to USD
    'ukraine': 0.027,  # Ukrainian Hryvnia to USD
    'united kingdom': 1.31  # British Pound to USD
}


def display_us_data(df):
    # For US data: Move department and level of the role to the end of the columns for display purposes
    df_reordered = df[['Job Title', 'Average Salary', 'Minimum Salary', 'Maximum Salary', 'Role Field/Scope', 'Seniority Level']]
    
    # Display the reshaped US data
    st.write(df_reordered)

# --- Display Logic for the Global Data ---
def display_global_data(df):
    # For Global data: Reshape for display only
    reshaped_global_data = []
        
    # Loop through each row to extract non-NA and non-zero salaries
    for index, row in df.iterrows():
        for country in df.columns[3:]:  # Start from the 4th column (after Job Title, Role Field/Scope, Seniority Level)
            salary = row[country]
            if pd.notna(salary) and salary > 0:
                # Convert salary to USD using the conversion rate if available
                conversion_rate = conversion_dict.get(country,1)  # Default to 1 if no conversion rate is found
                salary_in_usd = salary*conversion_rate
                
                reshaped_global_data.append({
                    'Job Title': row['Job Title'],
                    'Country': country,
                    'Salary (USD)': salary_in_usd,
                    'Role Field/Scope': row['Role Field/Scope'],
                    'Seniority Level': row['Seniority Level']
                })
    
    # Convert to DataFrame
    reshaped_global_df = pd.DataFrame(reshaped_global_data)
    
    # Display the reshaped Global data
    st.write(reshaped_global_df)
# Title of the app
st.title('👾 Games Salary Dashboard')

col1, col2, col3 = st.columns([1.5, 1, 1])

# Search bar for job title
with col1:
    search_term = st.text_input('Search by Job Title', '')

# Department/Role filter (multiselect)
with col2:
    departments = pd.concat([us_processed_df['Role Field/Scope'], global_processed_df['Role Field/Scope']]).unique()
    selected_department = st.multiselect('Department', departments)

# Seniority Level filter (multiselect)
with col3:
    levels = pd.concat([us_processed_df['Seniority Level'], global_processed_df['Seniority Level']]).unique()
    selected_level = st.multiselect('Seniority Level', levels)

# --- US Salaries Section ---
st.header('US Salaries')
# Filter the US dataframe based on search and selected filters
us_filtered_df = us_processed_df[us_processed_df['Job Title'].str.contains(search_term, case=False, na=False)]

if selected_department:
    us_filtered_df = us_filtered_df[us_filtered_df['Role Field/Scope'].isin(selected_department)]

if selected_level:
    us_filtered_df = us_filtered_df[us_filtered_df['Seniority Level'].isin(selected_level)]

# Display the filtered US results
display_us_data(us_filtered_df)

# --- Global Salaries Section ---
st.header('Global Salaries')

# Filter the Global dataframe based on search and selected filters
global_filtered_df = global_processed_df[global_processed_df['Job Title'].str.contains(search_term, case=False, na=False)]

if selected_department:
    global_filtered_df = global_filtered_df[global_filtered_df['Role Field/Scope'].isin(selected_department)]

if selected_level:
    global_filtered_df = global_filtered_df[global_filtered_df['Seniority Level'].isin(selected_level)]

# Display the filtered Global results
display_global_data(global_filtered_df)

# Optional: Add a button to export filtered data for both US and Global as CSV
if st.button('Export US Data as CSV'):
    us_filtered_df.to_csv('filtered_us_salaries.csv', index=False)
    st.success('US data exported successfully!')

if st.button('Export Global Data as CSV'):
    global_filtered_df.to_csv('filtered_global_salaries.csv', index=False)
    st.success('Global data exported successfully!')
