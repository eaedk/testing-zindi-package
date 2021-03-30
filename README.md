# zindi package

A user-friendly Zindi package which helps Zindians get things done on the Zindi platform.

## Installation

```bash
pip install git+https://github.com/eaedk/testing-zindi-package.git
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

## Documentation

TODO. For now, please refer to the [demo notebook][colab notebook] and **Usage** section.

## Contributers

<div align='center'>

| <img src='https://media-exp1.licdn.com/dms/image/C5103AQEWceAkHjUwVw/profile-displayphoto-shrink_400_400/0/1582378323644?e=1618444800&v=beta&t=dgTb6nwVBgbNzFOs8CLvoM_p2gYal4t0gStKWvfzcmk' width='100' height='100' style='border-radius:50%; margin:.8cm'> <br>Emmanuel KOUPOH | <img src='https://media-exp1.licdn.com/dms/image/C4D35AQGOLlRWnmK5UA/profile-framedphoto-shrink_800_800/0/1611062726937?e=1613314800&v=beta&t=IpUAuxmIMhOrhzAV9rQe3BTJz-6kSN8CUZK8RKf1Jso' width='100' height='100' style='border-radius:50%; margin:.8cm'> <br>Cédric MANOUAN | <img src='https://media-exp1.licdn.com/dms/image/C4D03AQH1XHqqND9Syg/profile-displayphoto-shrink_400_400/0/1588010132707?e=1618444800&v=beta&t=SHEg3OdAElJk8dUF7UZ-hZr_ydRZV6fRJW-YUgl4Pxw' width='100' height='100' style='border-radius:50%; margin:.8cm'> <br>Muhamed TUO |
|--------------------------------------|-------------------------------|----------------------------------------------|
| [eaedk](https://github.com/eaedk) | [dric2018](https://github.com/dric2018) | [NazarioR9](https://github.com/NazarioR9)|
| [Emmanuel on linkedin](https://www.linkedin.com/in/esaïe-alain-emmanuel-dina-koupoh-7b974a17a) | [Cedric on linkedin](https://www.linkedin.com/in/cédric-pascal-emmanuel-manouan-ba9ba1181) | [Muhamed on linkedin](https://www.linkedin.com/in/muhamed-tuo-b1b3a0162) |
|[@eaedk😂](https://zindi.africa/users/eaedk) | [@Zeus😆](https://zindi.africa/users/I_am_Zeus_AI) |   [@Nazario😁](https://zindi.africa/users/Muhamed_Tuo)   |

Dont forget to visit [Zindi](www.zindi.africa)

<img src='https://pbs.twimg.com/profile_images/1026842061587271680/NHtP1F7r_400x400.jpg' width='200' height='200' style='border-radius:50%; margin:.8cm'>

</div>

[colab notebook]: https://colab.research.google.com/drive/1zzAUWkJ8R5GQzxsdJ5i7XTxaGe2tmUF4?usp=sharing
