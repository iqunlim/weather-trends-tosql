# Steam Games Dataset: Analyzing ratings based on positive vs negative ratings

## Data Source: 
[Steam Games Dataset: Kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)

## Business Question:
"Of a random selection of some number of steam games specified by the user, what are the the average ratings of games based on positive and negative reviews"

## Cleaning Steps:
1. There was an extra comma causing the rows to disjoint, so we must rename all of the columns to account for this
2. Take a random sample of the data of X entries specified by the user
3. Reset the index and restart from 1, as the original index was scrambled around.
4. Sort by App ID, for clarity
5. Combine bad row back with its original row. If the dataset was dumped properly with string delimeters this would be unnecessary
6. Drop unneeded columns like images and movies, including the bad row that was combined wrong
7. Remove adult games. These tend to have skewed results and many are of poor quality and not representative of the greater dataset
8. Finally, drop games that have no reviews. We are looking primarily at the positive and negative review counts