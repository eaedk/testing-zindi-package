# zindi-package

## Description

A user-friendly ZINDI package which allow Zindians to achieve all available tasks on ZINDI Platform using this package.

## Usage

```python
# create a user object
from zindi.user import Zindian

my_username = "I_am_Zeus_AI"
user = Zindian(username = my_username)

#desired output
[ 🟢 ] 👋🏾👋🏾 Welcome I_am_Zeus_AI 👋🏾👋🏾

# get current challenge info if seleted
user.which_challenge

# select a new challenge
user.select_a_challenge()

# user.which_challenge

# user.leaderboard()

# user.my_rank

# user.download_dataset(destination="tests/dataset")

user.submit(filepaths=['tests/dataset/SampleSubmission.csv'])

user.submission_board()

user.create_team(team_name="New Team")

```

## Status

In progress 🚧 . Check the progression state in the `features.txt` file.

## Documentation

<table class="table table-bordered table-hover table-condensed">
<thead><tr><th title="Field #1">Source</th>
<th title="Field #2">Element Type</th>
<th title="Field #3">Name</th>
<th title="Field #4">Description</th>
</tr></thead>
<tbody><tr>
<td>utils</td>
<td>function</td>
<td>print_submission_board</td>
<td>Formated print the Zindi&#39;s challenge submission-board as table.</td>
</tr>
<tr>
<td>utils</td>
<td>function</td>
<td>join_challenge</td>
<td>Subscribe to a Zindi&#39;s challenge</td>
</tr>
<tr>
<td>utils</td>
<td>function</td>
<td>get_challenges</td>
<td>Get the available Zindi&#39;s challenges using filter options.</td>
</tr>
<tr>
<td>utils</td>
<td>function</td>
<td>challenge_idx_selector</td>
<td>Get from the keyboard the index of the challenge tha the user want to participate in.</td>
</tr>
<tr>
<td>utils</td>
<td>function</td>
<td>participations</td>
<td>Check if user is in team for a the Zindi&#39;s challenges.</td>
</tr>
<tr>
<td>utils</td>
<td>function</td>
<td>user_on_lb</td>
<td>Get rank of user on the leaderboard for a the Zindi&#39;s challenges.</td>
</tr>
<tr>
<td>utils</td>
<td>function</td>
<td>print_lb</td>
<td>Formated print the Zindi&#39;s challenge leaderboard as table.</td>
</tr>
<tr>
<td>utils</td>
<td>function</td>
<td>print_challenges</td>
<td>Formated print the Zindi&#39;s challenge as table.</td>
</tr>
<tr>
<td>utils</td>
<td>function</td>
<td>download</td>
<td>Download a file with progress bar.</td>
</tr>
<tr>
<td>user</td>
<td>method</td>
<td> </td>
<td> </td>
</tr>
<tr>
<td>user</td>
<td>method</td>
<td> </td>
<td> </td>
</tr>
<tr>
<td>user</td>
<td>method</td>
<td> </td>
<td> </td>
</tr>
<tr>
<td>user</td>
<td>property</td>
<td> </td>
<td> </td>
</tr>
<tr>
<td>user</td>
<td>property</td>
<td> </td>
<td> </td>
</tr>
</tbody></table>