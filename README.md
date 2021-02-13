# zindi-package

## Description

A user-friendly ZINDI package which allow Zindians to achieve all available tasks on ZINDI Platform using this package.

## Installation

Copy and Paste the instruction below in a Terminal or Jupyter Notebook.

```bash
pip install git+https://github.com/eaedk/testing-zindi-package.git
```

## Usage

You can check the [colab notebook here](https://colab.research.google.com/drive/1zzAUWkJ8R5GQzxsdJ5i7XTxaGe2tmUF4?usp=sharing)

```python
# create a user object
from zindi.user import Zindian

my_username = "I_am_Zeus_AI"
user = Zindian(username = my_username)

#desired output
[ 🟢 ] 👋🏾👋🏾 Welcome I_am_Zeus_AI 👋🏾👋🏾


user.select_a_challenge()                               # Select a Zindi challenge

user.which_challenge                                    # Get information about the selected challenge

user.leaderboard()                              # Show the Leaderboard of the selected challenge

user.my_rank                                    # Get the user's leaderboard rank

user.remaining_subimissions                         # Get information about how many submission you can still push now to Zindi

user.submission_board()                         # Show the user's Submission-board of the selected challenge

user.download_dataset(destination="tests/dataset") # Download the dataset of the selected challenge

user.submit(filepaths=['tests/dataset/SampleSubmission.csv'], comments=['initial submission']) # Push a submission to Zindi : the SampleSubmission file

user.remaining_subimissions                             # Get information about how many submission you can still push now to Zindi

user.submission_board()                             # Show the Submission-board of the selected challenge

user.create_team(team_name="New Team")             # Create a team for the selected challenge

```

## Status

In progress 🚧 . All listed functions in **Usage** part are working, but please share issues with use and request features that you need.

## Documentation

We will update this table soon ... Now you can refer to the notebook and **Usage** section.

<br>

# Contributers

<div align='center'>


| <img src='https://media-exp1.licdn.com/dms/image/C5103AQEWceAkHjUwVw/profile-displayphoto-shrink_400_400/0/1582378323644?e=1618444800&v=beta&t=dgTb6nwVBgbNzFOs8CLvoM_p2gYal4t0gStKWvfzcmk' width='100' height='100' style='border-radius:50%; margin:.8cm'> <br>Emmanuel KOUPOH                        | <img src='https://media-exp1.licdn.com/dms/image/C4D35AQGOLlRWnmK5UA/profile-framedphoto-shrink_800_800/0/1611062726937?e=1613314800&v=beta&t=IpUAuxmIMhOrhzAV9rQe3BTJz-6kSN8CUZK8RKf1Jso' width='100' height='100' style='border-radius:50%; margin:.8cm'> <br>Cédric MANOUAN                      | <img src='https://media-exp1.licdn.com/dms/image/C4D03AQH1XHqqND9Syg/profile-displayphoto-shrink_400_400/0/1588010132707?e=1618444800&v=beta&t=SHEg3OdAElJk8dUF7UZ-hZr_ydRZV6fRJW-YUgl4Pxw' width='100' height='100' style='border-radius:50%; margin:.8cm'> <br>Muhamed TUO                      |
|--------------------------------------|-------------------------------|----------------------------------------------|
| [eaedk](https://github.com/eaedk) | [dric2018](https://github.com/dric2018) | [NazarioR9](https://github.com/NazarioR9)|
| [Emmanuel on linkedin](https://www.linkedin.com/in/esaïe-alain-emmanuel-dina-koupoh-7b974a17a) | [Cedric on linkedin](https://www.linkedin.com/in/cédric-pascal-emmanuel-manouan-ba9ba1181) | [Muhamed on linkedin](https://www.linkedin.com/in/muhamed-tuo-b1b3a0162) |
|[@eaedk😂](https://zindi.africa/users/eaedk) | [@Zeus😆](https://zindi.africa/users/I_am_Zeus_AI) |   [@Nazario😁](https://zindi.africa/users/Muhamed_Tuo)   |

<br>


Dont forget to visite [ZINDI Plateform](www.zindi.africa)<br>
<img src='https://pbs.twimg.com/profile_images/1026842061587271680/NHtP1F7r_400x400.jpg' width='200' height='200' style='border-radius:50%; margin:.8cm'>


</div>
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Africa&#39;s biggest inter-university machine learning hackathon is back for Round 2!! 🎉😁 <a href="https://twitter.com/hashtag/UmojaHackAfrica2021?src=hash&amp;ref_src=twsrc%5Etfw">#UmojaHackAfrica2021</a> is set to kick off on 27 March! So get your teams together and apply today! 🌈🌍 <a href="https://twitter.com/hashtag/BuildingAITogether?src=hash&amp;ref_src=twsrc%5Etfw">#BuildingAITogether</a> <a href="https://twitter.com/hashtag/ZindiHack?src=hash&amp;ref_src=twsrc%5Etfw">#ZindiHack</a><br>APPLY NOW👉<a href="https://t.co/bNqx0d5Odc">https://t.co/bNqx0d5Odc</a> <a href="https://t.co/Tgd4vZw9pb">pic.twitter.com/Tgd4vZw9pb</a></p>&mdash; Zindi (@ZindiAfrica) <a href="https://twitter.com/ZindiAfrica/status/1359502643849273351?ref_src=twsrc%5Etfw">February 10, 2021</a></blockquote> 