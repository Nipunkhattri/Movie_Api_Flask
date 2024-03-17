# Movie Curd Api Using Flask

1. Create Virtual environment

```sh
python -m venv venv
```

2. Activate the environment

```sh
.\venv\scripts\activate.bat
```

3. Install packages

```sh
pip install -r requirements.txt
```

4. Flask Migrate

```sh
flask db migrate
```

5. Flask Upgarde

```sh
flask db upgrade
```

6. Run the application
```sh
python main.py
```

## API Documentation

### User Route

#### User Registration
Route

```http
POST /auth/register
```

Request Body
```json
{
    "username":"Test",
    "email":"test@gmail.com",
    "password":"Test1234"
}
```

Response
```json
{
    "message": "User registered successfully"
}
```

#### User Login
Route

```http
POST /auth/login
```

Request Body
```json
{
    "email":"test@gmail.com",
    "password":"12345"
}
```

Response
```json
{
    "access_token": "<JWT_TOKEN>"
}
```

### Movies Route

#### Create new movie

Route

```http
POST /movie
```

Request Header
| Key          | Value              |
---------------|---------------------
|Authorization | Bearer <JWT_TOKEN> |

Request Body
```json
{
    "avg_rating": 7.5,
    "description": "This is Test Movie",
    "director": "Smiles Unlimited",
    "genre": "comedy",
    "release_date": "2019-12-25",
    "ticket_price": 2300.0,
    "title": "Test Movie"
}
```

Response
```json
{
    "message": "Movie created successfully"
}
```


#### Get movies with page, filter and sorting parameters

Route

```http
GET /movie
```
Request Header
| Key          | Value              |
---------------|---------------------
|Authorization | Bearer <JWT_TOKEN> |

Route Parameter
| Key          | Value                                       |
---------------|----------------------------------------------
| page         | page number of the result to be returned    |
| sort_by      | sorting criteria (release_date , ticket_price)    |
| filter_by    | filter criteria  (genere, director)   |
| filter_value | the actual value of the filter              |
| order_by     | the sorting order - asc or desc             |
| movies_per_page | the number of result to be displayed per page|


Example:
```http
GET /movie?sort_by=ticket_price&filter_by=genre&filter_value=action&order_by=asc
```

Response
```json
[
    {
        "avg_rating": 7.5,
        "description": "This is movie 2",
        "director": "Smiles Unlimited",
        "genre": "action",
        "release_date": "2019-12-25",
        "ticket_price": 2000.0,
        "title": "Movie 2"
    },
    {
        "avg_rating": 7.5,
        "description": "This is movie 3",
        "director": "Smiles Unlimited",
        "genre": "action",
        "release_date": "2019-12-25",
        "ticket_price": 2000.0,
        "title": "Movie 3"
    }
]
```

#### Get movies by ID
Route

```http
GET /movie/<movie_id:int>
```
Route Parameter
| Key          | Value              |
---------------|---------------------
|Movie ID      | ID of the movie    |

Request Header
| Key          | Value              |
---------------|---------------------
|Authorization | Bearer <JWT_TOKEN> |

Example
```http
GET /movie/4
```

Response
```json
{
    "avg_rating": 7.5,
    "description": "This is Test Movie",
    "director": "Smiles Unlimited",
    "genre": "comedy",
    "release_date": "2019-12-25",
    "ticket_price": 2300.0,
    "title": "Test Movie"
}
```


#### Update the existing movie
Route

```http
PUT /movie/<movie_id:int>
```
Route Parameter
| Key          | Value              |
---------------|---------------------
|Movie ID      | ID of the movie    |

Request Header
| Key          | Value              |
---------------|---------------------
|Authorization | Bearer <JWT_TOKEN> |

Request Body
```json
{
    "title":"This is Updated Test"
}
```

Response
```json
{
    "message": "Movie updated successfully"
}
```

#### Deleting a movie
Route

```http
DELETE /movie/<movie_id:int>
```
Route Parameter
| Key          | Value              |
---------------|---------------------
|Movie ID      | ID of the movie    |

Request Header
| Key          | Value              |
---------------|---------------------
|Authorization | Bearer <JWT_TOKEN> |


Response
```json
{
    "message": "Movie deleted successfully"
}
```


#### Search movie

Route

```http
GET /movie/search
```

Route Parameter
| Key          | Value                  |
---------------|------------------------
| search_value | the actual seach value |

Example:
```http
GET /movie/Search?query=Test Movie
```

Response
```json
[
    {
        "title": "This is Updated Test",
        "description": "This is Test Movie",
        "director": "Smiles Unlimited",
        "avg_rating": "7.5"
    }
]
```
