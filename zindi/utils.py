import requests, os
from requests_toolbelt import (MultipartEncoder,MultipartEncoderMonitor)
from tqdm import tqdm
import pandas as pd

# Utils

## Download a file
def download(url="https://", filename="", headers=''):
    """Download a file with progress bar.

    Parameters
    ----------
    url : string
        The url of the file to download.
    filename : string
        The local filename of the file to download.
    headers : dictionary
        The headers of the download's request.
    """

    response = requests.post(url, headers=headers, stream=True)
    response.raise_for_status() # check if there is no error
    total = int(response.headers.get('content-length', 0))
    with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total,
            unit='o',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


# Upload a file
def upload(filepath, url, headers):
    """Upload a file with progress bar.

    Parameters
    ----------
    filepath : string
        The local filepath of the file to upload.
    url : string
        The url of the file to upload.
    headers : dictionary
        The headers of the upload's request.

    Returns
    -------
    headers : dictionary | json
        The response of the upload's request.
    """

    filename = (os.sep).join(filepath.split(os.sep)[-2:]) 
    encoder = MultipartEncoder({'file': (filename, open(filepath, 'rb'), 'text/plain'),})

    with tqdm(desc=f"Submit {filename}",
              total=encoder.len, ncols=100,
              unit='o', unit_scale=True,
              unit_divisor=1024             ) as progress_bar :

        multipart_monitor = MultipartEncoderMonitor(encoder, lambda monitor: progress_bar.update(monitor.bytes_read - progress_bar.n))
        headers = {**headers, 'Content-Type': multipart_monitor.content_type,}

        response = requests.post(url, data=multipart_monitor, headers= headers, )
    return response


## Print
### Challenges
def print_challenges(challenges_data):
    """Formated print the Zindi's challenge as table.

    Parameters
    ----------
    challenges_data : dictionary | json
        The json's response of the request to get informations about the challenges.
    """

    n_challenges = challenges_data.shape[0] # total count of retreived challenges
    print("_"*130 )
    print("|{:^5}|{:^14.14}|{:^18.18}|{:^20.20}|{:^10}".format( "" , "" , "", "" , "" ,  ))
    print("|{:^5}|{:^14.14}|{:^18.18}|{:^20.20}|{:^10}".format( "index" , "challenge" , "problem", "reward" , "id" ,  ))
    print("|{:^5}|{:^14.14}|{:^18.18}|{:^20.20}|{:^10}".format( "" , "" , "", "" , "" ,  ))
    # for data in challenges_data:
    for i in range(n_challenges):
        data = dict(challenges_data.iloc[i]) # data - each challenge, one after another
        reward = data['reward'] # Challenge's reward for top challengers
        id = data['id'][:50]+"..." # Challenge's id
        problem = '' if  len(data['type_of_problem'])==0 else data['type_of_problem'][0] # category of the challenge's problem
        kind = "Hack" if data['kind'] == "hackathon" else "Compet"  # simple challenge's kind
        visibility = 'Public' if not data['secret_code_required'] else 'Private' # Challenge's visibility
        challenge = f"{visibility} {kind}" # general challenge's kind - join visibility & kind 
        print("-"*130 )
        print ("|{:^5}|{:^14.14}|{:^18.18}|{:^20.20}| {:10}".format( i , challenge , problem , reward , id ,  ))
    print(f"{'_'*130}\n\n" )   


## Print
### Leaderboard
def print_lb(challengers_data, user_rank):
    """Formated print the Zindi's challenge leaderboard as table.

    Parameters
    ----------
    challengers_data : dictionary | json
        The json's response of the request to get informations about the leaderboard.
    user_rank : int
        The rank of the user on the leaderboard of a challenge.
    """

    print("_"*130 )
    print("|{:^6}|{:^20}|{:^44}|{:^12}|{:^12}".format( "" , "" , "", "" ,"" ,  ))
    print("|{:^6}|{:^20}|{:^44}|{:^12}|{:^12}".format( "rank" , "score" , "name", "counter", "last_submission" ,  ))
    print("|{:^6}|{:^20}|{:^44}|{:^12}|{:^12}".format( "" , "" , "", "" ,"" ,  ))
    # for data in challengers_data:
    for i in range(len(challengers_data)):
        data = challengers_data[i] # data - each row of the leaderboard
        try:
            score = data['best_private_score'] if "best_private_score" in data else data['best_public_score'] # Best submission's score
            rank = data['private_rank'] if "private_rank" in data else data['public_rank'] # Rank on leaderboard
            name = data['user']['username'] if "user" in data else f"TEAM - {data['team']['title']}" # Name of user or team
            n_submission = data['submission_count']
            last_submission = data['best_private_submitted_at'] if "best_private_submitted_at" in data else data['best_public_submitted_at']
            check = str(last_submission)==str(None) # conditioin to set last_submission value
            last_submission = '' if check==True else pd.to_datetime(str(last_submission)).strftime("%d %B %Y, %H:%M")
            # Check rank to exclude not yet active challengers
            if rank != None: 
                if rank == user_rank:# Check rank to mark my position on the leaderboard
                    name = f"{name} 🟢"
                print("-"*130 )
                print("|{:^6}|{:^20.20}|{:^44.44}|{:^12.12}|{:^12}".format( str(rank) , str(score) , str(name) , str(n_submission), str(last_submission), ))
            else:
                break # all the next zindians haven't made a correct submission yet
        except Exception as e:
            print(e)
    print(f"{'_'*130}\n\n" )  


## Print
### Submission-board
def print_submission_board(submissions_data):
    """Formated print the Zindi's challenge submission-board as table.

    Parameters
    ----------
    submissions_data : dictionary | json
        The json's response of the request to get informations about the submission-board of a challenge.
    """

    print("_"*130 )
    print("|{:^6}|{:^10}|{:^18}|{:^16}|{:^30} |{:^25}".format( "" , "" , "", "" ,"" , "" ,  ))
    print("|{:^6}|{:^10}|{:^18}|{:^16}|{:^30} |{:^25}".format( "status" , "id" , "date", "score", "filename", "comment" ,  ))
    print("|{:^6}|{:^10}|{:^18}|{:^16}|{:^30} |{:^25}".format( "" , "" , "", "" ,"" , "" ,  ))

    for data in submissions_data:
        filename = data['filename'] # Submission's filename
        date = pd.to_datetime(data['created_at'] ).strftime("%d %b %Y, %H:%M") # Date of submission
        id = data['id'] # submission's id
        
        if data['status'] in ["successful", "initial"]: 
            status = "🟢" # Status - for valid of the submission
            score = data['private_score'] if "private_score" in data else data['public_score'] # Score of the submission
            score = "In processing" if score == None else score # Show a message when processing of the score is not yet finished
            comment = "" if data['comment'] == None else data['comment'] # Comment of the submission
        else:
            score = "-" # Score of the submission : "-" for wrong submission
            status = "🔴" # Status - for wrong of the submission
            comment = "" if data['status_description'] == None else data['status_description'] # Submission error description
        print("-"*130 )
        try:
            print("|{:^5}|{:^10}|{:^12}| {:^14.14} |{:30.30} |{:40.40}".format( status , id , date, str(score) , filename, comment ,  ))
        except:
            print("|{:^5}|{:^10}|{:^12}| {:^14.14} |{:30.30} |{:40.40}".format( status , id , date, "" , filename, "Oop there is an unknown bug, sorry !" ,  ))
    print(f"{'_'*130}\n\n" )


## Join challenge
def join_challenge( url, headers, code=False):
    """Formated print the Zindi's challenge submission-board as table.

    Parameters
    ----------
    url : string
        The url of the selected challenge.
    headers : dictionary
        The headers of the request to participate in a challenge.    
    """

    # {secret_code: "cccccccccc"}
    if not code:
        response = requests.post( url=url, headers=headers )
    else:
        secret_code = input("Enter the secret code to join the challenge.\n>>")
        params = {'secret_code': secret_code}
        response = requests.post( url=url, headers=headers, params=params )

    response = response.json()['data']
    if "errors" in response : # raise error if request failed
        error = response['errors']['message']
        if error == "already in" :
            # print(f"\n[ 🟢 ] {error}\n")
            pass
        elif error == "This competition requires a secret code to join." :
            join_challenge( url, headers, code=True)
        else:
            msg_error = f"\n[ 🔴 ] {error}\n"
            raise Exception(msg_error)
    else: # else print success message
        if "ids" in response :
            print(f"\n[ 🟢 ] Welcome for the first time to this challenge.\n")
        else:
            print(f"\n[ 🟢 ] {response}.\n")


## Get available challenges
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

    to_show_challenge_data = ["id","kind",  "subtitle", "reward", "type_of_problem", "data_type", "secret_code_required", "sealed"]
    challenges_data = pd.DataFrame()
    
    # check validity of challenge sorting's values
    reward = '' if reward.lower() not in ['prize', 'points', 'knowledge' ] else reward.lower()
    kind = '' if kind.lower() not in ['competition', 'hackathon'] else kind.lower()
    active = '' if active.lower() not in [True, False] else int(active)
    # join sorting params in a dictionary which will be passed in the url
    sorting_params = dict(page=0, per_page=800, reward=reward, kind=kind, active=active )
    
    # request
    response = requests.get( url, headers=headers , params=sorting_params)
    response = response.json()['data']
    try: # raise error if request failed
        print( response['errors'] )
    except: # else go on in processing
        challenges_data = pd.DataFrame(response)
        # extract relevant columns and print the recap table
        challenges_data = challenges_data[to_show_challenge_data]
    return challenges_data


## challenge index selector
def challenge_idx_selector(n_challenges):
    """Get on the keyboard the index of the challenge tha the user want to participate in.

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
        user_input = input("Type the index of the challenge you want to select or 'q' to exit.\n>>")
        try: # user_input must be a valid integer or 'q' else we stay in the infinite loop
            user_input = int( user_input.strip() )

            if (user_input >= 0) and (user_input < n_challenges):
                challenge_index = user_input
                return challenge_index
            else:
                raise Exception()
        except:
            if user_input.lower().strip() == 'q': # to stop selection 
                return challenge_index 
            else:
                print("\n[ 🔴 ] Please enter a correct challenge index.\n")


##  Info about the challenges user participate in
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
    url = "https://api.zindi.africa/v1/participations"
    response = requests.get( url, headers=headers )
    response.raise_for_status() # check if there is no error
    response = response.json()['data']
    team_id = response[challenge_id]['team_id']
    return team_id


## Info about user position on lb 
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
    df_lb = pd.DataFrame(challengers_data) # DataFrame verion of the leaderboard
    df_lb = df_lb[ (df_lb.public_rank != None) ] # filter to use only leaderboard part with the active challengers
    try:
        team_id = participations(challenge_id=challenge_id, headers=headers)
        # Simple user
        if  not team_id:
            user = df_lb[df_lb['user'].astype(str).str.contains( username,)] # na=False, case=True, regex=False
            user_index = user.index.values[0].astype(int)
        # Team
        else :
            my_team = df_lb[df_lb['team'].astype(str).str.contains(team_id,)]
            user_index = my_team.index.values[0].astype(int)
        user_rank = user_index + 1
    except:
        user_rank = 0 # rank initialization if user is not yet active for the challenge
    return user_rank


## Info about number of submissions to do by day
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

    response = requests.get( url=url, headers=headers )
    response = response.json()['data']
    for info in response['pages']:
        if info['title'] == 'Rules' :
            break
    n_sub = info['content_html'].split( "You may make a maximum of")[-1].split("submissions per day.")[0].strip()
    try: # raise error if there is any problem
        n_sub = int(n_sub)
    except: # else n of subimission_per_day is unknown
        n_sub = 0
    return n_sub
