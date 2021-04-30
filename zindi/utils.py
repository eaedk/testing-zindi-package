import re
from getpass import getpass
from pathlib import Path

import pandas as pd
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm


def file_download(url=None, filepath=None, headers=None):
    """Download a file, while displaying a progress-bar.

    Parameters
    ----------
    url : str
        The url for the file to download.
    filepath : str
        The local path for the file to download.
    headers : dict
        The headers passed in the download request.
    """
    if filepath is None:
        time_now = pd.to_datetime('now').strftime('%d-%b-%H:%m')
        filepath = Path(f'zindi-download-{time_now}')
    # Send a request for the file at the given url
    response = requests.post(url, headers=headers, stream=True)
    # Check if a HTTPError occured
    response.raise_for_status()
    # Get number of 1KiB chunks
    content_size_kib = \
        int(response.headers.get('content-length', 0)) // 1024 + 1
    # Write the content to file in 1KiB chunks
    with filepath.open(mode='wb') as file:
        for chunk in tqdm(response.iter_content(chunk_size=1024), unit='KiB',
                          desc=filepath.name, total=content_size_kib):
            file.write(chunk)


def file_upload(filepath, comment, url, headers):
    """Upload a file while displaying a progress bar.

    Parameters
    ----------
    filepath : pathlib.Path
        The local path to the file to upload.
    comment : str
        The comment for the file to upload.
    url : str
        The url for the file to upload.
    headers : dict
        The headers for the upload's request.

    Returns
    -------
    headers : dict | json
        The response of the upload's request.
    """
    encoder = MultipartEncoder(
        {"file": (filepath.name, filepath.open(mode='rb'), 'text/csv'),
         "comment": comment}
    )
    with tqdm(desc=f"Submit {filepath.name}", total=encoder.len, ncols=100,
              unit='KiB') as progress_bar:
        multipart_monitor = MultipartEncoderMonitor(
            encoder,
            lambda monitor: progress_bar.update(monitor.bytes_read
                                                - progress_bar.n))
        headers['Content-Type'] = multipart_monitor.content_type

        response = requests.post(url, data=multipart_monitor, headers=headers)
    return response


def print_challenges(challenges_data):
    """Print Zindi challenges formated as table.

    Parameters
    ----------
    challenges_data : pandas.DataFrame
        A dataframe with information on challenges.
    """
    # Table header
    print("_"*110)
    print(f'|{"":^5}|{"":^14}|{"":^18}|{"":^20}|{"":^10}')
    print(f'|{"index":^5}|{"challenge":^14.14}|{"problem":^18.18}',
          f'|{"reward":^20.20}|{"id":^10}', sep='')
    print(f'|{"":^5}|{"":^14}|{"":^18}|{"":^20}|{"":^10}')
    # Table body
    for idx, row in challenges_data.iterrows():
        reward = row['reward']
        challenge_id = f"{row['id'][:45]}..."
        problem = ', '.join(row['type_of_problem'])
        kind = "Hack" if row['kind'] == "hackathon" else "Compet"
        visibility = 'Private' if row['secret_code_required'] else 'Public'
        challenge = f"{visibility} {kind}"
        print("-"*11)
        print(f"|{idx:^5}|{challenge:^14.14}|{problem:^18.18}|{reward:^20.20}",
              f"|{challenge_id}", sep='')
    print(f"{'_'*110}\n\n")


def print_leaderboard(challengers_data, user_rank):
    """Print the Zindi challenge's leaderboard formated as table.

    Parameters
    ----------
    challengers_data : dict | json
        The JSON response of the request for information about the leaderboard.
    user_rank : int
        The rank of the user on the leaderboard of a challenge.
    """
    print("_"*110)
    print(f"|{'':^6}|{'':^15}|{'':^44}|{'':^12}|{'':^12}")
    print(f"|{'rank':^6}|{'score':^15}|{'name':^44}|{'counter':^12}|",
          f"{'last_submission':^12}", sep='')
    print(f"|{'':^6}|{'':^15}|{'':^44}|{'':^12}|{'':^12}")

    # Create table
    ranked_user_data = challengers_data.dropna(subset=['public_rank'])

    for _, row in ranked_user_data.iterrows():
        if "best_private_score" in row:  # prefer private score
            score = row['best_private_score']
            last_submission = row['best_private_submitted_at']
        else:
            score = row['best_public_score']
            last_submission = row['best_public_submitted_at']
        if "private_rank" in row:
            rank = row['private_rank']
        else:
            rank = row['public_rank']
        name = row['username_or_teamtitle']
        n_submissions = row['submission_count']

        # Mark user's position on the leaderboard
        if rank == user_rank:
            name = f"{name} 🟢"
        # Print the leaderboard as a table
        print("-"*110)
        print(f"|{rank:^6.0f}|{score:^15.10f}|{name:^44.44}|",
              f"{n_submissions:^12.0f}|{last_submission:^12}", sep='')
    print(f"{'_'*110}\n\n")


def print_submission_board(submissions_data):
    """Print the Zindi challenge's submission-board formated as table.

    Parameters
    ----------
    submissions_data : pandas.DataFrame
        The JSON response to the request for information about the
        submission-board of a challenge.
    """

    print("_"*110)
    print(f"|{'':^6}|{'':^10}|{'':^20}|{'':^15}|{'':^25}|{'':^25}")
    print(f"|{'status':^6}|{'id':^10}|{'date':^20}|{'score':^15}|",
          f"{'filename':^25}|{'comment':^25}", sep='')
    print(f"|{'':^6}|{'':^10}|{'':^20}|{'':^15}|{'':^25}|{'':^25}")

    submissions_data['created_at_str'] = \
        submissions_data['created_at'].dt.strftime("%d %b %Y, %H:%M")

    for _, row in submissions_data.iterrows():
        filename = row['filename']
        date = row['created_at_str']
        id = row['id']
        comment = "" if row['comment'] is None else row['comment'][:25]

        if row['status'] in {"successful", "initial"}:
            status = "🟢"
            if "private_score" in row:
                score = row['private_score']
            else:
                score = row['public_score']
        else:
            status = "🔴"  # Status for invalid submission
            score = "-"  # Score for invalid submission
        # Create a table
        print("-"*110)
        print(f"|{status:^5}|{id:^10}|{date:^20}|{score:^15.10f}|",
              f"{filename:^25.25}|{comment:25.25}", sep='')
    print("-"*110)


def join_challenge(url, headers, code=False):
    """Print the Zindi challenge's submission-board formated as table.

    Parameters
    ----------
    url : str
        The url for the selected challenge.
    headers : dict
        The headers for the request to participate in a challenge.
    """
    if not code:
        response = requests.post(url=url, headers=headers)
    else:
        secret_code = getpass("Please enter the secret code to proceed.\n>> ")
        params = {'secret_code': secret_code}
        response = requests.post(url=url, headers=headers, params=params)

    response = response.json()['data']
    if "errors" in response:  # raise error if the request failed
        error = response['errors']['message']
        if error == "This competition requires a secret code to join.":
            join_challenge(url, headers, code=True)
        elif error == "already in":
            print("You already joined this challenge.")
        else:
            raise Exception(f"Unexpected error: {error}")
    else:
        if "ids" in response:
            print("\n[ 🟢 ] Welcome for the first time to this challenge.\n")
        else:
            print(f"\n[ 🟢 ] {response}.\n")


def get_challenges(reward='all', kind='all', url=None, headers=None):
    """Get the available Zindi's challenges using filter options.

    Parameters
    ----------
    reward : {'prize', 'points', 'knowledge' , 'all'}, default='all'
        The reward type for the challenges.
    kind : {'competition', 'hackathon', 'all'}, default='all'
        The kind of the challenge.
    url : string
        The url to the challenge data.
    headers : dict
        The headers for the request to obtain challenge info.

    Returns
    -------
    challenges_data : pd.DataFrame
        A dataframe with details on the available challenges.
    """
    reward = reward.lower()
    kind = kind.lower()
    # Validate reward and kind filters
    reward = '' if reward not in {'prize', 'points', 'knowledge'} else reward
    kind = '' if kind not in {'competition', 'hackathon'} else kind
    # Send request for challenge data
    params = dict(per_page=1000, reward=reward, kind=kind)
    response = requests.get(url, headers=headers, params=params)
    data = response.json()['data']
    challenges_data = pd.DataFrame(data)
    # Select relevant columns
    challenges_data = challenges_data[
        ["id", "kind", "subtitle", "reward", "type_of_problem", "data_type",
         "secret_code_required", "sealed"]
    ]
    return challenges_data


def challenge_idx_selector(n_challenges):
    """Get input on the index of the challenge that the user wants to
    participate in.

    Parameters
    ----------
    n_challenges : integer
        The number of retrieved challenges.

    Returns
    -------
    challenge_index : int
        The index of the challenge selected by the user.
    """
    challenge_index = -1

    while True:
        user_input = input("Type the index of the challenge you want to"
                           + " select or 'q' to exit.\n>> ")
        try:  # user_input must be a valid integer or 'q'
            user_input = int(user_input)
        except ValueError:
            if user_input.lower().strip() == 'q':  # 'q' stops selection
                return challenge_index

        if 0 <= user_input < n_challenges:  # a valid zero-based index
            return user_input
        else:
            print(f"""
[ 🔴 ] Please enter a correct challenge index, between 0 and {n_challenges - 1}
""")


def get_user_rank(challengers_data, challenge_id, username, headers):
    """Get the user's rank on the leaderboard of a Zindi challenge.

    Parameters
    ----------
    challengers_data : pandas.DataFrame
        The response of the request for information about the leaderboard.
    challenge_id : str
        The id of the selected challenge.
    username : str
        The user's username.
    headers : dict
        The headers for the request to participate in a challenge.

    Returns
    -------
    user_rank : int
        The rank of the user on the leaderboard of a challenge.
    """
    # Select only publicly ranked users
    leaderboard_df = challengers_data.dropna(subset=['public_rank'])
    username_or_teamtitle = leaderboard_df['username_or_teamtitle']

    user_index = username_or_teamtitle[
        username_or_teamtitle.str.contains(username)].index
    try:
        user_rank = user_index[0] + 1  # since index is zero-based
    except IndexError:  # user_index is empty, so user is not in leaderboard
        user_rank = 0

    return user_rank


def get_submissions_per_day(url, headers):
    """Get the number of submissions the user can make to the selected
    challenge per day.

    Parameters
    ----------
    url : str
        The the url to the challenge.
    headers : dict
        The headers for the request.
    Returns
    -------
    A string with the submission limit info.
    """

    response = requests.get(url=url, headers=headers)
    response = response.json()['data']

    # Get the rules section
    rules = response['pages'][2]['content_html']
    submission_limit = re.findall(
        r'You may make a maximum of \d+ submissions per day', rules)

    if submission_limit != []:
        submission_info = submission_limit[0]
        daily_limit = re.findall(r'\d+', submission_info)[0]
        return int(daily_limit)
    else:
        return "Couldn't get the daily submission limit"
