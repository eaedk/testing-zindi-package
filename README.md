# zindi-package

## Description

A user-friendly ZINDI package which allow Zindians to achieve all available tasks on ZINDI Platform using this package.

## Installation
Copy and Paste the instruction below in a Terminal or Jupyter Notebook.
```bash
pip install git+https://github.com/eaedk/testing-zindi-package.git
```

## Usage

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

In progress 🚧 . Check the progression state in the `features.txt` file.

## Documentation
We will update this table soon ...
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
