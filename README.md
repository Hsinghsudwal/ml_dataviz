# DataViz

A lightweight Python library for interactive data exploration and automatic insights.

## Features
- 🔍 Data quality analysis
- 💡 Automatic insight generation
- 🔧 Code Generation (`generate_code()`)
- ⚡ Code Optimizer (`optimize()`)
- 📊 Chart Builder (`suggest_charts()`)
- 💼 Generate analysis (`export_analysis_code()`)
- 📈 Smart visualization

```bash
!pip install ml-dataviz

## imports
from dataviz import DataViz, analyze

data = DataFrame
dv = analyze(data)
dv.show()
dv.insights()
dv.optimize()
dv.visualize()
dv.generate_code()
# dv.export_analysis_code('my_analysis.py')
dv.suggest_charts()
```

## Installation

```bash
pip install -e .
```

## Quick Start

```python
import pandas as pd
from dataviz import enhanced

# Load your data
df = pd.read_csv('your_data.csv')

# Create DataViz object
dv = analyze(df)

# View first N rows with interactive table
dv.show(n=20)  # default is 20

# Get automatic insights
dv.insights()  # Basic insights (5 by default)
dv.insights(max_insights=10)  # More insights
dv.insights(detailed=True, max_insights=15)  # Comprehensive analysis

# Get optimization suggestions
dv.optimize()

# Control number of charts and visualization recommendations
dv.visualize(max_charts=2)      # Show only 2 charts
dv.visualize(max_charts=6)      # Show 6 charts
dv.visualize(max_charts=10)     # Show 10 charts
dv.visualize(max_charts='all')  # Show all available charts (default)

# Individual plots
dv.plot_distribution('age', kind='hist')  # or 'kde', 'box'
dv.plot_categorical('category', top_n=15)
dv.plot_scatter('x_col', 'y_col', hue='category')
dv.plot_correlation(method='pearson')  # or 'spearman', 'kendall'
dv.plot_pairplot(columns=['col1', 'col2', 'col3'], hue='category')

# Perform operations (these get tracked)
dv.filter(df['col'] > value, "df['col'] > value")
dv.sort_values('col', ascending=False)
dv.drop_missing(['col'])

# Generate code for your operations
dv.generate_code(df_name='my_df', include_load=True)

# Or export complete analysis code
dv.export_analysis_code('my_analysis.py')

# Suggest charts with code snippets
dv.suggest_charts(max_charts=6)  # Get code for 6 charts
dv.suggest_charts(max_charts='all')  # Get all suggestions

# Reset to original DataFrame
dv.reset()

```

