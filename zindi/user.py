# Imports

import sys, os

## To avoid errors of importing before instalation
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from zindi.utils import *
from getpass import getpass

import pandas as pd
import requests, datetime
from tqdm import tqdm


# Class declaration and init
class Zindian:
    """Zindi user-friendly account manager."""

    def __init__(self, username, fixed_password=None):
        """Singin, connect user to the Zindi platform.

        Parameters
        ----------
        username : string
            The challenger's username.
        fixed_password : string, default=None
            The challenger's password, for test.

        """
        self.__headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        }
        self.__base_api = "https://api.zindi.africa/v1/competitions"
        self.__auth_data = self.__signin(
            username, fixed_password
        )  # auth & user data from Zindi server after signin
        self.__challenge_selected = False

    # Properties
    @property
    def which_challenge(
        self,
    ):
        """Property: Get the information about the selected challenge."""

        if self.__challenge_selected:
            msg = f"\n[ 🟢 ] You are currently enrolled in : {self.__challenge_data['id']} challenge,\n\t{self.__challenge_data['subtitle']}.\n"
            challenge = self.__challenge_data["id"]
        else:
            msg = f"\n[ 🔴 ] You have not yet selected any challenge.\n"
            challenge = None
        print(msg)
        return challenge

    @property
    def my_rank(
        self,
    ):
        """Property: Get the user rank on the leaderboard for the selected challenge."""

        if self.__challenge_selected:
            self.leaderboard(to_print=False)
            int_rank = self.__rank
            if int_rank == 0:
                rank = f"not yet"
            elif str(int_rank)[-1] == "1":
                if str(int_rank)[-2] == "1":
                    rank = f"{int_rank}th"
                else:
                    rank = f"{int_rank}st"
            elif str(int_rank)[-1] == "2":
                rank = f"{int_rank}nd"
            elif str(int_rank)[-1] == "3":
                rank = f"{int_rank}rd"
            else:
                rank = f"{int_rank}th"
            msg = f"\n[ 🟢 ] You are {rank} on the leaderboad of {self.__challenge_data['id']} challenge, Go on...\n"
        else:
            msg = f"\n[ 🔴 ] You have not yet selected any challenge.\n"
            int_rank = 0
        print(msg)
        return int_rank

    @property
    def remaining_subimissions(
        self,
    ):
        """Property: Get the number of now remaining submissions for the selected challenge.

        Returns
        -------
        free_submissions : int, default=n_subimissions_per_day.
            The number of now remaining submissions.
        """
        if self.__challenge_selected:
            url = self.__api
            headers = {**self.__headers, "auth_token": self.__auth_data["auth_token"]}

            free_submissions = None
            n_sub = n_subimissions_per_day(url=url, headers=headers)
            n_submitted_today = 0
            self.submission_board(to_print=False)
            sb_time = pd.DataFrame(self.__sb_data)

            if n_sub > 0:
                if sb_time.shape[0] != 0:
                    sb_time = sb_time[
                        ["id", "status", "created_at", "filename"]
                    ]  # get useful columns
                    sb_time["created_at"] = pd.to_datetime(
                        sb_time["created_at"]
                    )  # .tz_localize('UTC')
                    sb_time["now"] = pd.to_datetime(
                        datetime.datetime.utcnow()
                    ).tz_localize("UTC")
                    sb_time["delta"] = sb_time["now"] - sb_time["created_at"]
                    n_submitted_today = sb_time[
                        (sb_time.status.isin(["successful", "initial"]))
                        & (sb_time.delta.dt.days < 1)
                    ].shape[0]
                    free_submissions = n_sub - n_submitted_today
                else:
                    free_submissions = n_sub
            else:
                free_submissions = n_sub
            msg = f"\n[ 🟢 ] You have {free_submissions} remaining submissions for the challenge {self.__challenge_data['id']}.\n"
            print(msg)
        else:
            msg = f"\n[ 🔴 ] You have not yet selected any challenge.\n"
            print(msg)
        return free_submissions

    # Account
    ## Sign In
    def __signin(self, username, fixed_password=None):
        """Singin, connect user to the Zindi platform.

        Parameters
        ----------
        username : string
            The challenger's username.
        fixed_password : string, default=None
            The challenger's password, for test.

        Returns
        -------
        auth_data :  dictionary | json
            The json's response of the sign in request.
        """

        auth_data = None
        url = "https://api.zindi.africa/v1/auth/signin"
        if fixed_password == None:
            password = getpass(prompt="Your password\n>> ")
        else:
            password = fixed_password
        data = {"username": username, "password": password}

        response = requests.post(url, data=data, headers=self.__headers)
        response = response.json()["data"]
        if "errors" in response:
            error_msg = f"[ 🔴 ] {response['errors']}"
            raise Exception(error_msg)
        else:
            print(f"\n[ 🟢 ] 👋🏾👋🏾 Welcome {response['user']['username'] } 👋🏾👋🏾\n")
            auth_data = response
        return auth_data

    # Challenge
    ## Select a challenge to participate in
    def select_a_challenge(
        self, reward="all", kind="all", active="all", fixed_index=None
    ):
        """Select a challenge among those available on Zindi, using filter options.

        Parameters
        ----------
        reward : {'prize', 'points', 'knowledge' , 'all'}, default='all'
            The reward of the challenges for top challengers.
        kind : {'competition', 'hackathon', 'all'}, default='all'
            The kind of the challenges.
        active : {True, False, 'all'}, default='all'
            The status of the challenges.

        fixed_index : int, default=None
            The set index of the selected challenge : for test.

        """

        headers = self.__headers
        url = self.__base_api
        challenges_data = get_challenges(
            reward=reward, kind=kind, active=active, url=url, headers=headers
        )
        n_challenges = challenges_data.shape[0]

        if fixed_index is None:
            print_challenges(challenges_data=challenges_data)
            challenge_index = challenge_idx_selector(n_challenges)
        else:
            error_msg = f"\n[ 🔴 ] The parameter 'fixed_index' must be an integer in range(0, {n_challenges}) to be valid.\n"
            try:
                if isinstance(fixed_index, int) and (fixed_index > -1):
                    challenge_index = fixed_index
                    if challenge_index > n_challenges:
                        raise Exception(error_msg)
                else:
                    raise Exception(error_msg)
            except Exception as e:
                print(
                    "\n[ 🔴 ] The parameter 'fixed_index' value must be None or a valid integer.\n"
                )
                raise Exception(e)
        if challenge_index > -1:
            self.__challenge_data = challenges_data.iloc[challenge_index]
            self.__api = f"{self.__base_api}/{self.__challenge_data['id']}"
            self.__challenge_selected = True
            headers = {**self.__headers, "auth_token": self.__auth_data["auth_token"]}
            url = f"{self.__api}/participations"
            print(
                f"\n[ 🟢 ] You choose the challenge : {self.__challenge_data['id']},\n\t{self.__challenge_data['subtitle']}.\n"
            )
            join_challenge(
                url=url,
                headers=headers,
            )

    ## Download dataset
    def download_dataset(self, destination=".", make_destination=True):
        """Download the dataset of the selected challenge.

        Parameters
        ----------
        destination : int, default='.'
            The dataset's destination folder .
        make_destination : boolean, default=True
            Create destination folder if doesn't exist.

        """

        if not os.path.isdir(destination):
            os.makedirs(destination, exist_ok=True)
        if self.__challenge_selected:
            headers = {**self.__headers, "auth_token": self.__auth_data["auth_token"]}
            url = self.__api

            response = requests.get(url, headers=headers)
            datafiles = response.json()["data"]["datafiles"]

            # DOWNLOAD FILES USING ANOTHER METHOD TO SAVE THE ABILITY OF MULTIPROCESSING
            [
                download(
                    url=f"{url}/files/{data['filename']}",
                    filename=os.path.join(destination, data["filename"]),
                    headers=headers,
                )
                for data in datafiles
            ]

        else:
            error_msg = f"\n[ 🔴 ] You have to select a challenge before to downoad a dataset,\n\tuse the select_a_challenge method before.\n"
            raise Exception(error_msg)

    ## Push submission file
    def submit(self, filepaths=[], comments=[]):
        """Push submission files for the selected challenge to Zindi platform.

        Parameters
        ----------
        filepaths : list
            The filepaths of submission files to push.
        comments : list
            The comments of submission files to push.

        """

        if self.__challenge_selected:
            headers = {**self.__headers, "auth_token": self.__auth_data["auth_token"]}
            url = f"{self.__api}/submissions"
            # self.submit__ = url
            allowed_extensions = [
                "csv",
            ]
            if len(comments) < len(filepaths):
                n_blank_comment = len(filepaths) - len(comments)
                comments += [""] * n_blank_comment

            for filepath, comment in zip(filepaths, comments):
                extension = filepath.split(".")[-1].strip().lower()
                if extension in allowed_extensions:
                    if os.path.isfile(filepath):
                        # print(f"[INFO] Submiting file : {filepath} , wait ...")
                        response = upload(
                            filepath=filepath,
                            comment=comment,
                            url=url,
                            headers=headers,
                        )
                        response = response.json()["data"]
                        try:
                            print(
                                f"\n[ 🔴 ] Something wrong with file :{filepath} ,\n{response['errors']}\n"
                            )
                        except:
                            print(
                                f"\n[ 🟢 ] Submission ID: {response['id'] } - File submitted : {filepath}\n"
                            )
                    else:
                        print(
                            f"\n[ 🔴 ] File doesn't exists, please verify this filepath : {filepath}\n"
                        )
                else:
                    print(
                        f"\n[ 🔴 ] Submission file must be a CSV file ( .csv ),\n\tplease verify this filepath : {filepath}\n"
                    )
        else:
            error_msg = f"\n[ 🔴 ] You have to select a challenge before to push any submission file,\n\tuse the select_a_challenge method before.\n"
            raise Exception(error_msg)

    ## Show leaderboard
    def leaderboard(self, to_print=True):
        """Get the leaderboard and upadte the user rank for the selected challenge.

        Parameters
        ----------
        to_print : boolean, default=True
            Display the leaderboard or not.

        """

        if self.__challenge_selected:
            headers = {**self.__headers, "auth_token": self.__auth_data["auth_token"]}
            url = f"{self.__api}/participations"
            per_page = 100000
            params_in_url = {
                "page": 0,
                "per_page": per_page,
            }

            response = requests.get(url, headers=headers, params=params_in_url)
            response = response.json()["data"]
            if "errors" in response:
                error_msg = f"\n[ 🔴 ] {response['errors']}\n"
                raise Exception(error_msg)
            else:
                self.__challengers_data = response
                self.__rank = user_on_lb(
                    challengers_data=self.__challengers_data,
                    challenge_id=self.__challenge_data["id"],
                    username=self.__auth_data["user"]["username"],
                    headers=headers,
                )
                if to_print:
                    print_lb(
                        challengers_data=self.__challengers_data, user_rank=self.__rank
                    )
        else:
            error_msg = f"\n[ 🔴 ] You have to select a challenge before to get the leaderboard,\n\tuse the select_a_challenge method before.\n"
            raise Exception(error_msg)

    ## Show Submission-board
    def submission_board(self, to_print=True):
        """Get the submission-board for the selected challenge and upadte the private parameters __sb_data for compute remaining submissions.

        Parameters
        ----------
        to_print : boolean, default=True
            Display the submission-board or not.

        """

        # to add : number of submission, available subissions to do
        if self.__challenge_selected:
            url = f"{self.__api}/submissions"
            headers = {**self.__headers, "auth_token": self.__auth_data["auth_token"]}

            params_in_url = {
                "per_page": 1000
            }  # per_page : max number of subimission to retrieve
            response = requests.get(url, headers=headers, params=params_in_url)
            response = response.json()["data"]
            if "errors" in response:
                error_msg = f"\n[ 🔴 ] {response['errors']}\n"
                raise Exception(error_msg)
            else:
                self.__sb_data = response
                # self.sb_data = response # for test
                if to_print:
                    print_submission_board(submissions_data=self.__sb_data)
        else:
            error_msg = f"\n[ 🔴 ] You have to select a challenge before to get the submission-board,\n\tuse the select_a_challenge method before.\n"
            raise Exception(error_msg)

    # Team
    ## Create
    def create_team(self, team_name, teammates=[]):
        """Create a team for the selected challenge.

        Parameters
        ----------
        team_name : string
            Name of the team to create.
        teammates : list
            List of usernames of Zindians you want to invite to be part of your team.

        """

        if self.__challenge_selected:
            headers = {**self.__headers, "auth_token": self.__auth_data["auth_token"]}
            url = f"{self.__api}/my_team"
            data = {"title": team_name}

            response = requests.post(url, headers=headers, data=data)
            response = response.json()["data"]
            if ("errors" in response) and (
                "Leader can only be" not in response["errors"]["base"]
            ):

                error_msg = f"\n[ 🔴 ] {response['errors']['base']}\n"
                raise Exception(error_msg)
            else:
                if ("errors" in response) and (
                    "Leader can only be" in response["errors"]["base"]
                ):
                    print(f"\n[ 🟢 ] You are already the leader of a team.\n")
                else:
                    print(
                        f"\n[ 🟢 ] Your team is well created as :{response['title']}\n"
                    )
                ##### Invite teammates
                if len(teammates) > 0:
                    self.team_up(zindians=teammates)
                else:
                    print(
                        "You can send invitation to join your team using teamup function"
                    )
        else:
            error_msg = f"\n[ 🔴 ] You have to select a challenge before to manage your team,\n\tuse the select_a_challenge method before.\n"
            raise Exception(error_msg)

    ## Team Up
    def team_up(self, zindians=[]):
        """Add challengers to user team for the selected challenge.

        Parameters
        ----------
        zindians : list
            List of challenger's usernames of Zindians to add the team.

        """

        if self.__challenge_selected:
            headers = {**self.__headers, "auth_token": self.__auth_data["auth_token"]}
            url = f"{self.__api}/my_team/invite"

            for zindian in zindians:
                data = {"username": zindian}
                response = requests.post(url, headers=headers, data=data)
                response = response.json()["data"]
                if "errors" in response:
                    if "is already invited" in response["errors"]["base"]:
                        print(
                            f"\n[ 🟢 ] An invitation has been sent already to join your team to: {zindian}\n"
                        )
                    else:
                        error_msg = f"\n[ 🔴 ] {response['errors']}\n"
                        raise Exception(error_msg)
                else:
                    print(
                        f"\n[ 🟢 ] An invitation has been sent to join your team to: {zindian}\n"
                    )

        else:
            error_msg = f"\n[ 🔴 ] You have to select a challenge before to manage your team,\n\tuse the select_a_challenge method before.\n"
            raise Exception(error_msg)

    ## Disband ... think to add kick function to kick-off some selected teammates... think to add team status (invited users, teammates)
    def disband_team(
        self,
    ):
        """Disband user team for the selected challenge."""

        if self.__challenge_selected:
            headers = {**self.__headers, "auth_token": self.__auth_data["auth_token"]}
            url = f"{self.__api}/my_team"

            response = requests.delete(
                url,
                headers=headers,
            )
            response = response.json()["data"]
            if "errors" in response:
                error_msg = f"\n[ 🔴 ] {response['errors']}\n"
                raise Exception(error_msg)
            else:
                print(f"\n[ 🟢 ] {response}\n")
        else:
            error_msg = f"\n[ 🔴 ] You have to select a challenge before to manage your team,\n\tuse the select_a_challenge method before.\n"
            raise Exception(error_msg)
