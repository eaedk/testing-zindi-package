def participations(challenge_id, headers):
    """Check if user is in team for a the Zindi's challenges.

    Parameters
    ----------
    challenge_id : string
        The id of the selected challenge.
    headers : dictionary
        The headers of the request to participate in a challenge.  

    Returns
    -------
    challenges_data : pd.DataFrame
        The response of the request to get informations about the available challenges.
    """