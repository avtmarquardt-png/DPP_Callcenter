
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from IPython.display import display


def check_required_packages(needed_packages):
    """
    Checks if all packages in needed_packages are installed (using importlib.util.find_spec).
    Prints an error message listing missing packages.
    """
    import importlib.util
    missing = []
    for pkg in needed_packages:
        if importlib.util.find_spec(pkg) is None:
            missing.append(pkg)
    if missing:
        print(f"Error: The following packages are missing: {', '.join(missing)}")
        print("Please install them using pip before running this script.")


# Plot grouped distributions of numerical features
def numplots(col, data, key):
    '''
    Plot a histogram, boxplot and kernel density estimation (kde) plot, grouped by 'key'.
    ARGS:
        col: Column to plot
        data: DataFrame
        key: Column to group by
    RETURN: None

    Needed packages: matplotlib, seaborn, pandas
    '''
    needed_packages = ['matplotlib', 'seaborn', 'pandas']
    check_required_packages(needed_packages)
    fig, ax = plt.subplots(ncols=3, figsize=(16,3))
    sns.boxplot(data=data, y=col, x=key, ax=ax[0])
    data.groupby(key)[col].plot(kind='hist', bins=20, ax=ax[1], alpha=0.5, density=True)
    data.groupby(key)[col].plot(kind='kde', ax=ax[2])

# Plot grouped distributions of categorical features
def catplot(x, y):
    '''
    Display 'x vs. y' barplots of a normalized crosstab for relative distributions and an absolute crosstab for a sanity check.
    ARGS:
        x: Crosstab 'index' column
        y: Crosstab 'columns' column
    RETURNS: None

    Needed packages: matplotlib, pandas
    '''
    needed_packages = ['matplotlib', 'pandas']
    check_required_packages(needed_packages)
    crosstab_rel = pd.crosstab(index=x, columns=y, normalize='index')
    crosstab_abs = pd.crosstab(index=x, columns="count")
    fig, ax = plt.subplots(figsize=(16,3), ncols=2)
    crosstab_rel.plot(kind='bar', ax=ax[0])
    crosstab_abs.plot(kind='bar', ax=ax[1])



def overview(df):
    '''
    Erstelle einen Überblick über einige Eigenschaften der Spalten eines DataFrames.
    VARs
        df: Der zu betrachtende DataFrame
    RETURNS:
        None

    Needed packages: pandas, IPython
    '''
    needed_packages = ['pandas', 'IPython', 'numpy']
    check_required_packages(needed_packages)
    display(pd.DataFrame({
        'dtype': df.dtypes,
        'total': df.count(),
        'missing_n': df.isna().sum(),
        'missing_%': df.isna().mean()*100,
        'uniques_n': df.nunique(),
        'uniques': [df[col].unique() for col in df.columns]
    }))
