# Discord Car Rating Bot
 A discord bot meant to be used to rate and compare car listings on Facebook Marketplace as well as Craigslist. 
 Currently in extreme beta, this bot is able to scrape FB and CL and then upload listings to a MongoDB. 


### Docker!
 * For ease of use and keeping alive, this bot is able to be containerized
 * In your host machine, first create the `config.json` file as mentioned below in the /Bot directory, and it will be transferred over to your container.
 * To run, just use the command `sudo docker-compose up --build` and let docker do the rest
 * In mongosh, if you'd like to view the information stored in your local DB, you can do the following:
      ```$ mongosh
      test> show dbs #to verify the database has been successfully created
      test> use CarRatingBotDB
      CarRatingBotDB> for(var i = 0; i < collections.length; i++){
         print('Collection: ' + collections[i]);
         db.getCollection(collections[i]).find().forEach(printjson);
      }
#### A speical note for Raspberry Pis
 * I tested this on a Pi 4 running Ubuntu server 64 bit, and there's a few extra steps needed to be taken. 
 * Big thanks and credit where credit's due, this was made possible thanks to this [repo](https://github.com/themattman/mongodb-raspberrypi-docker)
 * **Steps**
   
   * [Install Docker](https://dev.to/elalemanyo/how-to-install-docker-and-docker-compose-on-raspberry-pi-1mo)
  
   * `cd /path/to/repo`
  
   * Install the required modules `pip install -r Bot/requirements.txt`

   * `wget https://github.com/themattman/mongodb-raspberrypi-docker/releases/download/r7.0.4-mongodb-raspberrypi-docker-unofficial/mongodb.ce.pi4.r7.0.4-mongodb-raspberrypi-docker-unofficial.tar.gz`
   
   * `sudo docker load --input mongodb.ce.pi4.r7.0.4-mongodb-raspberrypi-docker-unofficial.tar.gz`
   
   * Make sure to utilize the `docker-compose.rPi.yml` file for Pis specifically

   * `sudo docker-compose -f docker-compose.rPi.yml up -d`
  
   * `* sudo docker compose up -d`



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
If you choose to run the bot locally, you will need to change the following:
 * line 7 in MongoDB_Client.py should be `localhost` not `mongodb`
 * line 13 in createDB.py should be `localhost` not `mongodb`
