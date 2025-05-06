# Urinary System Disease Diagnosis

This project provides tools for the presumptive diagnosis of two diseases of the urinary system: acute inflammation of the urinary bladder and acute nephritis of renal pelvis origin.

## Project Structure

- `data_clean.py` - Script for cleaning and preprocessing the raw data
- `diagnosis.data` - Original dataset
- `diagnosis.names` - Dataset description and metadata
- `diagnosis_cleaned.csv` - Cleaned dataset
- `eda.py` - Exploratory Data Analysis script
- `eda_results/` - Directory containing EDA output files and visualizations
- `interactive_viz.py` - Interactive dashboard for visualization and diagnosis

## Data Cleaning

The data cleaning script handles:
- Loading data with proper encoding (UTF-16)
- Converting temperature values from comma to dot format
- Converting categorical variables to appropriate data types
- Checking for missing values and duplicates

Run the data cleaning script:
```
python data_clean.py
```

## Exploratory Data Analysis

The EDA script generates:
- Temperature distribution analysis by disease
- Symptom correlation analysis
- Symptom frequency analysis for each disease
- Diagnostic insights and guidelines

Run the EDA script:
```
python eda.py
```

## Interactive Visualization Dashboard

The interactive dashboard provides:
1. **Temperature vs. Symptoms Interactive Exploration**: Visualize relationships between temperature, symptoms, and diagnoses.
2. **Temperature Distribution Analysis**: Compare temperature ranges across different diagnoses.
3. **Symptom Correlation Heatmap**: Understand relationships between symptoms and diagnoses.
4. **Symptom Frequency Analysis**: Compare symptom prevalence in patients with and without each condition.
5. **Interactive Diagnostic Tool**: Input patient parameters and get a presumptive diagnosis.

### Running the Interactive Dashboard

1. Make sure you have installed the required packages:
```
pip install dash plotly pandas numpy
```

2. Run the interactive dashboard:
```
python interactive_viz.py
```

3. Open your web browser and navigate to:
```
http://127.0.0.1:8050/
```

## Key Findings

- **Bladder Inflammation**: Characterized by urinary symptoms (urine pushing, micturition pains) with moderate fever (mean 38.3°C)
- **Nephritis**: Distinguished by lumbar pain and higher fever (mean 40.3°C)
- Temperature is a key differentiator between the two conditions
- Specific symptom patterns can provide reliable presumptive diagnosis 