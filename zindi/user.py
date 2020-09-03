# Imports

import sys, os

## To avoid errors of importing before instalation
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from zindi.utils import *
from getpass import getpass

import pandas as pd
import requests
from tqdm import tqdm


# Class declaration and init
class Zindian:
    # __auth_data = ""
    
    def __init__(self, username, fixed_password=None):
        self.__headers = {'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
        self.__base_api = "https://api.zindi.africa/v1/competitions"
        self.__auth_data = None #auth & user data from Zindi server after signin
        self.__signin(username, fixed_password)
        self.__challenge_selected = False

# Properties
    @property
    def which_challenge(self,):
        if self.__challenge_selected:
            msg = f"\n[ 🟢 ] You are currently enrolled in : {self.__challenge_data['id']} challenge, {self.__challenge_data['subtitle']}." 
            challenge = self.__challenge_data['id']

        else:
            msg = f"\n[ 🔴 ] You have not yet selected any challenge."
            challenge = None
        print(msg)
        return challenge

    @property
    def my_rank(self,):
        
        if self.__challenge_selected:
            self.leaderboard(to_print=False)
            int_rank = self.__rank
            if int_rank == 0:
                rank = f"not yet"
            elif str(int_rank)[-1] == "1":
                rank = f"{int_rank}st"
            elif str(int_rank)[-1] == "2":
                rank = f"{int_rank}nd"
            elif str(int_rank)[-1] == "3":
                rank = f"{int_rank}rd"
            else:
                rank = f"{int_rank}th"
            msg = f"\n[ 🟢 ] You are {rank} on the leaderboad of {self.__challenge_data['id']} challenge, Go on..." 
        else:
            msg = f"\n[ 🔴 ] You have not yet selected any challenge."
            rank = 0
        print(msg)
        return rank

# Account
## Sign In
    def __signin(self, username ,fixed_password=None):
        
        url = "https://api.zindi.africa/v1/auth/signin"
        if fixed_password is None:
            password = getpass(prompt='Your password\n>> ')
        else:
            password = fixed_password
        data = {"username": username, "password": password }


        response = requests.post( url, data=data , headers=self.__headers )
        response = response.json()['data']
        try: 
            print( f"[ 🔴 ] {response['errors']}" )
        except:
            print( f"\n[ 🟢 ] 👋🏾👋🏾 Welcome {response['user']['username'] } 👋🏾👋🏾\n" )
            self.__auth_data = response


# Challenge
## Select a challenge to participate in
    def select_a_challenge(self, reward='all', kind='all', active='all', fixed_index=None):
        
        headers = self.__headers 
        url = self.__base_api 
        challenges_data = get_challenges(reward=reward, kind=kind, active=active, url=url, headers=headers )
        print_challenges( challenges_data=challenges_data )
        n_challenges = challenges_data.shape[0]

        if fixed_index is None:
            challenge_index = challenge_idx_selector(n_challenges)
        else:
            error_msg = f"\n[ 🔴 ] The parameter 'fixed_index' must be an integer in range(0, {n_challenges}) to be valid.\n"
            try:
                if isinstance(fixed_index, int) and (fixed_index > -1) :
                    challenge_index = fixed_index
                    if (challenge_index > n_challenges) :
                        raise Exception(error_msg)
                else:
                    raise Exception(error_msg)
            except Exception as e:
                print("\n[ 🔴 ] The parameter 'fixed_index' value must be None or a valid integer.\n")
                print(e)
        if challenge_index > -1 :
            self.__challenge_data = challenges_data.iloc[challenge_index]
            self.__api = f"{self.__base_api}/{self.__challenge_data['id']}"
            self.__challenge_selected = True

            print(f"\n[ 🟢 ] You choose the challenge : {self.__challenge_data['id']}, {self.__challenge_data['subtitle']}.\n")
            
            

## Download dataset
    def download_dataset(self, destination="." ):
        if os.path.isdir(destination):
            if self.__challenge_selected :
                headers = {**self.__headers, "auth_token":self.__auth_data['auth_token'] }
                url = self.__api

                response = requests.get( url,  headers=headers )
                datafiles = response.json()['data']['datafiles']

                # DOWNLOAD FILES USING ANOTHER METHOD TO SAVE THE ABILITY OF MULTIPROCESSING
                [ download(url=f"{url}/files/{data['filename']}", filename=os.path.join(destination, data['filename']), headers=headers) 
                for data in datafiles]
                
            else:
                print(f"\n[ 🔴 ] You have to select a challenge before to downoad a dataset, use the select_a_challenge method before.\n")
        else:
            print(f"\n[ 🔴 ] You have to choose a correct destination's path for the dataset.\n")

## Push submission file
    def submit(self, filepaths=[], comments=[]):

        if self.__challenge_selected :
            headers = {**self.__headers, "auth_token":self.__auth_data['auth_token'] }
            url = f"{self.__api}/submissions"
            allowed_extensions = [ 'csv', ]
            if len(comments) < len(filepaths):
                n_blank_comment = len(filepaths) - len(comments)
                comments += ['']*n_blank_comment

            for filepath, comment in zip(filepaths, comments):
                extension = filepath.split(".")[-1].strip().lower()
                if extension in allowed_extensions:
                    if os.path.isfile(filepath):
                        file = {"file": open(filepath, 'rb')} # Loading the file to be submitted
                        data = {"comment": comment}
                        print(f"[INFO] Submiting file : {filepath} , wait ...")
                        response = requests.post(url, headers=headers, files=file, data=data,)
                        response = response.json()['data']
                        try:
                            print(f"\n[ 🔴 ] Something wrong with file :{filepath} ,\n{response['errors']}\n")
                        except:
                            print(f"\n[ 🟢 ] Submission ID: {response['id'] } - File submitted : {filepath}\n")
                    else:
                        print(f"\n[ 🔴 ] File doesn't exists, please verify this filepath : {filepath}\n")
                else:
                    print(f"\n[ 🔴 ] Submission file must be a CSV file ( .csv ), please verify this filepath : {filepath}\n")
        else:
            print(f"\n[ 🔴 ] You have to select a challenge before to push any submission file, use the select_a_challenge method before.\n")

## Show leaderboard
    def leaderboard(self, to_print=True):

        if self.__challenge_selected :
            headers = {**self.__headers, "auth_token":self.__auth_data['auth_token'] }
            per_page = 100000
            url = f"{self.__api}/participations"
            params_in_url = { "page": 0, "per_page": per_page,}

            response = requests.get( url, headers=headers, params=params_in_url )
            response = response.json()['data']
            try:
                print(f"\n[ 🔴 ] {response['errors']}\n")
            except:
                challengers_data = response
                self.challengers_data = response
                self.__rank = user_on_lb(challengers_data, challenge_id=self.__challenge_data['id'], username=self.__auth_data['user']['username'], headers=headers)
                if to_print:
                    print_lb(challengers_data=challengers_data, user_rank=self.__rank)
        else:
            print(f"\n[ 🔴 ] You have to select a challenge before to get the leaderboard, use the select_a_challenge method before.\n")
    
## Show Submission-board

    def submission_board(self, ):
        #to add : number of submission, available subissions to do
        if self.__challenge_selected :
            url = f"{self.__api}/submissions"
            headers = {**self.__headers, "auth_token":self.__auth_data['auth_token'] }

            params_in_url = { "per_page": 1000 } # per_page : max number of subimission to retrieve
            response = requests.get( url, headers=headers, params=params_in_url )
            response = response.json()['data']
            try:
                print(f"\n[ 🔴 ] {response['errors']}\n")
            except:
                print_submission_board(submissions_data=response)
        else:
            print(f"\n[ 🔴 ] You have to select a challenge before to get the submission-board, use the select_a_challenge method before.\n")


# Team
## Create
    def create_team(self, team_name=""):

        if self.__challenge_selected :
            headers = {**self.__headers, "auth_token":self.__auth_data['auth_token'] }
            url = f"{self.__api}/my_team"
            data = {"title": team_name}

            response = requests.post( url, headers=headers, data=data )
            response = response.json()['data']
            try:
                print(f"\n[ 🔴 ] {response['errors']}\n")
            except:
                print(f"\n[ 🟢 ] {response}\n")
        else:
            print(f"\n[ 🔴 ] You have to select a challenge before to manage your team, use the select_a_challenge method before.\n")

## Team Up
    def team_up(self, zindians=[]):

        if self.__challenge_selected :
            headers = {**self.__headers, "auth_token":self.__auth_data['auth_token'] }
            url = f"{self.__api}/my_team/invite"

            for zindian in zindians:
                data = {"username": zindian}
                response = requests.post( url, headers=headers, data=data )
                response = response.json()['data']
                try:
                    print(f"\n[ 🔴 ] {response['errors']}\n")
                except:
                    print(f"\n[ 🟢 ] {response}\n")
        else:
            print(f"\n[ 🔴 ] You have to select a challenge before to manage your team, use the select_a_challenge method before.\n")

## Disband
    def disband_team(self, ):

        if self.__challenge_selected :
            headers = {**self.__headers, "auth_token":self.__auth_data['auth_token'] }
            url = f"{self.__api}/my_team"

            response = requests.delete( url, headers=headers,)
            response = response.json()['data']
            try:
                print(f"\n[ 🔴 ] {response['errors']}\n")
            except:
                print(f"\n[ 🟢 ] {response}\n")
        else:
            print(f"\n[ 🔴 ] You have to select a challenge before to manage your team, use the select_a_challenge method before.\n")
