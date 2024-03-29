# Code Challenge Template
## Problem 1 - Data Modeling

-------------------------


Choose a database to use for this coding exercise (SQLite, Postgres, etc.). Design a data model to represent the weather data records. If you use an ORM, your answer should be in the form of that ORM's data definition format. If you use pure SQL, your answer should be in the form of DDL statements.

*Solution*
We use sqlite to form our data model and generate DDL statements for creating WeatherData table and wx_data.db database.
**Refer to the following script: answers/P1DataModeling.py**



## Problem 2 - Ingestion

---------------------

Write code to ingest the weather data from the raw text files supplied into your database, using the model you designed. Check for duplicates: if your code is run twice, you should not end up with multiple rows with the same data in your database. Your code should also produce log output indicating start and end times and number of records ingested.

**For Solution, refer to the following script: answers/P2Ingest.py**

## Problem 3 - Data Analysis

-------------------------

For every year, for every weather station, calculate:
* Average maximum temperature (in degrees Celsius)

* Average minimum temperature (in degrees Celsius)

* Total accumulated precipitation (in centimeters)
Ignore missing data when calculating these statistics.
Design a new data model to store the results. Use NULL for statistics that cannot be calculated.
Your answer should include the new model definition as well as the code used to calculate the new values and store them in the database.

*Solution*
We define a new data model - WeatherAnalysis Table in the wx_data.db database. 
Then we analyze the pre-existing loaded data in WeatherData to process and load it into the WeatherAnalysis table.
**Refer to the script: answers/P3WeatherAnalysis.py**

## Problem 4 - REST API

--------------------

Choose a web framework (e.g. Flask, Django REST Framework). Create a REST API with the following GET endpoints:
/api/weather
/api/weather/stats

Both endpoints should return a JSON-formatted response with a representation of the ingested/calculated data in your database. Allow clients to filter the response by date and station ID (where present) using the query string. Data should be paginated.
Include a Swagger/OpenAPI endpoint that provides automatic documentation of your API.
Your answer should include all files necessary to run your API locally, along with any unit tests.

*Solution*
This Flask application effectively addresses Problem 4 by creating a REST API that serves weather data. Here's how it solves each part of the problem:

#### REST API Creation with Flask

- **Flask and Flask-RESTful** are used to set up and define the REST API. Flask-RESTful simplifies API creation with resource-based classes.

#### Endpoints

- **Two GET endpoints** (`/api/weather` and `/api/weather/stats`) are defined, corresponding to fetching weather data and weather statistics, respectively.

#### JSON Responses

- Both endpoints **return JSON-formatted responses**, aligning with the requirement for the API to output data in a structured and easily consumable format for clients.

#### Query String Filtering

- The API allows clients to **filter responses based on query string parameters** (e.g., `station_id`, `start_date`, `end_date`, `year`). This feature enhances the API's flexibility, allowing users to retrieve specific subsets of data.

#### Pagination

- The `/api/weather` endpoint incorporates **pagination**, a crucial feature for APIs that can potentially return large sets of data. Pagination improves performance and usability by limiting the number of records in a single response and allowing clients to fetch data incrementally.

#### Database Integration

- Utilizing **SQLite through direct connections**, the API interacts with a database to fetch weather data and statistics. While SQLite is simple and sufficient for demonstration purposes or lightweight applications, this approach showcases how to execute raw SQL queries within a Flask application.

#### Swagger UI Documentation

- **Swagger (Flasgger)** integration provides automatic API documentation, making the API easier to use and understand. The `@swag_from` decorators reference YAML files that contain the OpenAPI specifications for each endpoint, offering a self-documenting API that users can interact with through a generated web interface.

**Refer to the script: answers/P4api.py**


#### Unit Test Cases
We wrote test cases in the testcases.py


**Refer to the script: answers/testcases.py**


## Deployment

-------------------------

To incorporate AWS S3 for storing raw data files and streamline the deployment of our app, we have 
1. **S3 Bucket**: Create an S3 bucket and upload your raw `.txt` data files.
2. **Docker**: Containerize your Flask API and data ingestion scripts.
3. **Amazon Elastic Container Service(ECS)**: Deploy containers to ECS for serverless execution.
4. **RDS**: Set up your database on RDS or Aurora.
5. **Lambda + CloudWatch Events**: Schedule data ingestion scripts with Lambda functions triggered by CloudWatch Events.
6. **CloudWatch**: Monitor application and infrastructure performance.
8. **CodePipeline + CodeBuild**: Automate deployments with a CI/CD pipeline.

