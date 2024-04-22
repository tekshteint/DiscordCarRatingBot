# Discord Car Rating Bot
 A discord bot meant to be used to rate and compare car listings on Facebook Marketplace as well as Craigslist. 
 This bot is able to scrape FB and CL and then upload listings to a MongoDB. From there you have the following options for commands:
   * `$add`: The add command is used to add a car listing(s) to the database. This command takes a URL of a 1 to many cars not in the database.

   * `$rate`: The rate command is used to rate a car listing. It will rate it based on the average price of that model in the database. This command takes a URL of a car already in the database

   * `$avg`: The avg command is used to get the average rating of a car model. An example call would be `$avg brz` which will return the average price of BRZs in the database. 

   * `$tweak`: The tweak command is used to modify the details of a car listing in the database. Since there is no golden standard to listing cars, the model of a car could be stored as "MX-5 SUPER CLEAN LOW MILES 8000 OBO" instead of just MX-5. This command takes a URL of a car already in the database

   * `$return`: The return command is used to retrieve all information about a car from the database. This command takes a URL of a car already in the database

   * `$kbb`: The kbb command is used to interact with the Kelley Blue Book (KBB) service. It returns a GIF image of the result (currently broken and needs to be fixed, but works when not dockerized). This command takes a URL of a car already in the database


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

   * `wget https://github.com/themattman/mongodb-raspberrypi-docker/releases/download/r7.0.4-mongodb-raspberrypi-docker-unofficial/mongodb.ce.pi4.r7.0.4-mongodb-raspberrypi-docker-unofficial.tar.gz`
   
   * `sudo docker load --input mongodb.ce.pi4.r7.0.4-mongodb-raspberrypi-docker-unofficial.tar.gz`
   
   * Make sure to utilize the `docker-compose.rPi.yml` file for Pis specifically

   * `sudo docker-compose -f docker-compose.rPi.yml up -d`
  
   * `sudo docker compose up -d`

   * In MongoDB_Client.py, make sure to follow the directions there to connect to the database instance if you do run in a dockerized environment

   * I personally have it setup as a systemd service on my raspberry pi which allows for nightly reboots and the bot will always come back alive when the machine comes on.

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

