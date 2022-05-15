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

user.download_dataset(destination="t./dataset") # Download the dataset of the selected challenge

user.submit(filepaths=['./dataset/SampleSubmission.csv'], comments=['initial submission']) # Push a submission to Zindi : the SampleSubmission file

user.remaining_subimissions                             # Get information about how many submission you can still push now to Zindi

user.submission_board()                             # Show the Submission-board of the selected challenge

user.create_team(team_name="New Team")             # Create a team for the selected challenge

```

## Status

In progress 🚧 . All listed functions in **Usage** part are working, but please share issues with use and request features that you need.

## Documentation

We will update this table soon ... Now you can refer to the notebook and **Usage** section.

# Contributers

<div align='center'>

| <img src='https://media-exp1.licdn.com/dms/image/C5103AQEWceAkHjUwVw/profile-displayphoto-shrink_100_100/0/1582378323644?e=1658361600&v=beta&t=HLQGLn2wqkq_Utgt3e0hiM-vBGZF8_-RRVAl12PP_N0' width='100' height='100' style='border-radius:50%; margin:.8cm'> <br>Emmanuel KOUPOH                        | <img src='https://dric2018.github.io/static/media/pic1.19034710.png' width='100' height='100' style='border-radius:50%; margin:.8cm'> <br>Cédric MANOUAN                      | <img src='https://media-exp1.licdn.com/dms/image/C4D03AQH1XHqqND9Syg/profile-displayphoto-shrink_400_400/0/1588010132707?e=1658361600&v=beta&t=qRhIGUjwBx9BnThdKR2kgbjkZDh0m2x5mx9FntgKPEA' width='100' height='100' style='border-radius:50%; margin:.8cm'> <br>Muhamed TUO                      |
|--------------------------------------|-------------------------------|----------------------------------------------|
| [eaedk](https://github.com/eaedk) | [dric2018](https://github.com/dric2018) | [NazarioR9](https://github.com/NazarioR9)|
| [Emmanuel on linkedin](https://www.linkedin.com/in/esaïe-alain-emmanuel-dina-koupoh-7b974a17a) | [Cedric on linkedin](https://www.linkedin.com/in/cédric-pascal-emmanuel-manouan-ba9ba1181) | [Muhamed on linkedin](https://www.linkedin.com/in/muhamed-tuo-b1b3a0162) |
|[@eaedk😂](https://zindi.africa/users/eaedk) | [@Zeus😆](https://zindi.africa/users/I_am_Zeus_AI) |   [@Nazario😁](https://zindi.africa/users/Muhamed_Tuo)   |

<br>


Dont forget to visite [ZINDI Plateform](www.zindi.africa)<br>
<img src='https://media-exp1.licdn.com/dms/image/C4D1BAQFlZkR1frDd6w/company-background_10000/0/1632989550932?e=1653228000&v=beta&t=ApaXaPwZhe0UtIQp7gz_wF9eJKNrMMPp0xpnjS3vL9E' width='90%' height='200' style='border-radius:5; margin:.8cm'>


</div>
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Africa&#39;s biggest inter-university machine learning hackathon is back for Round 2!! 🎉😁 <a href="https://twitter.com/hashtag/UmojaHackAfrica2021?src=hash&amp;ref_src=twsrc%5Etfw">#UmojaHackAfrica2021</a> is set to kick off on 27 March! So get your teams together and apply today! 🌈🌍 <a href="https://twitter.com/hashtag/BuildingAITogether?src=hash&amp;ref_src=twsrc%5Etfw">#BuildingAITogether</a> <a href="https://twitter.com/hashtag/ZindiHack?src=hash&amp;ref_src=twsrc%5Etfw">#ZindiHack</a><br>APPLY NOW👉<a href="https://t.co/bNqx0d5Odc">https://t.co/bNqx0d5Odc</a> <a href="https://t.co/Tgd4vZw9pb">pic.twitter.com/Tgd4vZw9pb</a></p>&mdash; Zindi (@ZindiAfrica) <a href="https://twitter.com/ZindiAfrica/status/1359502643849273351?ref_src=twsrc%5Etfw">February 10, 2021</a></blockquote> 