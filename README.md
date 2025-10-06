# Steam Games Dataset: Analyzing ratings based on positive vs negative ratings

## Data Source: 
[Steam Games Dataset: Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)

## Business Question:
"Of a random selection of some number of steam games specified by the user, what sort of correlation is there between metacritic reviews and positive/negative ratios of user reviews"

## Cleaning Steps:
1. There was an extra comma causing the rows to disjoint, so we must rename all of the columns to account for this
2. Take a random sample of the data of X entries specified by the user
3. Reset the index and restart from 1, as the original index was scrambled around.
4. Sort by App ID, for clarity
5. Combine bad row back with its original row. If the dataset was dumped properly with string delimeters this would be unnecessary
6. Drop unneeded columns like images and movies, including the bad row that was combined wrong
7. Remove adult games. These tend to have skewed results and many are of poor quality and not representative of the greater dataset
8. Finally, drop games that have no reviews. We are looking primarily at the positive and negative review counts

# Kaggle
Please check the kaggle documentation on how to pull the dataset. Please keep in mind that it is A VERY LARGE REQUEST (>1GB) in size, so try and avoid
hitting their servers over and over.

I am using the kaggle package in order to pull it, as they do not prefer direct API requests to the download endpoint without going through it and cant guarantee it will cache correctly if you do.


# Args

`--count`: Sample size to check through, defaults to 10. (I would suggest 10,000 at least)

`--source`: For my dataset, please use `fronkongames/steam-games-dataset` with no url

`--table`: Defaults to `api_data`

`--db-path`: Database output path: defaults to `output.db`

`--verbose`: FLAG: Verbose debug logging.