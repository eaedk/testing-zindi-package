import datetime
import os
from getpass import getpass

import pandas as pd
import requests

from zindi import utils


class Zindian:
    """Zindi user-friendly account manager."""

    def __init__(self, username, password=None):
        """Sing in to the Zindi platform as a user.

        Parameters
        ----------
        username : string
            The username for an account on Zindi.
        password : string, default=None
            The user's password.

        """
        self._username = username
        self._base_url = "https://api.zindi.africa/v1"
        self._challenge_selected = False
        self._headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
        self._signin(username, password)

    @property
    def which_challenge(self):
        """Get information about the currently selected challenge."""

        self._check_if_a_challenge_is_selected()

        print(f"""
[ 🟢 ] You are currently enrolled in: {self._challenge_data['id']} challenge,
    {self._challenge_data['subtitle']}.""")

        return self._challenge_data['id']

    @property
    def my_rank(self,):
        """Get the user's rank on the leaderboard for the selected challenge.
        """
        self._check_if_a_challenge_is_selected()

        # Get leaderboard information
        self.leaderboard(to_print=False)
        # Nicely format the rank
        if self._user_rank == 0:
            rank = "not yet"
        elif self._user_rank in range(11, 20) or self._user_rank % 10 == 0:
            rank = f"{self._user_rank}th"
        elif self._user_rank % 10 == 1:
            rank = f"{self._user_rank}st"
        elif self._user_rank % 10 == 2:
            rank = f"{self._user_rank}nd"
        elif self._user_rank % 10 == 3:
            rank = f"{self._user_rank}rd"
        else:
            rank = f"{self._user_rank}th"
        print(f"""
[ 🟢 ] You are {rank} on the leaderboad for {self._challenge_data['id']} \
challenge. Carry on...
""")
        return self._user_rank

    @property
    def remaining_submissions(self):
        """Get the number of remaining submissions for the selected
        challenge.

        Returns
        -------
        free_submissions : int
            The number of remaining submissions.
        """
        self._check_if_a_challenge_is_selected()

        daily_sub_limit = utils.n_subimissions_per_day(
            url=self._competition_url, headers=self._headers)

        # Get user's submission data
        self.submission_board(to_print=False)
        submissions_df = pd.DataFrame(self._submission_data)

        if submissions_df.shape[0] != 0:  # If submissions have been made
            # Select useful columns
            submissions_df = submissions_df[
                ["id", "status", "created_at", "filename"]
            ]
            # Make time-zone aware
            submissions_df['created_at'] = pd.to_datetime(
                submissions_df['created_at']
            )
            submissions_df['now'] = pd.to_datetime(
                datetime.datetime.utcnow()
            ).tz_localize('UTC')
            submissions_df['delta'] = (
                submissions_df['now'] - submissions_df['created_at']
            )
            n_submitted_today = submissions_df[
                (submissions_df.status.isin(["successful", "initial"]))
                & (submissions_df.delta.dt.days < 1)
            ].shape[0]
            free_submissions = daily_sub_limit - n_submitted_today
        else:
            free_submissions = daily_sub_limit

        print(f"""
[ 🟢 ] You have {free_submissions} remaining submissions for the challenge \
{self._challenge_data['id']}
""")

        return free_submissions

    def _signin(self, username, password=None):
        """Sing in to the Zindi platform.

        Parameters
        ----------
        username : string
            The username for the user's account on Zindi.
        password : string, default=None
            The user's password.
        """
        if password is None:
            password = getpass(prompt='Please enter your password: ')
        # Sign in using the collected username and password
        response = requests.post(
            url=f"{self._base_url}/auth/signin", headers=self._headers,
            data={"username": username, "password": password}
        ).json()['data']

        if "errors" in response:
            raise Exception(f"[ 🔴 ] {response['errors']}")
        else:
            print(f"""
[ 🟢 ] 👋🏾👋🏾 Welcome {response['user']['username'] } 👋🏾👋🏾""")
        # Add auth token to headers
        self._headers["auth_token"] = response["auth_token"]

    def _check_if_a_challenge_is_selected(self):
        """Check whether a challenge is selected. Raises an exception if none
        is currently selected.
        """
        if not self._challenge_selected:
            raise Exception("[ 🔴 ] Please select a challenge first")

    def select_a_challenge(self, reward='all', kind='all', active='all',
                           fixed_index=None):
        """Select a challenge among those available on Zindi.

        Parameters
        ----------
        reward : {'prize', 'points', 'knowledge' , 'all'}, default='all'
            The type of prize for the challenges.
        kind : {'competition', 'hackathon', 'all'}, default='all'
            The kind of challenge.
        active : {True, False, 'all'}, default='all'
            The status of the challenges.
        fixed_index : int, default=None
            The set index of the selected challenge (for tests).
        """
        challenges_data = utils.get_challenges(
            reward=reward, kind=kind, active=active, headers=self._headers,
            url=f'{self._base_url}/competitions'
        )
        n_challenges = challenges_data.shape[0]

        if fixed_index is None:
            utils.print_challenges(challenges_data=challenges_data)
            challenge_index = utils.challenge_idx_selector(n_challenges)

        elif isinstance(fixed_index, int) and (fixed_index > -1):
            challenge_index = fixed_index
            if (challenge_index > n_challenges):
                raise Exception('Invalid challenge_index > n_challenges')
        else:
            raise Exception("""[ 🔴 ] The parameter 'fixed_index' value must \
be None or a valid integer.""")

        if challenge_index > -1:
            self._challenge_data = challenges_data.iloc[challenge_index]
            self._competition_url = f"""{self._base_url}/competitions/\
{self._challenge_data['id']}"""
            self._challenge_selected = True

            print(f"""
[ 🟢 ] You have chosem the challenge : {self._challenge_data['id']},
    {self._challenge_data['subtitle']}.
""")
            utils.join_challenge(
                url=f"{self._competition_url}/participations",
                headers=self._headers)

    def download_dataset(self, destination=".", make_destination=True):
        """Download the dataset for the selected challenge.

        Parameters
        ----------
        destination : str, default='.'
            The dataset's destination folder.
        """
        self._check_if_a_challenge_is_selected()

        if make_destination and not os.path.isdir(destination):
            os.makedirs(destination, exist_ok=True)

        response = requests.get(
            self._competition_url, headers=self._headers
        ).json()['data']

        [utils.download(
            url=f"{self._competition_url}/files/{data['filename']}",
            headers=self._headers,
            filename=os.path.join(destination, data['filename']))
            for data in response['datafiles']]

    def submit(self, filepaths=None, comments=None):
        """Push submission files for the selected challenge to the Zindi
        platform.

        Parameters
        ----------
        filepaths : list
            The filepaths of submission files to push.
        comments : list
            The comments for submission files to push.
        """
        self._check_if_a_challenge_is_selected()

        allowed_extensions = ['csv']

        if len(comments) != len(filepaths):
            raise Exception('Unmatching number of files and comments')

        for filepath, comment in zip(filepaths, comments):
            extension = filepath.split(".")[-1].strip().lower()
            if extension in allowed_extensions:
                if os.path.isfile(filepath):
                    try:
                        response = utils.upload(
                            filepath=filepath, comment=comment,
                            url=f"{self._competition_url}/submissions",
                            headers=self._headers,)
                        response = response.json()['data']
                        print(f"""
[ 🟢 ] Submission ID: {response['id'] } - File submitted: {filepath}\n""")
                    except Exception:
                        print(f"""
[ 🔴 ] Something is wrong with file: {filepath} ,\n{response['errors']}\n""")

                else:
                    print(f"""
[ 🔴 ] File doesn't exists, please verify this filepath : {filepath}\n""")
            else:
                print(f"""
[ 🔴 ] Submission file must be a CSV file ( .csv ),
    please verify this filepath : {filepath}\n""")

    def leaderboard(self, to_print=True):
        """Get the leaderboard and update the user rank for the selected
        challenge.

        Parameters
        ----------
        to_print : boolean, default=True
            Wether to display the leaderboard or not.
        """
        self._check_if_a_challenge_is_selected()

        response = requests.get(
            f"{self._competition_url}/participations", headers=self._headers,
            params={"page": 0, "per_page": 1000}
        ).json()['data']

        if "errors" in response:
            raise Exception(f"[ 🔴 ] {response['errors']}")
        else:
            self._user_data = response
            self._user_rank = utils.user_on_lb(
                challengers_data=self._user_data, headers=self._headers,
                challenge_id=self._challenge_data['id'],
                username=self._username,)

            if to_print:
                utils.print_lb(challengers_data=self._user_data,
                               user_rank=self._user_rank)

    def submission_board(self, to_print=True):
        """Get the submission-board for the selected challenge and update
        _submission_data to compute remaining submissions.

        Parameters
        ----------
        to_print : boolean, default=True
            Whether to display the submission-board or not.
        """
        self._check_if_a_challenge_is_selected()

        response = requests.get(
            f'{self._competition_url}/submissions', headers=self._headers,
            params={"per_page": 1000}
        ).json()['data']

        if "errors" in response:
            raise Exception(f"[ 🔴 ] {response['errors']}")
        else:
            self._submission_data = response

            if to_print:
                utils.print_submission_board(self._submission_data)

    def create_team(self, team_name, teammates=None):
        """Create a team for the selected challenge.

        Parameters
        ----------
        team_name : string
            Name of the team to create.
        teammates : list, default=None
            List of users you want to invite to be part of your team.
        """
        self._check_if_a_challenge_is_selected()

        response = requests.post(
            f"{self._competition_url}/my_team", headers=self._headers,
            data={"title": team_name}
        ).json()['data']

        if "errors" in response:
            if 'Leader can only be' not in response['errors']['base']:

                raise Exception(f"[ 🔴 ] {response['errors']['base']}")
            elif 'Leader can only be' in response['errors']['base']:
                print("\n[ 🟢 ] You are already the leader of a team.\n")
            else:
                print(
                    f"""
[ 🟢 ] Your team is well created as :{response['title']}
""")
            # Invite team-mates
            if len(teammates) > 0:
                self.team_up(zindians=teammates)
            else:
                print("""You can send invitation to join your team using the \
teamup function""")

    def team_up(self, zindians=None):
        """Create a team of users for the selected challenge.

        Parameters
        ----------
        zindians : list, default=None
            List of user usernames of Zindians.
        """
        self._check_if_a_challenge_is_selected()

        for zindian in zindians:
            # Send team-up request
            response = requests.post(
                f"{self._competition_url}/my_team/invite",
                headers=self._headers, data={"username": zindian}
            ).json()['data']

            if ("errors" in response):
                if 'is already invited' in response['errors']['base']:
                    print(f"""
[ 🟢 ] An invitation has been sent already to {zindian} to join your team""")
                else:
                    raise Exception(f"[ 🔴 ] {response['errors']}")

# TODO add kick function to kick-off some selected teammates...
# TODO add team status (invited users, teammates)
    def disband_team(self):
        """Disband a team in the selected challenge."""
        self._check_if_a_challenge_is_selected()

        # Send request to delete team
        response = requests.delete(
            f"{self._competition_url}/my_team", headers=self._headers
        ).json()['data']

        if "errors" in response:
            raise Exception(f"[ 🔴 ] {response['errors']}")
        else:
            print(f"\n[ 🟢 ] {response}\n")
