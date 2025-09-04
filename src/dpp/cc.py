#######
# dpp/cc.py - Call Center Workforce Planning Functions
# 
#######
# Functions to reload on the fly in Jupyter notebooks
# %load_ext autoreload
# %autoreload 2
#


import matplotlib.pyplot as plt


def compute_needed_agents(total_service_seconds, work_seconds_per_agent, target_utilization):
    """
    Compute the number of agents needed given the total service seconds,
    work time per agent, and target utilization.

    Parameters:
    total_service_seconds : float or Series
        Total seconds of service required in the period.
    work_seconds_per_agent : float
        Total work seconds available per agent.
    target_utilization : float
        Target agent utilization (0-1).

    Returns:
    float or Series: number of agents needed
    """
    agents_needed = total_service_seconds / (work_seconds_per_agent * target_utilization)
    return agents_needed





### Calculate Utilization for a target service level


def utilization_with_target(agg, target_sl, num_agents, work_seconds_per_agent):
    """
    Compute the average agent utilization required to reach the target service level.

    Parameters
    ----------
    agg : pandas.DataFrame
        DataFrame already aggregated with at least these 3 columns in this order:
        [total_calls, calls_within_threshold, total_service_seconds]
    target_sl : float
        Target service level (0-1).

    Returns
    -------
    float
        Average utilization required to meet the target service level.

    Example
    -------
    >>> agg = (
    ...     df.groupby("date")
    ...     .agg(
    ...         total_calls=("wait_length", "count"),
    ...         calls_within_threshold=("wait_length", lambda x: (x <= 60).sum()),
    ...         total_service_seconds=("service_length", "sum")
    ...     )
    ...     .reset_index()
    ... )
    >>> agg["service_level"] = agg.iloc[:,1] / agg.iloc[:,0]  # calls_within_threshold / total_calls
    >>> util = compute_required_utilization(agg, target_sl=0.9)
    >>> print(util)
    """

    # average utilization adjusted for target SL
    agg["service_level"] = agg.iloc[:,1] / agg.iloc[:,0]
    # historical utilization
    agg["agent_utilization"] = agg.iloc[:,2] / (num_agents * work_seconds_per_agent)

    average_agent_utilization = agg["agent_utilization"].mean() * (agg["service_level"].mean() / target_sl)

    return float(average_agent_utilization)



import pandas as pd
import matplotlib.pyplot as plt

def plot_weekly_calls_by_skills(df, skills, min_display=5):
    """
    Plot weekly inbound and outbound calls for one or more skills, with numbers and percentages on bars.
    Only display numbers greater than min_display.
    
    Parameters:
        df (pd.DataFrame): The cleaned call center dataframe.
        skills (list): List of skill numbers (as strings or ints) to display.
        min_display (int): Minimum number to show on the bars.
    """
    for skill in skills:
        # Filter for current skill
        df_skill = df[df['Skill #'] == str(skill)].copy()

        if df_skill.empty:
            print(f"No data for Skill {skill}. Skipping.")
            continue

        # Create ISO week labels
        iso_calendar = df_skill['Date'].dt.isocalendar()
        df_skill['Week'] = iso_calendar['week'].apply(lambda x: f"W{x:02d}") + '-' + iso_calendar['year'].astype(str)

        # Aggregate calls per week
        agg_skill_week = (
            df_skill
            .groupby('Week', as_index=False)
            .agg({
                'ACD Calls': 'sum',
                'Long Distance Outbounds': 'sum'
            })
        )

        # Sort by week
        agg_skill_week = agg_skill_week.sort_values(by='Week').reset_index(drop=True)

        # Plot stacked bar chart
        fig, ax = plt.subplots(figsize=(14, 6))  # wider figure to avoid layout issues
        ax.bar(agg_skill_week['Week'], agg_skill_week['ACD Calls'], label='Inbound (ACD Calls)', color='skyblue')
        ax.bar(agg_skill_week['Week'], agg_skill_week['Long Distance Outbounds'],
               bottom=agg_skill_week['ACD Calls'], label='Outbound', color='salmon')

        # Add numbers and percentages on top of each stacked bar
        for idx, row in agg_skill_week.iterrows():
            total_calls = row['ACD Calls'] + row['Long Distance Outbounds']

            # Inbound
            if row['ACD Calls'] > min_display:
                pct_in = row['ACD Calls'] / total_calls * 100
                ax.text(idx, row['ACD Calls'] / 2, f"{row['ACD Calls']}\n({pct_in:.0f}%)",
                        ha='center', va='center', color='black', fontsize=9)

            # Outbound
            if row['Long Distance Outbounds'] > min_display:
                pct_out = row['Long Distance Outbounds'] / total_calls * 100
                ax.text(idx, row['ACD Calls'] + row['Long Distance Outbounds'] / 2,
                        f"{row['Long Distance Outbounds']}\n({pct_out:.0f}%)",
                        ha='center', va='center', color='black', fontsize=9)

        # Beautify
        ax.set_xlabel("Week")
        ax.set_ylabel("Number of Calls")
        ax.set_title(f"Weekly Calls for Skill {skill} (Inbound vs Outbound)")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout(pad=2.0)  # Add padding to avoid tight layout warnings
        plt.show()