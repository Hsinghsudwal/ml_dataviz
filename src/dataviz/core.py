"""
DataViz: Unified data visualization and insights library
Features: Interactive editing, auto-visualizations, code generation, and optimization
"""

import pandas as pd
import numpy as np
from IPython.display import display, HTML, Code
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Dict, Any, Union
import warnings
from textwrap import dedent

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


class CodeGenerator:
    """Generate reproducible pandas code from operations"""
    
    def __init__(self):
        self.operations = []
        
    def add_operation(self, op_type: str, params: Dict[str, Any]):
        """Record an operation"""
        self.operations.append({'type': op_type, 'params': params})
        
    def generate_code(self, df_name: str = 'df') -> str:
        """Generate pandas code from recorded operations"""
        code_lines = [f"import pandas as pd", f"import numpy as np", ""]
        
        for op in self.operations:
            if op['type'] == 'filter':
                condition = op['params']['condition']
                code_lines.append(f"{df_name} = {df_name}[{condition}]")
                
            elif op['type'] == 'sort':
                col = op['params']['column']
                asc = op['params']['ascending']
                code_lines.append(f"{df_name} = {df_name}.sort_values('{col}', ascending={asc})")
                
            elif op['type'] == 'drop_na':
                subset = op['params'].get('subset')
                if subset:
                    code_lines.append(f"{df_name} = {df_name}.dropna(subset={subset})")
                else:
                    code_lines.append(f"{df_name} = {df_name}.dropna()")
                    
            elif op['type'] == 'fill_na':
                col = op['params']['column']
                value = op['params']['value']
                code_lines.append(f"{df_name}['{col}'] = {df_name}['{col}'].fillna({repr(value)})")
                
            elif op['type'] == 'groupby':
                by = op['params']['by']
                agg = op['params']['agg']
                code_lines.append(f"{df_name} = {df_name}.groupby({repr(by)}).agg({agg})")
                
            elif op['type'] == 'add_column':
                col = op['params']['column']
                expr = op['params']['expression']
                code_lines.append(f"{df_name}['{col}'] = {expr}")
                
        return "\n".join(code_lines)
    
    def reset(self):
        """Clear operation history"""
        self.operations = []


class CodeOptimizer:
    """Analyze and suggest code optimizations"""
    
    @staticmethod
    def analyze_dataframe(df: pd.DataFrame) -> List[Dict[str, str]]:
        """Analyze DataFrame and suggest optimizations"""
        suggestions = []
        
        # Memory optimization
        mem_usage = df.memory_usage(deep=True).sum() / 1024**2
        if mem_usage > 100:
            suggestions.append({
                'type': 'memory',
                'severity': 'warning',
                'title': 'High Memory Usage',
                'suggestion': f'DataFrame uses {mem_usage:.2f} MB. Consider optimizing dtypes.',
                'code': CodeOptimizer._generate_dtype_optimization(df)
            })
        
        # String columns to category
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() / len(df) < 0.5:
                suggestions.append({
                    'type': 'dtype',
                    'severity': 'info',
                    'title': f'Optimize {col}',
                    'suggestion': f"Convert '{col}' to category type for better performance",
                    'code': f"df['{col}'] = df['{col}'].astype('category')"
                })
        
        # Vectorization opportunities
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            suggestions.append({
                'type': 'vectorization',
                'severity': 'info',
                'title': 'Vectorization Tips',
                'suggestion': 'Use vectorized operations instead of loops for numeric columns',
                'code': dedent(f"""
                # Instead of: for i in range(len(df)): df.loc[i, 'new'] = df.loc[i, 'col'] * 2
                # Use vectorized:
                df['new_col'] = df['{numeric_cols[0]}'] * 2
                """).strip()
            })
        
        # Index optimization
        if not df.index.is_unique and len(df) > 1000:
            suggestions.append({
                'type': 'index',
                'severity': 'warning',
                'title': 'Non-unique Index',
                'suggestion': 'Set a unique index for faster lookups',
                'code': "df = df.reset_index(drop=True)"
            })
        
        return suggestions
    
    @staticmethod
    def _generate_dtype_optimization(df: pd.DataFrame) -> str:
        """Generate code to optimize dtypes"""
        code_lines = ["# Optimize data types"]
        
        for col in df.select_dtypes(include=['int64']).columns:
            code_lines.append(f"df['{col}'] = pd.to_numeric(df['{col}'], downcast='integer')")
            
        for col in df.select_dtypes(include=['float64']).columns:
            code_lines.append(f"df['{col}'] = pd.to_numeric(df['{col}'], downcast='float')")
            
        return "\n".join(code_lines)


class ChartBuilder:
    """Build chart code snippets"""
    
    @staticmethod
    def histogram(column: str) -> str:
        """Generate histogram code"""
        return dedent(f"""
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.hist(df['{column}'], bins=30, edgecolor='black', alpha=0.7)
        plt.xlabel('{column}')
        plt.ylabel('Frequency')
        plt.title(f'Distribution of {column}')
        plt.grid(True, alpha=0.3)
        plt.show()
        """).strip()
    
    @staticmethod
    def scatter(x: str, y: str, hue: Optional[str] = None) -> str:
        """Generate scatter plot code"""
        if hue:
            return dedent(f"""
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x='{x}', y='{y}', hue='{hue}', s=100, alpha=0.6)
            plt.xlabel('{x}')
            plt.ylabel('{y}')
            plt.title(f'{y} vs {x}')
            plt.legend()
            plt.show()
            """).strip()
        else:
            return dedent(f"""
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(10, 6))
            plt.scatter(df['{x}'], df['{y}'], s=100, alpha=0.6)
            plt.xlabel('{x}')
            plt.ylabel('{y}')
            plt.title(f'{y} vs {x}')
            plt.grid(True, alpha=0.3)
            plt.show()
            """).strip()
    
    @staticmethod
    def bar_chart(column: str, top_n: int = 10) -> str:
        """Generate bar chart code"""
        return dedent(f"""
        import matplotlib.pyplot as plt
        
        value_counts = df['{column}'].value_counts().head({top_n})
        
        plt.figure(figsize=(10, 6))
        value_counts.plot(kind='barh')
        plt.xlabel('Count')
        plt.ylabel('{column}')
        plt.title(f'Top {top_n} {column}')
        plt.tight_layout()
        plt.show()
        """).strip()
    
    @staticmethod
    def correlation_heatmap() -> str:
        """Generate correlation heatmap code"""
        return dedent("""
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        numeric_df = df.select_dtypes(include=['number'])
        corr_matrix = numeric_df.corr()
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, square=True, cbar_kws={'label': 'Correlation'})
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.show()
        """).strip()
    
    @staticmethod
    def pairplot(hue: Optional[str] = None) -> str:
        """Generate pairplot code"""
        if hue:
            return dedent(f"""
            import seaborn as sns
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()[:4]
            sns.pairplot(df[numeric_cols + ['{hue}']], hue='{hue}', diag_kind='kde', 
                        plot_kws={{'alpha': 0.6}}, height=2.5)
            plt.show()
            """).strip()
        else:
            return dedent("""
            import seaborn as sns
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()[:4]
            sns.pairplot(df[numeric_cols], diag_kind='kde', 
                        plot_kws={'alpha': 0.6}, height=2.5)
            plt.show()
            """).strip()


class InsightGenerator:
    """Generate automatic insights from data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
    def generate_all(self, max_insights: int = 10) -> List[Dict[str, Any]]:
        """Generate comprehensive insights"""
        insights = []
        
        insights.extend(self.basic_stats())
        insights.extend(self.missing_value_analysis())
        insights.extend(self.distribution_analysis())
        insights.extend(self.outlier_detection())
        insights.extend(self.correlation_analysis())
        
        return insights[:max_insights]
    
    def basic_stats(self) -> List[Dict[str, Any]]:
        """Basic statistical insights"""
        return [{
            'category': 'overview',
            'title': 'Dataset Shape',
            'description': f'{self.df.shape[0]:,} rows × {self.df.shape[1]} columns',
            'type': 'info'
        }]
    
    def missing_value_analysis(self) -> List[Dict[str, Any]]:
        """Analyze missing values"""
        insights = []
        missing = self.df.isnull().sum()
        missing_pct = (missing / len(self.df)) * 100
        
        for col in missing[missing > 0].index:
            insights.append({
                'category': 'quality',
                'title': f'Missing values in {col}',
                'description': f'{missing[col]} ({missing_pct[col]:.1f}%)',
                'type': 'warning' if missing_pct[col] > 10 else 'info'
            })
        
        return insights
    
    def distribution_analysis(self) -> List[Dict[str, Any]]:
        """Analyze distributions of numeric columns"""
        insights = []
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            skewness = self.df[col].skew()
            if abs(skewness) > 1:
                insights.append({
                    'category': 'distribution',
                    'title': f'{col} distribution',
                    'description': f'Highly skewed (skewness: {skewness:.2f})',
                    'type': 'analysis'
                })
        
        return insights
    
    def outlier_detection(self) -> List[Dict[str, Any]]:
        """Detect outliers using IQR method"""
        insights = []
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < (Q1 - 1.5 * IQR)) | 
                       (self.df[col] > (Q3 + 1.5 * IQR))).sum()
            
            if outliers > 0:
                insights.append({
                    'category': 'quality',
                    'title': f'Outliers in {col}',
                    'description': f'{outliers} potential outliers detected',
                    'type': 'warning'
                })
        
        return insights
    
    def correlation_analysis(self) -> List[Dict[str, Any]]:
        """Analyze correlations between numeric variables"""
        insights = []
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) >= 2:
            corr_matrix = self.df[numeric_cols].corr()
            
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        insights.append({
                            'category': 'correlation',
                            'title': 'Strong correlation',
                            'description': f'{corr_matrix.columns[i]} ↔ {corr_matrix.columns[j]} ({corr_val:.3f})',
                            'type': 'analysis'
                        })
        
        return insights


class DataViz:
    """Main class with spreadsheet editing, insights, and code generation"""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize DataViz with a pandas DataFrame"""
        self.df = df.copy()
        self.original_df = df.copy()
        self.code_gen = CodeGenerator()
        self._analysis_cache = {}
        
    def show(self, n: int = 20):
        """Display interactive spreadsheet view"""
        html = self._generate_spreadsheet_html(n)
        display(HTML(html))
        
    def insights(self, max_insights: int = 5, detailed: bool = False):
        """
        Generate automatic insights about the data
        
        Parameters:
        -----------
        max_insights : int
            Maximum number of insights to display
        detailed : bool
            If True, use InsightGenerator for comprehensive analysis
        """
        if detailed:
            generator = InsightGenerator(self.df)
            insights = generator.generate_all(max_insights)
            html = self._generate_detailed_insights_html(insights)
        else:
            insights = []
            insights.append(self._shape_insight())
            
            missing_insight = self._missing_values_insight()
            if missing_insight:
                insights.append(missing_insight)
            
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                insights.append(self._numeric_insight())
            
            cat_cols = self.df.select_dtypes(include=['object', 'category']).columns
            if len(cat_cols) > 0:
                insights.append(self._categorical_insight())
            
            if len(numeric_cols) > 1:
                insights.append(self._correlation_insight())
            
            html = self._generate_insights_html(insights[:max_insights])
        
        display(HTML(html))
        
    def optimize(self):
        """🔧 Suggest optimizations for your DataFrame"""
        optimizer = CodeOptimizer()
        suggestions = optimizer.analyze_dataframe(self.df)
        
        print("⚡ Optimization Suggestions\n")
        for i, sug in enumerate(suggestions, 1):
            icon = "⚠️" if sug['severity'] == 'warning' else "💡"
            print(f"{icon} {i}. {sug['title']}")
            print(f"   {sug['suggestion']}\n")
            print(f"   Code:")
            print(f"   {sug['code']}\n")
        
        if not suggestions:
            print("✅ Your DataFrame is already well-optimized!")
            
    def generate_code(self, df_name: str = 'df', include_load: bool = True) -> str:
        """📄 Generate pandas code for all operations"""
        code = self.code_gen.generate_code(df_name)
        
        if len(self.code_gen.operations) == 0:
            print("ℹ️  No operations recorded yet. Try using methods like:")
            print("   • dv.filter(condition, 'description')")
            print("   • dv.sort_values('column')")
            print("   • dv.drop_missing(['col1', 'col2'])")
            print("   • dv.fill_missing('column', value)")
            print("\nOr generate code for current visualizations:")
            self.suggest_charts()
            return ""
        
        if include_load:
            code = f"# Load your data\n{df_name} = pd.read_csv('your_data.csv')\n\n" + code
        
        print("📄 Generated Pandas Code:\n")
        display(Code(code, language='python'))
        return code
    
    def suggest_charts(self, max_charts: Union[int, str] = 'all'):
        """
        📊 Suggest appropriate visualizations
        
        Parameters:
        -----------
        max_charts : int or 'all'
            Maximum number of charts to suggest. Use 'all' for unlimited.
            Common values: 2, 6, 10, 'all'
        """
        print("📊 Suggested Visualizations\n")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        suggestions = []
        
        # Histograms for numeric columns
        for col in numeric_cols[:3]:
            suggestions.append({
                'title': f'Distribution of {col}',
                'code': ChartBuilder.histogram(col)
            })
        
        # Bar charts for categorical
        for col in cat_cols[:3]:
            if self.df[col].nunique() <= 20:
                suggestions.append({
                    'title': f'Frequency of {col}',
                    'code': ChartBuilder.bar_chart(col)
                })
        
        # Scatter plot for correlated variables
        if len(numeric_cols) >= 2:
            suggestions.append({
                'title': f'{numeric_cols[0]} vs {numeric_cols[1]}',
                'code': ChartBuilder.scatter(numeric_cols[0], numeric_cols[1])
            })
        
        # Correlation heatmap
        if len(numeric_cols) >= 2:
            suggestions.append({
                'title': 'Correlation Heatmap',
                'code': ChartBuilder.correlation_heatmap()
            })
        
        # Pairplot
        if len(numeric_cols) >= 2:
            hue_col = cat_cols[0] if cat_cols and self.df[cat_cols[0]].nunique() <= 5 else None
            suggestions.append({
                'title': 'Pairplot Analysis',
                'code': ChartBuilder.pairplot(hue_col)
            })
        
        # Limit suggestions based on max_charts
        if max_charts != 'all':
            suggestions = suggestions[:max_charts]
        
        for i, sug in enumerate(suggestions, 1):
            print(f"{i}. {sug['title']}")
            print("   Code:")
            for line in sug['code'].split('\n'):
                print(f"   {line}")
            print()
        
        return suggestions
    
    def export_analysis_code(self, filename: Optional[str] = None) -> str:
        """📁 Export complete analysis code including EDA steps"""
        code_lines = [
            "# Complete Data Analysis Code",
            "import pandas as pd",
            "import numpy as np",
            "import matplotlib.pyplot as plt",
            "import seaborn as sns",
            "",
            "# Load data",
            "df = pd.read_csv('your_data.csv')  # Replace with your file",
            "",
            "# Basic info",
            "print('Dataset Shape:', df.shape)",
            "print('\\nColumn Types:')",
            "print(df.dtypes)",
            "print('\\nMissing Values:')",
            "print(df.isnull().sum())",
            "print('\\nBasic Statistics:')",
            "print(df.describe())",
            ""
        ]
        
        # Add operations
        if len(self.code_gen.operations) > 0:
            code_lines.append("# Data transformations")
            for op in self.code_gen.operations:
                if op['type'] == 'filter':
                    code_lines.append(f"df = df[{op['params']['condition']}]")
                elif op['type'] == 'sort':
                    col = op['params']['column']
                    asc = op['params']['ascending']
                    code_lines.append(f"df = df.sort_values('{col}', ascending={asc})")
                elif op['type'] == 'drop_na':
                    subset = op['params'].get('subset')
                    if subset:
                        code_lines.append(f"df = df.dropna(subset={subset})")
                    else:
                        code_lines.append(f"df = df.dropna()")
                elif op['type'] == 'fill_na':
                    col = op['params']['column']
                    value = op['params']['value']
                    code_lines.append(f"df['{col}'] = df['{col}'].fillna({repr(value)})")
            code_lines.append("")
        
        # Add visualization code
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if numeric_cols:
            code_lines.append("# Visualizations")
            code_lines.append("")
            
            if len(numeric_cols) > 0:
                code_lines.extend([
                    f"# Distribution of {numeric_cols[0]}",
                    "plt.figure(figsize=(10, 6))",
                    f"plt.hist(df['{numeric_cols[0]}'], bins=30, edgecolor='black', alpha=0.7)",
                    f"plt.xlabel('{numeric_cols[0]}')",
                    "plt.ylabel('Frequency')",
                    f"plt.title('Distribution of {numeric_cols[0]}')",
                    "plt.show()",
                    ""
                ])
            
            if len(numeric_cols) >= 2:
                code_lines.extend([
                    "# Correlation heatmap",
                    "plt.figure(figsize=(12, 8))",
                    "numeric_df = df.select_dtypes(include=['number'])",
                    "corr_matrix = numeric_df.corr()",
                    "sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0)",
                    "plt.title('Correlation Matrix')",
                    "plt.tight_layout()",
                    "plt.show()",
                    ""
                ])
            
            if len(numeric_cols) >= 2:
                code_lines.extend([
                    f"# Scatter plot: {numeric_cols[0]} vs {numeric_cols[1]}",
                    "plt.figure(figsize=(10, 6))",
                    f"plt.scatter(df['{numeric_cols[0]}'], df['{numeric_cols[1]}'], alpha=0.6)",
                    f"plt.xlabel('{numeric_cols[0]}')",
                    f"plt.ylabel('{numeric_cols[1]}')",
                    f"plt.title('{numeric_cols[1]} vs {numeric_cols[0]}')",
                    "plt.show()",
                    ""
                ])
        
        if cat_cols and self.df[cat_cols[0]].nunique() <= 20:
            code_lines.extend([
                f"# Bar chart for {cat_cols[0]}",
                f"value_counts = df['{cat_cols[0]}'].value_counts().head(10)",
                "plt.figure(figsize=(10, 6))",
                "value_counts.plot(kind='barh')",
                "plt.xlabel('Count')",
                f"plt.ylabel('{cat_cols[0]}')",
                f"plt.title('Top 10 {cat_cols[0]}')",
                "plt.tight_layout()",
                "plt.show()",
            ])
        
        code = "\n".join(code_lines)
        
        if filename:
            with open(filename, 'w') as f:
                f.write(code)
            print(f"✅ Code exported to {filename}")
        
        print("📁 Complete Analysis Code:\n")
        display(Code(code, language='python'))
        return code
            
    def visualize(self, auto: bool = True, max_charts: Union[int, str] = 'all'):
        """
        Generate automatic visualizations
        
        Parameters:
        -----------
        auto : bool
            If True, automatically select and generate best visualizations
        max_charts : int or 'all'
            Maximum number of charts to display. Use 'all' for unlimited.
            Common values: 2, 6, 10, 'all'
        """
        if auto:
            self._auto_visualize(max_charts)
        
    def plot_distribution(self, column: str, kind: str = 'hist', save_code: bool = False):
        """Plot distribution of a column"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if kind == 'hist':
            self.df[column].hist(bins=30, ax=ax, edgecolor='black', alpha=0.7)
            ax.set_title(f'Distribution of {column}', fontsize=14, fontweight='bold')
            ax.set_ylabel('Frequency', fontsize=12)
        elif kind == 'kde':
            self.df[column].plot(kind='kde', ax=ax, linewidth=2)
            ax.set_title(f'Density Plot of {column}', fontsize=14, fontweight='bold')
            ax.set_ylabel('Density', fontsize=12)
        elif kind == 'box':
            sns.boxplot(y=self.df[column], ax=ax)
            ax.set_title(f'Box Plot of {column}', fontsize=14, fontweight='bold')
        
        ax.set_xlabel(column, fontsize=12)
        plt.tight_layout()
        plt.show()
        
        if save_code:
            self.code_gen.add_operation('plot', {
                'type': 'histogram',
                'column': column,
                'kind': kind
            })
        
    def plot_categorical(self, column: str, top_n: int = 10):
        """Plot categorical column distribution"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        value_counts = self.df[column].value_counts().head(top_n)
        sns.barplot(x=value_counts.values, y=value_counts.index, ax=ax, palette='viridis')
        
        ax.set_title(f'Top {top_n} Categories in {column}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Count', fontsize=12)
        ax.set_ylabel(column, fontsize=12)
        
        for i, v in enumerate(value_counts.values):
            ax.text(v, i, f' {v}', va='center', fontsize=10)
        
        plt.tight_layout()
        plt.show()
        
    def plot_scatter(self, x: str, y: str, hue: Optional[str] = None):
        """Create scatter plot"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if hue and hue in self.df.columns:
            sns.scatterplot(data=self.df, x=x, y=y, hue=hue, ax=ax, s=100, alpha=0.6)
        else:
            sns.scatterplot(data=self.df, x=x, y=y, ax=ax, s=100, alpha=0.6)
        
        ax.set_title(f'{y} vs {x}', fontsize=14, fontweight='bold')
        ax.set_xlabel(x, fontsize=12)
        ax.set_ylabel(y, fontsize=12)
        
        plt.tight_layout()
        plt.show()
        
    def plot_correlation(self, method: str = 'pearson'):
        """Plot correlation heatmap"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            print("Not enough numeric columns for correlation analysis")
            return
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        corr_matrix = numeric_df.corr(method=method)
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                    center=0, square=True, ax=ax, cbar_kws={'label': 'Correlation'})
        
        ax.set_title(f'Correlation Matrix ({method.capitalize()})', 
                    fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def plot_pairplot(self, columns: Optional[List[str]] = None, hue: Optional[str] = None):
        """Create pairplot for numeric columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if columns:
            plot_cols = [col for col in columns if col in numeric_cols]
        else:
            plot_cols = numeric_cols[:4]
        
        if len(plot_cols) < 2:
            print("Not enough numeric columns for pairplot")
            return
        
        if hue and hue in self.df.columns:
            sns.pairplot(self.df[plot_cols + [hue]], hue=hue, diag_kind='kde', 
                        plot_kws={'alpha': 0.6}, height=2.5)
        else:
            sns.pairplot(self.df[plot_cols], diag_kind='kde', 
                        plot_kws={'alpha': 0.6}, height=2.5)
        
        plt.suptitle('Pairplot Analysis', y=1.01, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
        
    def filter(self, condition, description: str = ""):
        """Filter data and record operation"""
        self.df = self.df[condition]
        self.code_gen.add_operation('filter', {
            'condition': description or 'condition'
        })
        return self
    
    def sort_values(self, column: str, ascending: bool = True):
        """Sort DataFrame and record operation"""
        self.df = self.df.sort_values(column, ascending=ascending)
        self.code_gen.add_operation('sort', {
            'column': column,
            'ascending': ascending
        })
        return self
    
    def drop_missing(self, subset: Optional[List[str]] = None):
        """Drop missing values and record operation"""
        self.df = self.df.dropna(subset=subset)
        self.code_gen.add_operation('drop_na', {'subset': subset})
        return self
    
    def fill_missing(self, column: str, value: Any):
        """Fill missing values and record operation"""
        self.df[column] = self.df[column].fillna(value)
        self.code_gen.add_operation('fill_na', {
            'column': column,
            'value': value
        })
        return self
    
    def groupby_agg(self, by: Union[str, List[str]], agg: Dict[str, str]):
        """Group by and aggregate, recording operation"""
        self.df = self.df.groupby(by).agg(agg).reset_index()
        self.code_gen.add_operation('groupby', {
            'by': by,
            'agg': agg
        })
        return self
    
    def add_column(self, column: str, expression: str):
        """Add new column and record operation"""
        # Note: This is for code generation, actual computation should be done separately
        self.code_gen.add_operation('add_column', {
            'column': column,
            'expression': expression
        })
        return self
    
    def reset(self):
        """Reset to original DataFrame"""
        self.df = self.original_df.copy()
        self.code_gen.reset()
        return self
    
    def _auto_visualize(self, max_charts: Union[int, str] = 'all'):
        """Generate automatic visualizations"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        print("🎨 Generating Automatic Visualizations...\n")
        
        chart_count = 0
        max_chart_num = float('inf') if max_charts == 'all' else max_charts
        
        # 1. Correlation heatmap for numeric columns
        if len(numeric_cols) >= 2 and chart_count < max_chart_num:
            print("📊 Correlation Heatmap")
            self.plot_correlation()
            chart_count += 1
        
        # 2. Distribution plots for numeric columns
        for col in numeric_cols[:3]:
            if chart_count >= max_chart_num:
                break
            print(f"📊 Distribution of {col}")
            self.plot_distribution(col, kind='hist')
            chart_count += 1
        
        # 3. Categorical plots
        for col in cat_cols[:3]:
            if chart_count >= max_chart_num:
                break
            if self.df[col].nunique() <= 20:
                print(f"📊 Category Distribution of {col}")
                self.plot_categorical(col)
                chart_count += 1
        
        # 4. Scatter plot for top 2 correlated variables
        if len(numeric_cols) >= 2 and chart_count < max_chart_num:
            corr_matrix = self.df[numeric_cols].corr()
            np.fill_diagonal(corr_matrix.values, 0)
            
            if corr_matrix.abs().max().max() > 0:
                max_idx = corr_matrix.abs().stack().idxmax()
                print(f"📊 Scatter Plot - {max_idx[0]} vs {max_idx[1]}")
                
                hue_col = cat_cols[0] if cat_cols and self.df[cat_cols[0]].nunique() <= 10 else None
                self.plot_scatter(max_idx[0], max_idx[1], hue=hue_col)
                chart_count += 1
        
        # 5. Pairplot for comprehensive view
        if len(numeric_cols) >= 2 and chart_count < max_chart_num:
            print("📊 Pairplot Analysis")
            hue_col = cat_cols[0] if cat_cols and self.df[cat_cols[0]].nunique() <= 5 else None
            self.plot_pairplot(hue=hue_col)
            chart_count += 1
        
        print(f"\n✅ Visualization complete! ({chart_count} charts generated)")
        
    def _shape_insight(self) -> Dict[str, Any]:
        """Generate insight about data shape"""
        return {
            'title': 'Dataset Overview',
            'description': f"Dataset contains {self.df.shape[0]:,} rows and {self.df.shape[1]} columns",
            'type': 'info'
        }
    
    def _missing_values_insight(self) -> Optional[Dict[str, Any]]:
        """Generate insight about missing values"""
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]
        
        if len(missing) > 0:
            total_missing = missing.sum()
            pct = (total_missing / (self.df.shape[0] * self.df.shape[1])) * 100
            return {
                'title': 'Missing Values Detected',
                'description': f"{total_missing:,} missing values ({pct:.2f}%) across {len(missing)} columns",
                'type': 'warning',
                'details': missing.to_dict()
            }
        return None
    
    def _numeric_insight(self) -> Dict[str, Any]:
        """Generate insight about numeric columns"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        variances = self.df[numeric_cols].var()
        max_var_col = variances.idxmax()
        
        return {
            'title': 'Numeric Data Summary',
            'description': f"{len(numeric_cols)} numeric columns detected. '{max_var_col}' shows highest variance",
            'type': 'analysis'
        }
    
    def _categorical_insight(self) -> Dict[str, Any]:
        """Generate insight about categorical columns"""
        cat_cols = self.df.select_dtypes(include=['object', 'category']).columns
        unique_counts = {col: self.df[col].nunique() for col in cat_cols}
        
        return {
            'title': 'Categorical Data Summary',
            'description': f"{len(cat_cols)} categorical columns with varying cardinality",
            'type': 'analysis',
            'details': unique_counts
        }
    
    def _correlation_insight(self) -> Dict[str, Any]:
        """Generate insight about correlations"""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        corr_matrix = self.df[numeric_cols].corr()
        
        np.fill_diagonal(corr_matrix.values, 0)
        max_corr = corr_matrix.abs().max().max()
        max_idx = corr_matrix.abs().stack().idxmax()
        
        return {
            'title': 'Correlation Analysis',
            'description': f"Strongest correlation: {max_idx[0]} ↔ {max_idx[1]} ({max_corr:.3f})",
            'type': 'analysis'
        }
    
    def _generate_spreadsheet_html(self, n: int) -> str:
        """Generate HTML for spreadsheet view"""
        table_html = self.df.head(n).to_html(classes='dataviz-table', index=True)
        
        html = f"""
        <style>
            .dataviz-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
            }}
            .dataviz-table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .dataviz-table th {{
                background: #007bff;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }}
            .dataviz-table td {{
                padding: 10px 12px;
                border-bottom: 1px solid #dee2e6;
            }}
            .dataviz-table tr:hover {{
                background-color: #f1f3f5;
            }}
        </style>
        <div class="dataviz-container">
            <h3>📊 Data View (showing first {n} rows)</h3>
            {table_html}
        </div>
        """
        return html
    
    def _generate_insights_html(self, insights: List[Dict[str, Any]]) -> str:
        """Generate HTML for insights"""
        icons = {'info': '📌', 'warning': '⚠️', 'analysis': '🔍'}
        
        insights_html = ""
        for insight in insights:
            icon = icons.get(insight['type'], '•')
            details_html = ""
            
            if 'details' in insight and insight['details']:
                if isinstance(insight['details'], dict):
                    details_items = '<br>'.join([f"  • {k}: {v}" for k, v in list(insight['details'].items())[:5]])
                    details_html = f"<div class='insight-details'>{details_items}</div>"
            
            insights_html += f"""
            <div class="insight-card insight-{insight['type']}">
                <div class="insight-icon">{icon}</div>
                <div class="insight-content">
                    <h4>{insight['title']}</h4>
                    <p>{insight['description']}</p>
                    {details_html}
                </div>
            </div>
            """
        
        html = f"""
        <style>
            .insights-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                padding: 20px;
            }}
            .insight-card {{
                display: flex;
                background: white;
                border-left: 4px solid #007bff;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .insight-card.insight-warning {{
                border-left-color: #ffc107;
            }}
            .insight-card.insight-analysis {{
                border-left-color: #28a745;
            }}
            .insight-icon {{
                font-size: 24px;
                margin-right: 15px;
            }}
            .insight-content h4 {{
                margin: 0 0 8px 0;
                color: #212529;
            }}
            .insight-content p {{
                margin: 0;
                color: #6c757d;
            }}
            .insight-details {{
                margin-top: 10px;
                font-size: 0.9em;
                color: #495057;
                font-family: monospace;
            }}
        </style>
        <div class="insights-container">
            <h3>💡 Automatic Insights</h3>
            {insights_html}
        </div>
        """
        return html
    
    def _generate_detailed_insights_html(self, insights: List[Dict[str, Any]]) -> str:
        """Generate HTML for detailed insights from InsightGenerator"""
        icons = {
            'overview': '📊',
            'quality': '⚠️',
            'distribution': '📈',
            'correlation': '🔗'
        }
        
        insights_html = ""
        for insight in insights:
            icon = icons.get(insight.get('category', 'overview'), '•')
            
            insights_html += f"""
            <div class="insight-card insight-{insight['type']}">
                <div class="insight-icon">{icon}</div>
                <div class="insight-content">
                    <h4>{insight['title']}</h4>
                    <p>{insight['description']}</p>
                </div>
            </div>
            """
        
        html = f"""
        <style>
            .insights-container {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                padding: 20px;
            }}
            .insight-card {{
                display: flex;
                background: white;
                border-left: 4px solid #007bff;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .insight-card.insight-warning {{
                border-left-color: #ffc107;
            }}
            .insight-card.insight-analysis {{
                border-left-color: #28a745;
            }}
            .insight-card.insight-info {{
                border-left-color: #17a2b8;
            }}
            .insight-icon {{
                font-size: 24px;
                margin-right: 15px;
            }}
            .insight-content h4 {{
                margin: 0 0 8px 0;
                color: #212529;
            }}
            .insight-content p {{
                margin: 0;
                color: #6c757d;
            }}
        </style>
        <div class="insights-container">
            <h3>💡 Detailed Insights</h3>
            {insights_html}
        </div>
        """
        return html


def analyze(df: pd.DataFrame) -> DataViz:
    """
    Quick analysis function - Create a DataViz object from a DataFrame
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to analyze
        
    Returns:
    --------
    DataViz object
    
    Examples:
    ---------
    >>> import pandas as pd
    >>> df = pd.read_csv('data.csv')
    >>> dv = analyze(df)
    >>> 
    >>> # View data
    >>> dv.show(n=20)
    >>> 
    >>> # Get insights
    >>> dv.insights()
    >>> dv.insights(detailed=True, max_insights=10)
    >>> 
    >>> # Optimize
    >>> dv.optimize()
    >>> 
    >>> # Suggest charts (with limit)
    >>> dv.suggest_charts(max_charts=6)
    >>> 
    >>> # Visualize (with limit)
    >>> dv.visualize(max_charts=2)
    >>> 
    >>> # Perform operations (method chaining)
    >>> dv.filter(df['age'] > 25, "df['age'] > 25") \\
    >>>   .sort_values('salary', ascending=False) \\
    >>>   .drop_missing(['name', 'email'])
    >>> 
    >>> # Generate code
    >>> dv.generate_code()
    >>> 
    >>> # Export complete analysis
    >>> dv.export_analysis_code('my_analysis.py')
    >>> 
    >>> # Reset to original
    >>> dv.reset()
    """
    return DataViz(df)