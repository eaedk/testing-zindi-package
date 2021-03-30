def n_subimissions_per_day( url, headers ):
    """Get the number of submissions we can make per day for the selected challenge.

    Parameters
    ----------
    url : {'prize', 'points', 'knowledge' , 'all'}, default='all'
        The reward of the challenges for top challengers.
    headers : dictionary ,
        The headers of the request.
    Returns
    -------
    n_sub : int, default=0 : Means error during info retrieval.
        The number of submissions we can make per day.
    """