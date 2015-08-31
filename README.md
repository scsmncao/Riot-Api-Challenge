# Riot Games API Challenge 2.0

# Deployment
This website is deploy at patchbypatch.herokuapp.com

# About
This project was developed for Riot Games API Challenge 2.0. The data set contained 400,000 games (200,000 Normal and 200,000 Ranked) from 10 different regions.

The data that was gathered was all from Riot's API. First, I gathered the items from the matches. I made sure to count how many times the item was bought and whether or not the summoner won the match. The champion that the item was bought on was also counted. I separated the data by their regions to future proof it in case I wanted to ever show the data by region. Also, since the data collecting took more than 3 days, it made it so that if the script ever stopped working, I didn't have to start over. 

However, all that told me was the items that the summoner ended the match with. This is problematic since if I bought a Luden's Echo, I also bought a Needlessly Large Rod and an Aether Wisp (which builds from an Amplifying Tome and so on). To account for this, I started by going to the highest depth and working my way down, adding to the item anything that it built into. This meant that if I bought a Luden's Echo, I also bought a NLR and Aether Wisp and Amplifying Tome. I made sure to update the champions that used the entire item tree as well. 

After that it was just a matter of combining all the regions and getting the percentages. For the buy rate I took the the number of times it was bought and divided it by 10000 (games) * 10 (people in each game). This would give me the ratio of times it was bought per summoner (note that an item can be bought more than once by the same summoner which explains the reason why Amplifying Tome's buy rate is over 100%). The win rate is found by dividing the number of wins by the number of times it was bought. The most popular champions was found based on the number of times each champion bought the item. 
