
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
        DataFrame already aggregated with at least these 4 columns in this order:
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