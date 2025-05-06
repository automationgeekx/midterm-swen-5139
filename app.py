import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import numpy as np

# Load the cleaned dataset
df = pd.read_csv("diagnosis_cleaned.csv")

# Convert categorical columns to 0/1 for some visualizations
df_numeric = df.copy()
for col in df.columns:
    if col != 'temperature':
        df_numeric[col] = df_numeric[col].map({'yes': 1, 'no': 0})

# Create the Dash app
app = dash.Dash(__name__, title="Urinary System Disease Diagnosis")
server = app.server  # Needed for deployment

# Define color scheme
colors = {
    'background': '#F9F9F9',
    'text': '#333333',
    'bladder': '#1F77B4',  # Blue
    'nephritis': '#FF7F0E',  # Orange
    'healthy': '#2CA02C',  # Green
    'both': '#D62728',  # Red
    'gridlines': '#DDDDDD'
}

# Create diagnostic categories
df['diagnosis_category'] = 'Unknown'
df.loc[(df['bladder_inflammation'] == 'yes') & (df['nephritis'] == 'no'), 'diagnosis_category'] = 'Bladder Inflammation Only'
df.loc[(df['bladder_inflammation'] == 'no') & (df['nephritis'] == 'yes'), 'diagnosis_category'] = 'Nephritis Only'
df.loc[(df['bladder_inflammation'] == 'yes') & (df['nephritis'] == 'yes'), 'diagnosis_category'] = 'Both Diseases'
df.loc[(df['bladder_inflammation'] == 'no') & (df['nephritis'] == 'no'), 'diagnosis_category'] = 'Healthy'
# Yes
# Create a color mapping
color_mapping = {
    'Bladder Inflammation Only': colors['bladder'],
    'Nephritis Only': colors['nephritis'],
    'Both Diseases': colors['both'],
    'Healthy': colors['healthy']
}

# Layout of the app
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    # Title and description
    html.H1("Interactive Diagnosis of Urinary System Diseases", 
            style={'textAlign': 'center', 'color': colors['text'], 'marginBottom': '10px'}),
    
    html.Div([
        html.P("This dashboard helps in the presumptive diagnosis of acute inflammations of urinary bladder and acute nephritises.",
               style={'textAlign': 'center', 'color': colors['text'], 'fontSize': 16})
    ], style={'marginBottom': '30px'}),

    # First row of visualizations
    html.Div([
        # Scatter plot with temperature vs symptoms
        html.Div([
            html.H3("Temperature vs. Symptoms", style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Dropdown(
                id='symptom-dropdown',
                options=[
                    {'label': 'Nausea', 'value': 'nausea'},
                    {'label': 'Lumbar Pain', 'value': 'lumbar_pain'},
                    {'label': 'Urine Pushing', 'value': 'urine_pushing'},
                    {'label': 'Micturition Pains', 'value': 'micturition_pains'},
                    {'label': 'Burning Urethra', 'value': 'burning_urethra'}
                ],
                value='lumbar_pain',
                clearable=False,
                style={'marginBottom': '10px'}
            ),
            dcc.Graph(id='temperature-symptom-scatter')
        ], style={'width': '48%', 'display': 'inline-block', 'backgroundColor': '#FFFFFF', 
                  'padding': '15px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),

        # Temperature distribution
        html.Div([
            html.H3("Temperature Distribution by Diagnosis", style={'textAlign': 'center', 'color': colors['text']}),
            dcc.RadioItems(
                id='diagnosis-radio',
                options=[
                    {'label': 'All', 'value': 'all'},
                    {'label': 'Bladder Inflammation', 'value': 'bladder_inflammation'},
                    {'label': 'Nephritis', 'value': 'nephritis'}
                ],
                value='all',
                inline=True,
                style={'textAlign': 'center', 'marginBottom': '10px'}
            ),
            dcc.Graph(id='temperature-histogram')
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'backgroundColor': '#FFFFFF', 
                  'padding': '15px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'})
    ], style={'marginBottom': '30px'}),

    # Second row of visualizations
    html.Div([
        # Symptom heatmap
        html.Div([
            html.H3("Symptom Correlation Heatmap", style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Graph(id='symptom-heatmap',
                     figure=px.imshow(
                         df_numeric[['nausea', 'lumbar_pain', 'urine_pushing', 'micturition_pains', 'burning_urethra', 
                                     'bladder_inflammation', 'nephritis']].corr(),
                         labels=dict(color="Correlation"),
                         color_continuous_scale='RdBu_r',
                         zmin=-1, zmax=1
                     ).update_layout(height=500))
        ], style={'width': '48%', 'display': 'inline-block', 'backgroundColor': '#FFFFFF', 
                  'padding': '15px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),

        # Symptom frequency by diagnosis
        html.Div([
            html.H3("Symptom Frequency by Diagnosis", style={'textAlign': 'center', 'color': colors['text']}),
            dcc.Dropdown(
                id='diagnosis-dropdown',
                options=[
                    {'label': 'Bladder Inflammation', 'value': 'bladder_inflammation'},
                    {'label': 'Nephritis', 'value': 'nephritis'}
                ],
                value='bladder_inflammation',
                clearable=False,
                style={'marginBottom': '10px'}
            ),
            dcc.Graph(id='symptom-frequency-bar')
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'backgroundColor': '#FFFFFF', 
                  'padding': '15px', 'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'})
    ], style={'marginBottom': '30px'}),

    # Third row - Interactive diagnostic tool
    html.Div([
        html.H2("Interactive Diagnostic Tool", style={'textAlign': 'center', 'color': colors['text'], 'marginBottom': '20px'}),
        
        # Input parameters for diagnosis
        html.Div([
            html.Div([
                html.Label("Temperature (°C):"),
                dcc.Input(
                    id='input-temperature',
                    type='number',
                    min=35,
                    max=42,
                    step=0.1,
                    value=38.5,
                    style={'width': '100%', 'height': '30px'}
                )
            ], style={'width': '16%', 'display': 'inline-block', 'paddingRight': '10px'}),
            
            html.Div([
                html.Label("Nausea:"),
                dcc.RadioItems(
                    id='input-nausea',
                    options=[{'label': 'Yes', 'value': 'yes'}, {'label': 'No', 'value': 'no'}],
                    value='no',
                    inline=True
                )
            ], style={'width': '16%', 'display': 'inline-block', 'paddingRight': '10px'}),
            
            html.Div([
                html.Label("Lumbar Pain:"),
                dcc.RadioItems(
                    id='input-lumbar-pain',
                    options=[{'label': 'Yes', 'value': 'yes'}, {'label': 'No', 'value': 'no'}],
                    value='no',
                    inline=True
                )
            ], style={'width': '16%', 'display': 'inline-block', 'paddingRight': '10px'}),
            
            html.Div([
                html.Label("Urine Pushing:"),
                dcc.RadioItems(
                    id='input-urine-pushing',
                    options=[{'label': 'Yes', 'value': 'yes'}, {'label': 'No', 'value': 'no'}],
                    value='no',
                    inline=True
                )
            ], style={'width': '16%', 'display': 'inline-block', 'paddingRight': '10px'}),
            
            html.Div([
                html.Label("Micturition Pains:"),
                dcc.RadioItems(
                    id='input-micturition-pains',
                    options=[{'label': 'Yes', 'value': 'yes'}, {'label': 'No', 'value': 'no'}],
                    value='no',
                    inline=True
                )
            ], style={'width': '16%', 'display': 'inline-block', 'paddingRight': '10px'}),
            
            html.Div([
                html.Label("Burning Urethra:"),
                dcc.RadioItems(
                    id='input-burning-urethra',
                    options=[{'label': 'Yes', 'value': 'yes'}, {'label': 'No', 'value': 'no'}],
                    value='no',
                    inline=True
                )
            ], style={'width': '16%', 'display': 'inline-block'})
        ], style={'marginBottom': '20px', 'backgroundColor': '#FFFFFF', 'padding': '15px', 
                  'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'}),
        
        html.Div([
            html.Button('Get Diagnosis', id='diagnose-button', 
                       style={'backgroundColor': '#007BFF', 'color': 'white', 'border': 'none', 
                              'padding': '10px 20px', 'cursor': 'pointer', 'fontSize': '16px',
                              'borderRadius': '5px', 'width': '200px', 'margin': '0 auto', 'display': 'block'})
        ], style={'marginBottom': '20px'}),
        
        # Diagnosis results
        html.Div(id='diagnosis-result', style={'backgroundColor': '#FFFFFF', 'padding': '15px', 'minHeight': '100px', 
                                             'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)', 'textAlign': 'center',
                                             'fontSize': '18px'})
    ], style={'marginBottom': '30px'})
])

# Callbacks for interactivity
@app.callback(
    Output('temperature-symptom-scatter', 'figure'),
    Input('symptom-dropdown', 'value')
)
def update_scatter(symptom):
    fig = px.scatter(
        df, x='temperature', y=symptom,
        color='diagnosis_category',
        color_discrete_map=color_mapping,
        labels={
            'temperature': 'Temperature (°C)',
            symptom: symptom.replace('_', ' ').title()
        },
        title=f'Temperature vs {symptom.replace("_", " ").title()}',
        height=500
    )
    
    fig.update_traces(marker=dict(size=12, line=dict(width=1, color='black')))
    
    # Jitter the y-values for better visualization
    for i, d in enumerate(fig.data):
        y_jitter = np.random.uniform(-0.05, 0.05, size=len(d.y))
        fig.data[i].y = [1 if y == 'yes' else 0 for y in d.y]
        fig.data[i].y = [y + j for y, j in zip(fig.data[i].y, y_jitter)]
    
    fig.update_layout(
        plot_bgcolor='white',
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1],
            ticktext=['No', 'Yes'],
            gridcolor=colors['gridlines']
        ),
        xaxis=dict(gridcolor=colors['gridlines']),
        legend_title_text='Diagnosis',
        hovermode='closest'
    )
    
    return fig

@app.callback(
    Output('temperature-histogram', 'figure'),
    Input('diagnosis-radio', 'value')
)
def update_histogram(diagnosis):
    if diagnosis == 'all':
        fig = px.histogram(
            df, x='temperature', color='diagnosis_category',
            color_discrete_map=color_mapping,
            barmode='overlay',
            opacity=0.7,
            nbins=20,
            histnorm='probability density',
            labels={'temperature': 'Temperature (°C)'},
            title='Temperature Distribution by Diagnosis'
        )
    elif diagnosis == 'bladder_inflammation':
        fig = px.histogram(
            df, x='temperature', color='bladder_inflammation',
            color_discrete_map={'yes': colors['bladder'], 'no': colors['healthy']},
            barmode='overlay',
            opacity=0.7,
            nbins=20,
            histnorm='probability density',
            labels={'temperature': 'Temperature (°C)'},
            title='Temperature Distribution by Bladder Inflammation'
        )
    else:  # nephritis
        fig = px.histogram(
            df, x='temperature', color='nephritis',
            color_discrete_map={'yes': colors['nephritis'], 'no': colors['healthy']},
            barmode='overlay',
            opacity=0.7,
            nbins=20,
            histnorm='probability density',
            labels={'temperature': 'Temperature (°C)'},
            title='Temperature Distribution by Nephritis'
        )
    
    fig.update_layout(
        plot_bgcolor='white',
        xaxis=dict(gridcolor=colors['gridlines']),
        yaxis=dict(gridcolor=colors['gridlines']),
        legend_title_text='Diagnosis',
        height=500
    )
    
    return fig

@app.callback(
    Output('symptom-frequency-bar', 'figure'),
    Input('diagnosis-dropdown', 'value')
)
def update_symptom_frequency(diagnosis):
    symptoms = ['nausea', 'lumbar_pain', 'urine_pushing', 'micturition_pains', 'burning_urethra']
    
    # Calculate percentage of 'yes' for each symptom for positive and negative cases
    positive_cases = df[df[diagnosis] == 'yes']
    negative_cases = df[df[diagnosis] == 'no']
    
    pos_percentages = [positive_cases[symptom].value_counts().get('yes', 0) / len(positive_cases) * 100 for symptom in symptoms]
    neg_percentages = [negative_cases[symptom].value_counts().get('yes', 0) / len(negative_cases) * 100 for symptom in symptoms]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[s.replace('_', ' ').title() for s in symptoms],
        y=pos_percentages,
        name=f'With {diagnosis.replace("_", " ").title()}',
        marker_color=colors['bladder'] if diagnosis == 'bladder_inflammation' else colors['nephritis']
    ))
    
    fig.add_trace(go.Bar(
        x=[s.replace('_', ' ').title() for s in symptoms],
        y=neg_percentages,
        name=f'Without {diagnosis.replace("_", " ").title()}',
        marker_color=colors['healthy']
    ))
    
    fig.update_layout(
        title=f'Symptom Frequency: {diagnosis.replace("_", " ").title()}',
        xaxis_title='Symptom',
        yaxis_title='Percentage of Patients (%)',
        plot_bgcolor='white',
        xaxis=dict(gridcolor=colors['gridlines']),
        yaxis=dict(gridcolor=colors['gridlines']),
        barmode='group',
        height=500
    )
    
    return fig

@app.callback(
    Output('diagnosis-result', 'children'),
    Input('diagnose-button', 'n_clicks'),
    State('input-temperature', 'value'),
    State('input-nausea', 'value'),
    State('input-lumbar-pain', 'value'),
    State('input-urine-pushing', 'value'),
    State('input-micturition-pains', 'value'),
    State('input-burning-urethra', 'value')
)
def make_diagnosis(n_clicks, temperature, nausea, lumbar_pain, urine_pushing, micturition_pains, burning_urethra):
    if n_clicks is None:
        return html.P("Enter patient symptoms and click 'Get Diagnosis' to see results.")
    
    # Simple rule-based model based on our EDA
    # Diagnosis factors based on our analysis
    bladder_factors = {
        'temp_range': temperature < 38.5,
        'urine_pushing': urine_pushing == 'yes',
        'micturition_pains': micturition_pains == 'yes',
        'burning_urethra': burning_urethra == 'yes'
    }
    
    nephritis_factors = {
        'temp_range': temperature >= 38.5,
        'nausea': nausea == 'yes',
        'lumbar_pain': lumbar_pain == 'yes'
    }
    
    # Calculate scores for each condition
    bladder_score = sum([
        2 if symptom == 'urine_pushing' and value else
        1.5 if symptom == 'micturition_pains' and value else
        1 if symptom == 'burning_urethra' and value else
        1 if symptom == 'temp_range' and value else 0
        for symptom, value in bladder_factors.items()
    ])
    
    nephritis_score = sum([
        2 if symptom == 'lumbar_pain' and value else
        1 if symptom == 'nausea' and value else
        2 if symptom == 'temp_range' and value else 0
        for symptom, value in nephritis_factors.items()
    ])
    
    # Normalize scores
    bladder_probability = min(100, int(bladder_score / 5.5 * 100))
    nephritis_probability = min(100, int(nephritis_score / 5 * 100))
    
    # Generate diagnosis results
    result = []
    result.append(html.H3("Diagnostic Results"))
    
    # Temperature range indicator
    if temperature < 38.0:
        temp_indicator = html.Span(f"Temperature {temperature}°C (normal to slightly elevated)", style={'color': colors['healthy']})
    elif temperature >= 38.0 and temperature < 39.0:
        temp_indicator = html.Span(f"Temperature {temperature}°C (moderately elevated - fever)", style={'color': colors['bladder']})
    else:
        temp_indicator = html.Span(f"Temperature {temperature}°C (significantly elevated - high fever)", style={'color': colors['nephritis']})
    
    result.append(html.P([temp_indicator]))
    
    # Results for each condition
    result.append(html.Div([
        html.H4("Diagnostic Probabilities:"),
        html.Div([
            html.Div(f"Bladder Inflammation: {bladder_probability}%", 
                    style={'backgroundColor': colors['bladder'], 'color': 'white', 'padding': '10px', 
                           'margin': '5px', 'borderRadius': '5px', 'display': 'inline-block',
                           'width': '45%', 'textAlign': 'center'}),
            html.Div(f"Nephritis: {nephritis_probability}%", 
                    style={'backgroundColor': colors['nephritis'], 'color': 'white', 'padding': '10px', 
                           'margin': '5px', 'borderRadius': '5px', 'display': 'inline-block',
                           'width': '45%', 'textAlign': 'center'})
        ])
    ]))
    
    # Diagnosis summary
    diagnosis_text = ""
    if bladder_probability >= 70 and nephritis_probability >= 70:
        diagnosis_text = "Likely both Bladder Inflammation and Nephritis"
        color = colors['both']
    elif bladder_probability >= 70:
        diagnosis_text = "Likely Bladder Inflammation"
        color = colors['bladder']
    elif nephritis_probability >= 70:
        diagnosis_text = "Likely Nephritis"
        color = colors['nephritis']
    elif bladder_probability >= 40 or nephritis_probability >= 40:
        diagnosis_text = "Possible urinary system condition - further tests recommended"
        color = '#9467BD'  # Purple
    else:
        diagnosis_text = "Unlikely to have either condition"
        color = colors['healthy']
    
    result.append(html.H4("Summary Diagnosis:", style={'marginTop': '10px'}))
    result.append(html.Div(diagnosis_text, style={'fontWeight': 'bold', 'fontSize': '20px', 'color': color}))
    
    # Key symptoms observed
    symptoms_present = []
    if nausea == 'yes':
        symptoms_present.append("Nausea")
    if lumbar_pain == 'yes':
        symptoms_present.append("Lumbar Pain")
    if urine_pushing == 'yes':
        symptoms_present.append("Urine Pushing")
    if micturition_pains == 'yes':
        symptoms_present.append("Micturition Pains")
    if burning_urethra == 'yes':
        symptoms_present.append("Burning Urethra")
    
    if symptoms_present:
        result.append(html.P([
            "Key symptoms observed: ",
            html.Span(", ".join(symptoms_present), style={'fontWeight': 'bold'})
        ]))
    
    return result

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 