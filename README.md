# zindi package

A user-friendly Zindi package which helps Zindians get things done on the Zindi platform.

## Installation

```bash
pip install git+https://github.com/eaedk/testing-zindi-package.git
```

Or even:

```bash
pip install https://github.com/eaedk/testing-zindi-package/archive/master.tar.gz
```

## Usage

Check out the [demo colab notebook][colab notebook]

```python
# create a user object
from zindi.user import Zindian

user = Zindian(username="your-username")

# desired output:
# [ 🟢 ] 👋🏾👋🏾 Welcome your-username 👋🏾👋🏾

user.select_a_challenge()  # Select a Zindi challenge

user.which_challenge  # Get information about the selected challenge

user.leaderboard()  # Show the Leaderboard for the selected challenge

user.my_rank  # Get the user's leaderboard rank

user.remaining_submissions  # See how many submission you can still push to Zindi

user.submission_board()  # Show the user's Submission-board of the selected challenge

user.download_dataset(destination="tests/dataset")  # Download the dataset for the selected challenge

# Push a submission to Zindi
user.submit(filepaths=['tests/dataset/SampleSubmission.csv'],
            comments=['initial submission']) 

user.remaining_subimissions  # Check how many submissions you still have

user.submission_board()  # View your updated Submission-board

user.create_team(team_name="New Team")  # Create a team
```

## Status

Work in progress 🚧 . All functions listed in **Usage** above work, but please share issues you experience, and request features that you need.

## Contributers

|  Emmanuel KOUPOH                     |   Cédric MANOUAN                  |  Muhamed TUO                          |
|--------------------------------------|-----------------------------------|---------------------------------------|
|[eaedk][eaedk_github]                 |[dric2018][dric_github]            |[NazarioR9][nazario_github]            |
|[Emmanuel on linkedin][eaedk_linkedin]|[Cedric on linkedin][dric_linkedin]|[Muhamed on linkedin][nazario_linkedin]|
|[@eaedk😂][eaedk_zindi]               |[@Zeus😆][dric_zindi]              |[@Nazario😁][nazario_zindi]            |

Dont forget to visit [Zindi][zindi]

[![zindi logo](images/zindi.jpg)][zindi]

[colab notebook]: https://colab.research.google.com/drive/1zzAUWkJ8R5GQzxsdJ5i7XTxaGe2tmUF4?usp=sharing
[eaedk_github]: https://github.com/eaedk
[eaedk_linkedin]: https://www.linkedin.com/in/esaïe-alain-emmanuel-dina-koupoh-7b974a17a
[eaedk_zindi]: https://zindi.africa/users/eaedk
[dric_github]: https://github.com/dric2018
[dric_linkedin]: https://www.linkedin.com/in/cédric-pascal-emmanuel-manouan-ba9ba1181
[dric_zindi]: https://zindi.africa/users/I_am_Zeus_AI
[nazario_github]: https://github.com/NazarioR9
[nazario_linkedin]: https://www.linkedin.com/in/muhamed-tuo-b1b3a0162
[nazario_zindi]: https://zindi.africa/users/Muhamed_Tuo
[zindi]: https://zindi.africa/
