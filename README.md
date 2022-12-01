# Opply Assignment

## Topics

- [Assumptions](#assumptions)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running](#running)
    - [Running the project](#running-the-project)
    - [Authentication](#authentication)
    - [Running unit tests](#running-unit-tests)
- [Extras](#extras)
- [Deployment process](#deployment-process)

## Assumptions

The following assumptions were considered:

- The project is implemented using Django with DRF;
- The project should be ready for deployment to production;
- Although not required, a swagger UI was created for testing purposes with some documentation.

## Requirements

The following requirements were considered:

- The solution must be implemented with Python;
- The solution must be implemented with Django;
- There must be a route that allows for a user to log in and retrieve its authentication token;
- There must be a route that allows a user to list all products with its id, name, price and quantity fields;
- There must be a route that allows a user to create an order for a given product;
- All orders should be registered an any user can see its order's history;
- Given that a product has enough quantity, when a user submits an order for that product then it should be expected
  that the product should decrease its quantity in stock by the same amount as defined in the order.

## Installation

This project requires `docker` and `docker-compose` to be installed (with either `v1` or `v2` version)
To set up the project run:

```shell
docker compose up web 
```

## Running

### Running the project

When the services are ready to be used, one can interact with the API at `http://0.0.0.0:8000/`.
The following routes are also available to see the schema and the documentation for the API:

- [http://0.0.0.0:8000/api/schema/swagger-ui/](http://0.0.0.0:8000/api/schema/swagger-ui/)
- [http://0.0.0.0:8000/api/schema/redoc/](http://0.0.0.0:8000/api/schema/redoc/)

### Authentication

It must be taken into account that the project uses Basic authentication and Session authentication, so it is needed to
create a user for that purpose, or use the Admin user already created. The credentials are stored in the `.env` file
with the following variables:

- `DJANGO_SUPERUSER_USERNAME`
- `DJANGO_SUPERUSER_PASSWORD`

Any new user created at `POST /api/v1/users` can also be used to log in as well

## Running unit tests

Whilst running the project, it is possible to run the unit tests with:

```shell
docker compose exec web python manage.py test tests 
```

## Extras

This project was developed using PyCharm, and this repository contains some Running configurations to run and debug the
project. It is also possible to run unit tests with it.
The indentation and formatting is done with `.editonconfig`.  
The following list highlights the possible improvements for this project:

- The `Product` model contains a `price` field, but it is not used thus far. It might make sense to have some sort of
  credit account model that could be used to validate whether a user could create an order for a given product;
- More robust documentation of the API, specifying additional details about possible errors for a given route;
- Additional tests to verify error scenarios;
- A stack of unit tests to validate the models and serializers;
- Improve `postgres` image creation;
- Create fixtures to be used in QA phase;
- Create a set of Github Actions to manage the CI pipeline.

## Deployment process

As it is, the project is ready to be sent to production when using Docker and Docker Compose, but there are 3 key things
to take in consideration:

- Create a "Continuous Integration" to validate the unit tests, run code coverage and any linters to verify code
  standards compliance;
- Create a new `.env` with different settings and adjusting it to have other settings if needed;
- Create a pipeline for "Continuous Delivery" with the new `.env` file and secrets to deploy the server into production.
  The most common scenario that should trigger a new deployment could be one when a new tag for the default branch is
  created.