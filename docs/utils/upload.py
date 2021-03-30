def upload(filepath, comment, url, headers):
    """Upload a file with progress bar.

    Parameters
    ----------
    filepath : string
        The local filepath of the file to upload.
    comment : string
        The comment for the file to upload.
    url : string
        The url of the file to upload.
    headers : dictionary
        The headers of the upload's request.

    Returns
    -------
    headers : dictionary | json
        The response of the upload's request.
    """