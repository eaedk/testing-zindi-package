def user_on_lb(challengers_data, challenge_id, username, headers):
    """Get rank of user on the leaderboard for a the Zindi's challenges.

    Parameters
    ----------
    challengers_data : dictionary | json
        The json's response of the request to get informations about the leaderboard.
    challenge_id : string
        The id of the selected challenge.
    username : string
        The username of the user.
    headers : dictionary
        The headers of the request to participate in a challenge.  

    Returns
    -------
    user_rank : int
        The rank of the user on the leaderboard of a challenge.
    """