# Discord Car Rating Bot
 A discord bot meant to be used to rate and compare car listings on Facebook Marketplace as well as Craigslist. 
 Currently in extreme beta, this bot is able to scrape FB and CL and then upload listings to a MongoDB. 
 
 **What to expect**
  - I'm looking to add searching through queries, rating listings in comparison to what's been stored, and comparing to KBB's pricing
  - I'd like to make the reliablity of the model names higher as currently it works, but what's stopping someone from listing a Mazda MX-5 as a Miata? Trims aren't implemented yet so a BMW M2 is basically the same as a BMW M2 Competition in the database's eyes.
 - While the scraping works off Facebook, its not as elegant/clean of a solution as I'd like. This needs to be reworked but Facebook makes this a challenge so if it isn't broken yet its at the bottom of the to-do list.
 - I'm also looking for a better name and a profile photo for the bot


**Final Note**
Make sure to get your own Bot Token from Discord's developer portal if you'd like to tinker/contribute, then in a config.json file, add a single object called token, with your own token as the value.
 ```
 {
    "token": "YOUR-TOKEN-HERE"
 }
 ```
