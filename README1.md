# Previous Weather Data: X Days Previous

## Data Source
[Open Weather Map](https://openweathermap.org/api/one-call-3/)


## Business Question

"What was temperature in Dallas like throughout the day on days where temperature was above expected user input"


## Summary
Cleaning Steps:

1. Normalizing Json. Much of the data was highly nested.
2. Column Normalization: Keeping columns consistent even if they may change in the future for SQL loading
3. Removing duplicated and unneeded columns
4. Renaming badly named columns that were changed by the flattening to be less than clear
4. Sorting the date in descending order, as we want to look at the oldest data to the newest
5. Filter by the user-provided minimum temperature
6. Modifying the "Wind Direction" To be the closest cardinal direction, instead of angles that are not useful to us.