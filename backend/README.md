# Casting Agency Backend

Backend for the Castin Agency App, which allow to manage the casting of actors for roles in different movies.

* [Getting Started](#getting-started)
* [API Reference](#api-reference) 
* [Heroku Deployment](#heroku) 


## Getting Started <a name="getting-started"></a>

### Installing Dependencies

#### Python

This project was developed using Python version 3.8.3. Please update your Python stack if you are using an older version

#### Virtual Environment

Please create a virtual environment in the `\backend\` directory with the command `python -m venv  path\to\env\`

#### PIP Dependencies

Once virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export (or set) FLASK_APP=flaskapp
flask run
```

### Testing
To run the tests, run


## API Reference <a name="api-reference"></a>

The backend is a RESTful JSON API. The sections below explain the model and how to use the different API endpoints. 

When testin, the API is not deployed and can only be accessed through the localhost:

```
http://localhost:5000
```

[View the Heroky Deployment for more information of the deployed version](#heroku)

### Data Model


The backend handles three types of objects: **Actors**, **Moview**, **Roles**.

**Actors**  
which is the following JSON object `ActorStruct`:
> ```
>     {
>      "name": String,
>      "gender": String,
>      "age":  Integer,
>      "photoUrl": String
>     }
>```

Where:

| Attribute | Type          | Description                                                          |
| :---      | :-----------: | -------------------------------------------------------------------: |
| name      | String        |  name of the actress/actor, with maximum 150 Characters. Cannot be null |
| gender    | String        |  gender: Female , Male |
| age       | Integer       |  age of the actor |
| photoUrl  | String        |  URL to the photo of the actress/actor. Default value is `empty` string |

**Roles**  
which is the following JSON object `RoleStruct`:
> ```
>     {
>      "name": String,
>      "type":  String,
>      "actors": [ActorStruct],
>      "movie": Integer,
>     }
>```

Where:

| Attribute | Type          | Description                                                          |
| :---      | :-----------: | -------------------------------------------------------------------: |
| name      | String        |  Role name in the movie, with maximum 150 Characters. Cannot be null |
| types     | String        |  Type of role: Lead Actor, Secondary Actor, extra |
| movie     | Integer       |  ID of the movie |
| actors    | Array[String] |  ID of actors casted for the role |


**Movies**  
which is the following JSON object `MovieStruct`:
> ```
>     {
>      "name": String,
>      "photoUrl": String,
>      "release": Date,
>      "genres":  [String],
>      "roles": [RoleStruct],
>     }
>```

Where:

| Attribute | Type          | Description                                                     |
| :---      | :-----------: | --------------------------------------------------------------: |
| name      | String        |  movie name with maximum 150 Characters. Cannot be null         |
| photoUrl  | String        |  URL to the photo of the movie. Default value is `empty` string |
| release   | Date          |  Release date of the movie as a Date timestamp                  |
| genres    | Array[String] |  genres related to the movie, an array of maximum 5 genres      |
| roles     | Array[Integer]|  ID of Roles to cast for the movie. Linked to `Roles` table     |


### Responses

When the backend return a success response, it is formatted as follows:

```json
{
    "success": true,
    "data": ResponseStruct,
}
```

where `ResponseStruct` depends on the endpoint, it can be a single object, or a array of objects. 

Unsuccessful requests follows the `RFC7807` standard, it is formatted as follows:

```json
{
    "success": false,
    "status": Integer,
    "type": URI,
    "title": String,
    "detail": String,
    "instance": URI
}
```
Where `instance` is not used and always equal to `about:blank` 

### Status Codes

The backend returns the following status codes:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 401 | `UNAUTHORIZED` |
| 403 | `FORBIDDEN`|
| 404 | `NOT FOUND` |
| 422 | `UNPROCESSABLE` |
| 500 | `INTERNAL SERVER ERROR` |
 
  
### Open Endpoints

Open endpoints require no Authentication.  
They are not open Endpoints for this app

### Protected Endpoints

Protected endpoints require a JWT token with the correct claims

* [List Movies](#movies)                 : `GET /movies?page=`
* [List Movie's actors](#movies-actors)  : `GET /movies/<int:id>/actors`
* [List Actors](#actors)                 : `GET /actors?page=`
* [Search Movies](#movies-search)        : `POST /movies/search`
* [Search Actors](#actors-search)        : `POST /actors/search`
* [Create Movie](#movie-create)          : `POST /movies`
* [Create Actor](#actor-create)          : `POST /actors`
* [Create Role](#role-create)            : `POST /roles`
* [Read Movie](#movie-read)              : `GET /movies/<int:id>`
* [Read Actor](#actor-read)              : `GET /actors/<int:id>`
* [Update Movie](#movie-update)          : `PATCH /movies/<int:id>`
* [Update Actor](#actor-update)          : `PATCH /actors/<int:id>`
* [Update Role](#role-update)            : `PATCH /roles/<int:id>`
* [Delete Movie](#movie-delete)          : `DELETE /movies/<int:id>`
* [Delete Role](#actor-delete)           : `DELETE /actors/<int:id>`

### List Movies <a name="movies"></a>  
Fetches an array of movies with pagination

***URL*** : `/movies?page=`

***Method*** : `GET`

***Auth required*** : Yes, with `get:movies` claim

***Data constraints***: No data required in the body of the request

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "movies": [MovieStruct],   
    "total": 30,
    "count": 10
}
```

### List Movie's actors <a name="movies-actors"></a>
Fetches an array of actors for the movie

***URL*** : `/movies/<int:id>/actors`

***Method*** : `GET`

***Auth required*** : Yes, with `get:movies` and `get:actors` claim

***Data constraints***: No data required in the body of the request

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "actors": [ActorStruct],
    "movie": MovieStruct
}
```


### List Actors <a name="actors"></a>
Fetches an array of actors with pagination

***URL*** : `/actors?page=`

***Method*** : `GET`

***Auth required*** : Yes, with `get:actors` claim

***Data constraints***: No data required in the body of the request

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "actors": [ActorStruct],   
    "total": 30,
    "count": 10
}
```


### Search Movies <a name="movies-search"></a>
Search for movies and respond with an array of movies validating the search terms

***URL*** : `/movies/search`

***Method*** : `POST`

***Auth required*** : Yes, with `get:movies` claim

***Data constraints***: No data required in the body of the request

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "movies": [MovieStruct]
}
```

### Search Actors <a name="actors-search"></a>
Search actors by name, age or gender and return an array of actors validating the search

***URL*** : `/actors/search`

***Method*** : `POST`

***Auth required*** : Yes, with `get:actors` claim

***Data constraints***: No data required in the body of the request

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "actors": [ActorStruct]
}
```

### Create Movie <a name="movie-create"></a>
Create a movie in the database

***URL*** : `/movies`

***Method*** : `POST`

***Auth required*** : Yes, with `post:movies` claim

***Data constraints***: Minimum required data to create a movie
```json
{
    "name": String,
    "release": Date,
    "genres": [String]
}
```

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "movie": MovieStruct,   
    "id": Integer
}
```

***Unsucess Condition***: 
1. Unauthorized
2. If body of request not well formated or data missing
3. Internal server error


### Create Actor <a name="actor-create"></a>
Create an actress/actor in the database

***URL*** : `/actors`

***Method*** : `POST`

***Auth required*** : Yes, with `post:actors` claim

***Data constraints***: Minimum required data to create an actress/actor
```json
{
    "name": String,
    "gender": String,
    "age": Integer
}
```

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "actor": ActorStruct,   
    "id": Integer
}
```

***Unsucess Condition***: 
1. Unauthorized
2. If body of request not well formated or data missing
3. Internal server error

### Create Role <a name="role-create"></a>
Create a role for a movie in the database

***URL*** : `/roles`

***Method*** : `POST`

***Auth required*** : Yes, with `post:roles` claim

***Data constraints***: Minimum required data to create a Role
```json
{
    "name": String,
    "type": String,
    "movie": Integer
}
```

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "role": RoleStruct,
    "id": Integer
}
```

***Unsucess Condition***: 
1. Unauthorized
2. If body of request not well formated or data missing
3. Internal server error

### Read Movie <a name="movie-read"></a>
Read a movie from the database

***URL*** : `/movies/<int:id>`

***Method*** : `GET`

***Auth required*** : Yes, with `get:movies` claim

***Data constraints***: No data required in the body of the request

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "movie": MovieStruct,   
    "id": Integer
}
```

***Unsucess Condition***: 
1. Unauthorized
2. Data with `id` not found
3. Internal server error


### Read Actor <a name="actor-read"></a>
Read an actress/actor from the database

***URL*** : `/actors/<int:id>`

***Method*** : `GET`

***Auth required*** : Yes, with `get:actors` claim

***Data constraints***: No data required in the body of the request

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "movie": ActorStruct,   
    "id": Integer
}
```

***Unsucess Condition***: 
1. Unauthorized
2. Data with `id` not found
3. Internal server error


### Update Movie <a name="movie-update"></a>
Create a movie in the database

***URL*** : `/movies/<int:id>`

***Method*** : `PATCH`

***Auth required*** : Yes, with `patch:movies` claim

***Data constraints***: At least one of the following data is necessary
```json
{
    "name": String,
    "release": Date,
    "genres": [String]
}
```

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "movie": MovieStruct,   
    "id": Integer
}
```

***Unsucess Condition***: 
1. Unauthorized
2. If body of request not well formated or data missing
3. Internal server error


### Update Actor <a name="actor-update"></a>
Create an actress/actor in the database

***URL*** : `/actors/<int:id>`

***Method*** : `PATCH`

***Auth required*** : Yes, with `patch:actors` claim

***Data constraints***: At least one of the following data is necessary
```json
{
    "name": String,
    "gender": String,
    "age": Integer
}
```

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "actor": ActorStruct,   
    "id": Integer
}
```

***Unsucess Condition***: 
1. Unauthorized
2. If body of request not well formated or data missing
3. Internal server error

### Update Role <a name="role-update"></a>
Create a role for a movie in the database

***URL*** : `/roles/<int:id>`

***Method*** : `PATCH`

***Auth required*** : Yes, with `patch:roles` claim

***Data constraints***: At least one of the following data is necessary
```json
{
    "name": String,
    "type": String,
    "movie": Integer,
    "actor": Integer
}
```

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "role": RoleStruct,
    "id": Integer
}
```

***Unsucess Condition***: 
1. Unauthorized
2. If body of request not well formated or data missing
3. Internal server error

### Delete Movie <a name="movie-delete"></a>
Read a movie from the database

***URL*** : `/movies/<int:id>`

***Method*** : `DELETE`

***Auth required*** : Yes, with `delete:movies` claim

***Data constraints***: No data required in the body of the request

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "movie": MovieStruct,   
    "id": Integer
}
```

***Unsucess Condition***: 
1. Unauthorized
2. Data with `id` not found
3. Internal server error


### Delete Actor <a name="actor-delete"></a>
Read an actress/actor from the database

***URL*** : `/actors/<int:id>`

***Method*** : `DELETE`

***Auth required*** : Yes, with `delete:actors` claim

***Data constraints***: No data required in the body of the request

***Success Response Code*** : `200`

***Success Response Content Example***

The `ResponseStruct` for this endpoint is composed as follows:
```json
{
    "actor": ActorStruct,   
    "id": Integer
}
```

***Unsucess Condition***: 
1. Unauthorized
2. Data with `id` not found
3. Internal server error

## Heroku Deployment <a name="heroku"></a>
