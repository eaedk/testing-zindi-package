import sys, os

## To avoid errors of importing before instalation
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from zindi.user import Zindian

## FOR TEST
USERNAME, PASSWORD = "____", "____"
user = Zindian(username=USERNAME, fixed_password=PASSWORD)

user.which_challenge

user.select_a_challenge(reward="knowledge" , fixed_index=2) # 

user.which_challenge

# user.leaderboard()

user.my_rank

# user.download_dataset(destination="tests/dataset")

# user.submit(filepaths=['tests/dataset/SampleSubmission.csv'], comments=['submission test'])

# user.submission_board()

# user.create_team(team_name="New Team")