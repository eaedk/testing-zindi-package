def get_challenges(reward='all', kind='all', active='all', url='', headers='' ):
    """Get the available Zindi's challenges using filter options.

    Parameters
    ----------
    reward : {'prize', 'points', 'knowledge' , 'all'}, default='all'
        The reward of the challenges for top challengers.
    kind : {'competition', 'hackathon', 'all'}, default='all'
        The kind of the challenges.
    active : {True, False, 'all'}, default='all'
        The status of the challenges.

    url : string
        The url of the selected challenge.
    headers : dictionary
        The headers of the request to participate in a challenge.  

    Returns
    -------
    challenges_data : pd.DataFrame
        The response of the request to get informations about the available challenges.
    """