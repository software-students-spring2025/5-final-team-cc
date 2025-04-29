![Game Log CI/CD](https://github.com/software-students-spring2025/5-final-team-cc/actions/workflows/web-app-deploy.yml/badge.svg)

# [GameLog](http://206.189.228.116/)

## Overview

GameLog is a web application designed to give users a place to post reviews and descriptions of any video game they've played, and also to find new games posted by other users to try! GameLog also provides users with their very own Tamagotchi-esque pet that can be taken care of by continuously making posts. Try out GameLog now by clicking [here](http://206.189.228.116/)!

## Team Members
- [James Hou](https://github.com/James-Hou22)
- [John Ma](https://github.com/j4ma)
- [Andrew Park](https://github.com/Toudles)
- [Larry Yang](https://github.com/larryyang04)

## Implementation

GameLog is comprised of two subsystems: one for the web application itself, and one for MongoDB. Our web application is containerized, and you can find its images [here](https://hub.docker.com/r/larryyang04/swe-project5-team-cc-web-app). For our MongoDB database, we used MongoDB Atlas, a cloud database service.

## Running GameLog Locally

### Prerequisites
Make sure both **[Docker](https://www.docker.com/products/docker-desktop)** and **[Docker Compose](https://docs.docker.com/compose/install/)** are installed.

### Setup
1. Clone the repository:
```bash
git clone git@github.com:software-students-spring2025/5-final-team-cc.git
```
2. Set up your own instance of a MongoDB database—whether using a cloud service or locally on your machine—with the following schema:

```bash
database_name: (Database)
    ├── user (Collection)
    │     ├── _id: ObjectId
    │     ├── username: String
    │     ├── password: String
    │     ├── last_post_time: Date
    ├── post (Collection)
    │     ├── _id: ObjectId
    │     ├── user_id: ObjectId
    │     ├── game: String
    │     ├── description: String
    │     ├── rating: Int32
    │     ├── likes: Int32
    │     ├── dislikes: Int32
    │     ├── hours_played: Double
    │     ├── recommend: Boolean
    ├── reactions (Collection)
          ├── _id: ObjectId
          ├── user_id: ObjectId
          ├── post_id: ObjectId
          ├── reaction_type: String
          ├── timestamp: Date
```
3. In the root directory, create a ".env" file and include your newly created URI; your ".env" file should now look something like the following:

```bash
MONGO_URI=mongodb+srv://username:password@cluster.xxxxx.mongodb.net/database_name
```

### Running the System
1. Ensure you are in the root directory, and run:
```bash
docker-compose up
```

2. Once the containers are up and running, open your browser and navigate to [http://localhost:5001](http://localhost:5001).


### Stopping the System
1. Run:
```bash
docker-compose down
```

### Running Unit Tests

If you wish to also run unit tests locally for the web application subsystem:

1. Set up an additional instance of a MongoDB database with the same schema as shown above (with a different database name, say "database_name_test").

2. For testing purposes, we need to pre-populate the "user" and "post" collections. With your newly created URI for testing, run the following command:
```bash
mongosh "mongodb+srv://username:password@cluster.xxxxx.mongodb.net/database_name_test"
```

3. Also, make sure to include this testing URI in your ".env" file, which should now look like:
```bash
MONGO_URI=mongodb+srv://username:password@cluster.xxxxx.mongodb.net/database_name
TEST_URI=mongodb+srv://username:password@cluster.xxxxx.mongodb.net/database_name_test
```

4. Then, run the following ```mongosh``` commands:
```bash
db.user.insertOne({
  _id: ObjectId("681057d55e6a93269c8c9155"),
  username: "johndoe",
  password: "secret",
  last_post_time: new Date(1745907886584)
});
```
```bash
db.user.insertOne({
  _id: ObjectId("68105df863a89476fe07f296"),
  username: "test_happiness",
  password: "no_delete",
  last_post_time: new Date(1745303088653)
});
```
```bash
db.post.insertOne({
  _id: ObjectId("68105b3a4404847de9b361cf"),
  user_id: ObjectId("681057d55e6a93269c8c9155"),
  game: "Test Post for Reactions",
  rating: 10,
  description: "DO NOT DELETE. This is intended to test reactions.",
  hours_played: 0.0,
  recommend: true,
  likes: 1,
  dislikes: 0
});
```

5. Exit ```mongosh``` by typing ```exit```.
6. Ensure you are in the ```web-app``` directory, and run the following commands:
```bash
pip install pipenv
```
```bash
pipenv install
```
```bash
pipenv shell
```
```bash
pytest
```






