# Configuration
Installation of the dependencies:

```
pip install -r requirements.txt
```

Environment variable OMDB_API_TOKEN should be set to be able to get additional movies data from OMDB.

# Running project

To run project locally you need to migrate database first then run the server

```
./manage.py migrate
./manage.py runserver
```

# Running tests

To run Tests exectue following command:

```
./manage.py test
```

# Types

Both types in this project have implemented `Nodez` interface which means they will have lists of edges that includes node.

## Movie

Movie type has available following fields that can be included in queries:

* id: stringified ID of the object
* title: String
* year: Int
* rated: String
* released: Date
* runtime: String
* genre: String
* director: String
* writer: String
* actors: String
* plot: String
* language: String
* country: String
* awards: String
* metascore: Int
* imdbRating: Float
* commentSet: Set of edges/nodes of all CommentTypes refferenced to this movie

Allows filtering by:
1. Title
    * exact value - `title: "Test"`
    * string contains - `title_Icontains: "es"`
    * string starts with - `title_Istartswith: "Te"`
2. Genre
    * exact value - `genre: "Test"`
    * string contains - `genre_Icontains: "es"`
3. Year
    * exact value - `year: 2000`
    * lower than - `year_Lt: 2005`
    * greater than - `year_Gt: 1970`
    
## Comment

Comment type has available following fields that can be included in queries

* id: stringified ID of the object
* body: String
* movie: MovieType

# Endpoint `/graphql`

One endpoint is available

## Queries

### allMovies

It would return a list of all movies

```graphql
query {
  allMovies {
    edges {
      node {
        id
        title
      }
    }
  }
}
```

It has some filters, which are defined in MovieType.
For example we can filter all movies that were created before year 2000:
```graphql
query {
  allMovies(year_Lt: 2000) {
    edges {
      node {
        id
        title
        year
      }
    }
  }
}
```

Example including commentSet, for all movies from year 1970.
```graphql
query {
  allMovies(year: 1970) {
    edges {
      node {
        id
        title
        year
        commentSet {
          edges {
            node {
              id
              body
            }
          }
        }
      }
    }
  }
}
```


### movie

Movie query can get us single Movie object by either id or title (if title is uniqie)

```graphql
query {
  movie(id: "TW92aWVUeXBlOjI=") {
    id
    title
    year
  }
}
```

### allComments

Gets list of all comments

```graphql
{
  allComments {
    id
    body
    movie {
      id
      title
    }
  }
}
```

### comment

Gets single comment based on given ID

```graphql
{
  comment(id: "Q29tbWVudFR5cGU6MQ==") {
    id
    body
    movie {
      id
      title
      year
    }
  }
}
```

## Mutations

Mutations are used to create/update objects

### createMovie

This mutation creates new movie object

```graphql
mutation {
  createMovie(title: "Test", year: 2010) {
    movie {
      id
      title
      year
    }
  }
}
```

### createComment

This mutation allows to create new comment objects, movie needs to be created first.

```graphql
mutation {
  createComment(body: "Test comment", movieId: "TW92aWVUeXBlOjY=") {
    id
    body
    movie {
      id
      title
      year
    }
  }
}
```