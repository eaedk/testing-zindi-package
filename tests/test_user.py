import sys, os, unittest

## To avoid errors of importing before instalation
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

######
# from pathlib import Path
# import sys
# path_root = Path(__file__).parents[2]
# sys.path.append(str(path_root))
# print(sys.path)
##########
from zindi.user import Zindian

## FOR TEST

USERNAME, PASSWORD = "test-000000X", "test-000000X"


class Test(unittest.TestCase):
    def setUp(self):
        self.user = Zindian(username=USERNAME, fixed_password=PASSWORD)

    def test_SignIn_positive(
        self,
    ):
        user = Zindian(username=USERNAME, fixed_password=PASSWORD)
        self.assertIsInstance(
            user,
            Zindian,
        )

    def test_SignIn_negative(
        self,
    ):
        with self.assertRaises(Exception) as exception_context:
            Zindian(username=USERNAME, fixed_password="-")
        self.assertEqual(
            str(exception_context.exception).strip(),
            "[ 🔴 ] {'password': 'wrong password'}",
        )

    def test_which_challenge_negative(
        self,
    ):
        self.assertIsNone(self.user.which_challenge)

    def test_which_challenge_positive(
        self,
    ):
        self.assertIsNone(self.user.which_challenge)
        print(self.user.which_challenge)
        print(type(self.user.which_challenge))


# # user.which_challenge # assertIsNotNone

# user.select_a_challenge(fixed_index=3) # reward="knowledge" ,

# user.which_challenge

# # user.leaderboard()

# user.my_rank
# user.create_team(team_name ='My team' , teammates=['I_am_Zeus_AI', 'Muhamed_Tuo'])

# # user.download_dataset(destination="tests/dataset")

# # user.submit(filepaths=['tests/dataset/SampleSubmission.csv'], comments=['submission test'])

# # user.submission_board()

# # user.create_team(team_name="New Team")

if __name__ == "__main__":
    unittest.main()
