# Flask blog starter project

Blog application built with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [SQLAlchemy](https://www.sqlalchemy.org/).

## Get started

Start by setting up your development environment. First, make sure that you have _Python 3.7.1_ or later available in your terminal. The easiest way to manage multiple versions of _Python_ is to use [pyenv](https://github.com/pyenv/pyenv).

Next, in your project root, install the Python dependencies by executing:

```
make dev_install
```

then run the application by executing:

```
make run
```

now you can access your application by navigating to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

## Linting

To lint your Python code using _flake8_ run:

```
make lint
```

## Testing

Run the automated tests by executing:

```
make test
```

## GraphQL

This starter features a GraphQL API built with [graphene](https://github.com/graphql-python/graphene). To access the GraphiQL of your running server navigate to [http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql) in your browser.

### Create a new post

To create a new post via the GraphQL API execute the following mutation in GraphiQL:

```
mutation {
  createPost (input: {
    title: "Test Post"
    content: "Test content"
    tags: "foo, bar"
  }) {
    __typename
    ... on CreatePostSuccess {
      post {
        id
        title
        content
        createdAt
        updatedAt
        tags {
          edges {
            node {
              id
              name
            }
          }
        }
      }
    }
  }
}
```

### Edit an existing post

To edit an existing post via the GraphQL API execute the following mutation in GraphiQL:

```
mutation {
  editPost (input: {
    postId: 1
    title: "New Post Title"
    content: "Something else"
    tags: "foo"
  }) {
    __typename
    ... on EditPostSuccess {
      post {
        id
        title
        content
        createdAt
        updatedAt
        tags {
          edges {
            node {
              id
              name
            }
          }
        }
      }
    }
  }
}
```
### Delete a  post

To delete a post via the GraphQL API execute the following mutation in GraphiQL:

```
mutation {
  deletePost (input: {
    postId: 1
  }) {
    __typename
    ... on DeletePostSuccess {
      post {
        id
      }
    }
  }
}
```

### Fetch all posts

To fetch all posts execute the following query in GraphiQL:

```
{
  posts {
    edges {
      node {
        id
        title
        content
        createdAt
        tags {
          edges {
            node {
              id
              name
            }
          }
        }
      }
    }
  }
}
```

Fetch all posts with a certain tag name:

```
{
  posts(tagName:"Foo") {
    edges {
      node {
        id
        title
        content
        createdAt
      }
    }
  }
}
```

Fetch all posts created at:

```
{
  posts(createdAt:"2021-04-05 22:03:09.235258") {
    edges {
      node {
        id
        title
        content
        createdAt
      }
    }
  }
}
```



## What you need to do

We need you to take this sample project, fork the repository, and add some extra features.

### Key goals and deliverables

- [x] We would like to be able to tag posts by associating zero or more tags with a single post.
- [x] We would like to filter the list of posts by tag.
- [x] We would like to filter posts by the date they were created.
- [x] Some of our client consume the blog content via the GraphQL API. Currently they can only list and create posts, but have asked for the ability to edit and delete posts.
- [x] We would also like to filter posts by tag and creation date via the GraphQL API.

**Bonus points**

- Implement user authentication (consider using [Flask-Login](https://flask-login.readthedocs.io/en/latest/))
- Deploy the project in AWS, Azure or GCP
- Add unit tests for the new features

### Dependencies and tools

You may install any other third-party dependencies and tools.

### Assignment submission

Submit this assignment by creating a fork of this repository in your own GitHub account and send a link to your _public_ fork to work@teamgeek.io (Please do not create a pull-request).

**NOTE:** Do not remove the *Plagiarism declaration*.

## Plagiarism declaration

1. I know that plagiarism is wrong. Plagiarism is to use another’s work and pretend that it is one’s own.
2. This assignment is my own work.
3. I have not allowed, and will not allow, anyone to copy my work with the intention of passing it off as his or her own work.
4. I acknowledge that copying someone else’s assignment (or part of it) is wrong and declare that my assignments are my own work.
