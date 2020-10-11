# CAPSTONE Project

## Casting Agency

The objective is to start from scratch with the proposed idea of a Casting Agency with an improvement on the idea. In this project, the movies will have one or many roles, and for each role the agency can cast one or many actors. It will be possible to make queries on actors, movies, and realize search.

## Project Structure

For this Capstone project, a Full Stack app is proposed, with the backend and tokens to complete test the API Endpoints.

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## About the Stack

### Backend

The `./backend` directory contains a full server with the following dependencies:

1. Flask server
2. SQLAlchemy as ORM database management with Postgres
3. Authentification with Auth0
4. Deployment in Heroku

[View the README.md within ./backend for more details.](./backend/README.md)

AWS Container deployment is not used because of cost.

### Frontend

The `./frontend` directory contains a complete express frontend to consume the data from the Flask server, developed with Webpack.

[View the README.md within ./frontend for more details.](./frontend/README.md)


## Development Strategy

The [backed](./backend/) is developed following TDD process as follows:

1. First the test will be written using `unittest` for the API Endpoints without Authorization/Authentification
2. The Front End will be developed to be ready for the server
3. Then the Flask server will be developed and tested. Unit Test and Front End visual test
4. When this first cycle is finished (all test pass), the test will be completed with Authorization/Authentification
5. Then the server will be completed and re-tested
6. The Front End will include the Auth0 sign in with default test accounts
7. Then the complete the server will be deployed in Heroky


