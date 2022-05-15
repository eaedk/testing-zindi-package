import sys, os

## To avoid errors of importing before instalation
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from zindi.user import Zindian

## FOR TEST
USERNAME, PASSWORD = "test-000000X", "test-000000X"
user = Zindian(username=USERNAME, fixed_password=PASSWORD)

# user.which_challenge

user.select_a_challenge(fixed_index=3) # reward="knowledge" , 

user.which_challenge

# user.leaderboard()

user.my_rank
user.create_team(team_name ='My team' , teammates=['I_am_Zeus_AI', 'Muhamed_Tuo'])

# user.download_dataset(destination="tests/dataset")

# user.submit(filepaths=['tests/dataset/SampleSubmission.csv'], comments=['submission test'])

# user.submission_board()

# user.create_team(team_name="New Team")