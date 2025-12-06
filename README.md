# DataViz

A lightweight Python library for interactive data exploration and automatic insights, inspired by Mito and Lux.

## Features

- 📊 Interactive spreadsheet view of your data
- 💡 Automatic insight generation
- 📈 Smart visualization recommendations
- 🔍 Data quality analysis
- 🎯 Zero configuration required

## Installation

```bash
pip install -e .
```

## Quick Start

```python
import pandas as pd
from dataviz import analyze

# Load your data
df = pd.read_csv('your_data.csv')

# Create DataViz object
dv = analyze(df)

# View data
dv.show()

# Get insights
dv.insights()

# Get visualization recommendations
dv.visualize()
```

```bash
from dataviz import analyze
import pandas as pd

df = pd.read_csv('data.csv')
dv = analyze(df)

# Auto-generate 6 smart visualizations
dv.visualize(max_plots=6)

# Or use specific plots
dv.plot_correlation()
dv.plot_scatter('x', 'y', hue='category')
dv.plot_pairplot(columns=['a', 'b', 'c'], hue='group')
```

