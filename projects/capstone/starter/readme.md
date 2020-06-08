# Casting Agency API

## Motivation

This API is my capstone project for Udacity's full stack web developer course. 

The API creates a simple mechanism for casting agencies to track actors, movies and castings. With it, a casting agency can:

1) Get from their database all actors, movies, and their castings 
2) Add actors, movies, and cast actors in movies 
3) Modify any pre-existing actor or movie information
4) Delete any record

An actor can be casted in many movies and movies can have many actors casted in it.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Local Database Setup

Create a database with Postgres running:
```bash
createdb castingagency
```

## Running the server locally

From within this project's directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python3 app.py
``` 

## API Reference

### Getting started

- Base URL: 
- Authentication: this application assumes 3 roles in the casting agency:
    - Casting Assistant: 
        - Can view actors and movies
        - JWT token: 
        ```
        eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3ODE2YmZjY2EzMDAxOTdkNTVlMyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2NDk0MzYsImV4cCI6MTU5MTczNTgzNiwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.yctWKSC4m2lBJKioR4BWBdOWicUxU6wZZD8dGIj99pJkgeYLJ9cyP6-mgojKByJZ1N6vY7wR77kZu76_RmV0DTVytnkfBt4XsS7FvTwXGq520649cQfTN_If0fzm0nTwO428TvtpUFWzT90XYfLszOzbHcLw86iNMR3vwrWXg72aIKb9PEt3VKW8engSadVnwvH0oysJsOZLZ-gQbLJV2wqE05nYFWhECk_zQ72fIFJ1KVqzJBL82aemjLiXjyj2joPCTHXfQ5CmA8O0mn9bJlAS8DCUYZXnxL48ToajKnnfq4tdw0eOA5bRZlPZQ9dFfAMxBKbnNVRUyWfnsyIX-w
      ```
    - Casting Director: Had all permissions of a casting assistant and a few more:
        - Can add or delete an actor or casting from the database. Can modify any actor and movie information
        - JWT token: 
        ```
        eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3OGI5MjI5ZGNlMDAxM2Q3OGVlZSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2NDk1MjEsImV4cCI6MTU5MTczNTkyMSwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZ3MiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDpjYXN0aW5ncyJdfQ.ADkAbby5iFnm13A9WaCWrLgtAN8K-yAydxrajkGqZX6HuIjgQWwFutVdwUxIgDRCblxnTY0kSONPiv1mumjVlKRVHTOOJzdFcBBYlvUt-XsXhpvbZQWgUxwfB6RGIexJnoiz_NOi9ftGRNmeiBF-LZ1YTOo_WViO-o4X_tzMdp8K_DmMeqPvyzbrc3dVr-E0w3AmXILJQqu2_akgj0feR51EzUCRy9XsQteltkSfQlZrCtQg1NYjwXCpIqzbm8rvbVXnLc95K_Vo4rJBNXVqjBukBQMckWw3wTEOz4Uff-pjnVegUq1BixzomPSAVv0mmTSEPxwWPnhBPbELUu6P8Q
      ``` 
    - Executive Producer: All permission of a casting director and a few more:
        - Can add or delete a movie from the database
        - JWT token:
        ```
      eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3OGRlYmZjY2EzMDAxOTdkNTY3ZiIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2NDk2MTYsImV4cCI6MTU5MTczNjAxNiwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZ3MiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6Y2FzdGluZ3MiLCJwb3N0Om1vdmllcyJdfQ.tzp_ID_YyJAw5T9vF7T9CLirvZ5YO_EHLBZmTMabl_3_ryo71gjnCVInNdo7kstN57NT5Xt8F7OLJl3Ad2w4UzC1IJLOJqxy9PhTMOhm8TDfSaOky91Q-2UHuv-xXDrqccU9rsiXF0CeFu0BhXfTt634HCtdoszLlNSwk3aGEWwDeo2I1Lyu9nuNg6MzTAYnOfA_KGjsySoeNcBFh4IFUtbMLUBoS6PoYSxiPzDy3OqvN_N4C074um83IuR8RuBsM9vJ0KpwmVmNGuhXo3fw8A7Mpezop7K5tPtHstZx1GUcNLzLUA834VYAO8JVd58vNEvP_xnWtAfR9X61UAvn8Q
      ```  

### Error handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The API can return these error types when requests fail:
- 400: bad request
- 404: resource not found
- 405: method not allowed
- 422: unprocessable
- 500: internal server error

Authorization errors will come with more detailed messages:
- 400: Permissions not included in JWT.
- 400: Unable to parse authentication token.
- 400: Unable to find the appropriate key.
- 401: Authorization header is expected.
- 401: Authorization header must start with "Bearer".
- 401: Token not found.
- 401: Authorization header must be bearer token.
- 401: Authorization malformed.
- 401: Token expired.
- 401: Incorrect claims. Please, check the audience and issuer.
- 403: Permission not found.

### Endpoints

#### ACTORS

##### GET /actors
- Fetches all actors, their movie castings and number of castings
- Sample request: `curl http://0.0.0.0:8080/actors -H "Authorization: Bearer <JWT_FROM_ANY_ROLE>"`
- Sample response: 
```
{
  "actors": [
    {
      "age": 21,
      "gender": "female",
      "id": 1,
      "movie_castings": [],
      "name": "Test actor 1",
      "num_movie_castings": 0
    },
    {
      "age": 21,
      "gender": "female",
      "id": 2,
      "movie_castings": [
        {
          "id": 3,
          "release_date": "Tue, 21 May 2019 21:30:00 GMT",
          "title": "Movie 3"
        }
      ],
      "name": "Test actor 2",
      "num_movie_castings": 1
    },
    {
      "age": 21,
      "gender": "female",
      "id": 3,
      "movie_castings": [
        {
          "id": 3,
          "release_date": "Tue, 21 May 2019 21:30:00 GMT",
          "title": "Movie 3"
        },
        {
          "id": 4,
          "release_date": "Tue, 21 May 2019 21:30:00 GMT",
          "title": "Movie 4"
        }
      ],
      "name": "Test actor 3",
      "num_movie_castings": 2
    },
    {
      "age": 21,
      "gender": "female",
      "id": 6,
      "movie_castings": [
        {
          "id": 2,
          "release_date": "Tue, 21 May 2019 21:30:00 GMT",
          "title": "Movie 2"
        }
      ],
      "name": "Test actor 6",
      "num_movie_castings": 1
    }
  ],
  "success": true 
}
``` 

##### GET /actors/{actor_id}
- Fetches specific actor by actor_id
- Sample request: `curl http://0.0.0.0:8080/actors/3 -H "Authorization: Bearer <JWT_FROM_ANY_ROLE>"`
- Sample response:
```
{
  "actor": {
    "age": 21,
    "gender": "female",
    "id": 3,
    "movie_castings": [
      {
        "id": 3,
        "release_date": "Tue, 21 May 2019 21:30:00 GMT",
        "title": "Movie 3"
      },
      {
        "id": 4,
        "release_date": "Tue, 21 May 2019 21:30:00 GMT",
        "title": "Movie 4"
      }
    ],
    "name": "Test actor 3",
    "num_movie_castings": 2
  },
  "success": true
}
```

##### POST /actors
- Adds a new actor to the database and returns the list of all actors, their castings and number of castings
- Sample request: `curl -X POST  http://0.0.0.0:8080/actors -H "Authorization: Bearer <JWT_DIRECTOR_OR_PRODUCER>" -H "Content-Type: application/json" -d '{"name": "Test actor 7", "age": 25, "gender": "male"}'`
- Sample response:
```
{
  "actors": [
    {
      "age": 21,
      "gender": "female",
      "id": 1,
      "movie_castings": [],
      "name": "Test actor 1",
      "num_movie_castings": 0
    },
    {
      "age": 21,
      "gender": "female",
      "id": 2,
      "movie_castings": [
        {
          "id": 3,
          "release_date": "Tue, 21 May 2019 21:30:00 GMT",
          "title": "Movie 3"
        }
      ],
      "name": "Test actor 2",
      "num_movie_castings": 1
    },
    {
      "age": 21,
      "gender": "female",
      "id": 3,
      "movie_castings": [
        {
          "id": 3,
          "release_date": "Tue, 21 May 2019 21:30:00 GMT",
          "title": "Movie 3"
        },
        {
          "id": 4,
          "release_date": "Tue, 21 May 2019 21:30:00 GMT",
          "title": "Movie 4"
        }
      ],
      "name": "Test actor 3",
      "num_movie_castings": 2
    },
    {
      "age": 21,
      "gender": "female",
      "id": 6,
      "movie_castings": [
        {
          "id": 2,
          "release_date": "Tue, 21 May 2019 21:30:00 GMT",
          "title": "Movie 2"
        }
      ],
      "name": "Test actor 6",
      "num_movie_castings": 1
    },
    {
      "age": 25,
      "gender": "male",
      "id": 7,
      "movie_castings": [],
      "name": "Test actor 7",
      "num_movie_castings": 0
    }
  ],
  "success": true
}
```

##### PATCH /actors/{actor_id}
- Modifies attributes from an actor in the database if they exist and returns the actor information
- Sample request: `curl -X POST  http://0.0.0.0:8080/actors/7 -H "Authorization: Bearer <JWT_DIRECTOR_OR_PRODUCER>" -H "Content-Type: application/json" -d '{"name": "Test modified actor", "age": 34, "gender": "female"}'`
- Sample response:
```
{
   "actor": {
     "age": 34,
     "gender": "female",
     "id": 7,
     "movie_castings": [],
     "name": "Test modified actor",
     "num_movie_castings": 0
   },
   "success": true
 }
```

##### DELETE /actors/{actor_id}
- Deletes the actor from the database if they exist
- Returns success value and actor_id of deleted actor.
- Sample request: `curl -X DELETE http://0.0.0.0:8080/actors/7 -H "Authorization: Bearer <JWT_DIRECTOR_OR_PRODUCER>`
- Sample response:
```
{
  "delete": "7",
  "success": true
}
```

#### MOVIES

##### GET /movies
- Fetches all movies, their actor castings and number of actors casted
- Sample request: `curl http://0.0.0.0:8080/movies -H "Authorization: Bearer <JWT_FROM_ANY_ROLE>"`
- Sample response: 
```
{
  "movies": [
    {
      "actors_casted": [
        {
          "age": 21,
          "gender": "female",
          "id": 6,
          "name": "Test actor 6"
        }
      ],
      "id": 2,
      "num_actors_casted": 1,
      "release_date": "Tue, 21 May 2019 21:30:00 GMT",
      "title": "Movie 2"
    },
    {
      "actors_casted": [
        {
          "age": 21,
          "gender": "female",
          "id": 2,
          "name": "Test actor 2"
        },
        {
          "age": 21,
          "gender": "female",
          "id": 3,
          "name": "Test actor 3"
        }
      ],
      "id": 3,
      "num_actors_casted": 2,
      "release_date": "Tue, 21 May 2019 21:30:00 GMT",
      "title": "Movie 3"
    },
    {
      "actors_casted": [
        {
          "age": 21,
          "gender": "female",
          "id": 3,
          "name": "Test actor 3"
        }
      ],
      "id": 4,
      "num_actors_casted": 1,
      "release_date": "Tue, 21 May 2019 21:30:00 GMT",
      "title": "Movie 4"
    },
    {
      "actors_casted": [],
      "id": 5,
      "num_actors_casted": 0,
      "release_date": "Tue, 21 May 2019 21:30:00 GMT",
      "title": "Movie 5"
    }
  ],
  "success": true
}
``` 

##### GET /movies/{movie_id}
- Fetches specific movie by movie_id
- Sample request: `curl http://0.0.0.0:8080/movies/3 -H "Authorization: Bearer <JWT_FROM_ANY_ROLE>"`
- Sample response:
```
{
  "movie": {
    "actors_casted": [
      {
        "age": 21,
        "gender": "female",
        "id": 2,
        "name": "Test actor 2"
      },
      {
        "age": 21,
        "gender": "female",
        "id": 3,
        "name": "Test actor 3"
      }
    ],
    "id": 3,
    "num_actors_casted": 2,
    "release_date": "Tue, 21 May 2019 21:30:00 GMT",
    "title": "Movie 3"
  },
  "success": true
}
```

##### POST /movies
- Adds a new movie to the database and returns the list of all movies, their castings and number of castings
- Sample request: `curl -X POST  http://0.0.0.0:8080/movies -H "Authorization: Bearer <JWT_PRODUCER>" -H "Content-Type: application/json" -d '{"title": "Movie 7", "release_date": "2020-07-21T21:30:00.000Z"}'`
- Sample response:
```
{
  "movies": [
    {
      "actors_casted": [
        {
          "age": 21,
          "gender": "female",
          "id": 6,
          "name": "Test actor 6"
        }
      ],
      "id": 2,
      "num_actors_casted": 1,
      "release_date": "Tue, 21 May 2019 21:30:00 GMT",
      "title": "Movie 2"
    },
    {
      "actors_casted": [
        {
          "age": 21,
          "gender": "female",
          "id": 2,
          "name": "Test actor 2"
        },
        {
          "age": 21,
          "gender": "female",
          "id": 3,
          "name": "Test actor 3"
        }
      ],
      "id": 3,
      "num_actors_casted": 2,
      "release_date": "Tue, 21 May 2019 21:30:00 GMT",
      "title": "Movie 3"
    },
    {
      "actors_casted": [
        {
          "age": 21,
          "gender": "female",
          "id": 3,
          "name": "Test actor 3"
        }
      ],
      "id": 4,
      "num_actors_casted": 1,
      "release_date": "Tue, 21 May 2019 21:30:00 GMT",
      "title": "Movie 4"
    },
    {
      "actors_casted": [],
      "id": 5,
      "num_actors_casted": 0,
      "release_date": "Tue, 21 May 2019 21:30:00 GMT",
      "title": "Movie 5"
    },
    {
      "actors_casted": [],
      "id": 6,
      "num_actors_casted": 0,
      "release_date": "Tue, 21 Jul 2020 21:30:00 GMT",
      "title": "Movie 7"
    }
  ],
  "success": true
}
```

##### PATCH /movies/{movie_id}
- Modifies attributes from a movie in the database if it exists and returns the movie information
- Sample request: `curl -X POST  http://0.0.0.0:8080/movies/6 -H "Authorization: Bearer <JWT_DIRECTOR_OR_PRODUCER>" -H "Content-Type: application/json" -d '{"title": "Test modified movie", "release_date: "2020-05-21T21:30:00.000Z"}'`
- Sample response:
```
{
  "movie": {
    "actors_casted": [],
    "id": 6,
    "num_actors_casted": 0,
    "release_date": "Thu, 21 May 2020 21:30:00 GMT",
    "title": "Test modified movie"
  },
  "success": true
}
```

##### DELETE /movies/{movie_id}
- Deletes the movie from the database if it exists
- Returns success value and movie_id of deleted movie
- Sample request: `curl -X DELETE http://0.0.0.0:8080/movies/6 -H "Authorization: Bearer <JWT_PRODUCER>`
- Sample response:
```
{
  "delete": "6",
  "success": true
}
```

#### POST /movies/{movie_id}/actors
- Casts an actor to the movie with movie_id if both actor and movie exist
- Return success value and actor castings for the movie
- Sample request: `curl -X POST  http://0.0.0.0:8080/movies/3/actors -H "Authorization: Bearer <JWT_DIRECTOR_OR_PRODUCER>" -H "Content-Type: application/json" -d '{"actor_id": 3}'`
- Sample response:
```
{
  "movie": {
    "actors_casted": [
      {
        "age": 21,
        "gender": "female",
        "id": 2,
        "name": "Test actor 2"
      },
      {
        "age": 21,
        "gender": "female",
        "id": 3,
        "name": "Test actor 3"
      }
    ],
    "id": 3,
    "num_actors_casted": 2,
    "release_date": "Tue, 21 May 2019 21:30:00 GMT",
    "title": "Movie 3"
  },
  "success": true
}
```

#### DELETE /movies/{movie_id}/actors
- Removes an actos from the movie with movie_id if both actor and movie exist
- Return success value and actor castings for the movie
- Sample request: `curl -X DELETE  http://0.0.0.0:8080/movies/3/actors -H "Authorization: Bearer <JWT_DIRECTOR_OR_PRODUCER>" -H "Content-Type: application/json" -d '{"actor_id": 3}'`
- Sample response:
```
{
  "movie": {
    "actors_casted": [
      {
        "age": 21,
        "gender": "female",
        "id": 2,
        "name": "Test actor 2"
      }
    ],
    "id": 3,
    "num_actors_casted": 1,
    "release_date": "Tue, 21 May 2019 21:30:00 GMT",
    "title": "Movie 3"
  },
  "success": true
}
```

## Testing
To run the tests, run
```bash
dropdb castingagency_test && createdb castingagency_test
psql castingagency_test < castingagency.psql
python test_app.py
```