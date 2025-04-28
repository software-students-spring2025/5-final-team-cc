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

## Configuration and Run Instructions

### Prerequisites
Make sure both **[Docker](https://www.docker.com/products/docker-desktop)** and **[Docker Compose](https://docs.docker.com/compose/install/)** are installed.

### Setup
1. Clone the repository:
```bash
git clone git@github.com:software-students-spring2025/5-final-team-cc.git
```
2. Create a .env file (literally named: .env) in the root directory that contains your MongoDB URI. An example URI:
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





