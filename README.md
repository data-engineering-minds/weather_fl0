# weather_fl0
A Python web service application that uses [Flask](https://flask.palletsprojects.com/en/2.3.x/) and [OpenWeatherMap](https://openweathermap.org/) API to perform the following:

* Display the weather data for different cities in Germany.
* Display the weather data for the city viewed most number of times in the current day.
* Display the total number of page visits for current day.

The application is deployed using [FL0](https://www.fl0.com/) Platform.

## Steps to run locally
* Create a file *.env* and copy the contents of the file *[`.env_local`](.env_local)*.
* Put the API key from your OpenWeatherMap account.
* Run the docker-compose command as below:<br/>
`docker-compose -f docker-compose.yaml up -d`
* Check the application via http://localhost:5001

## Things to remember before deploying on FL0
* Create the environment variables specified in the file *[`.env_flo`](.env_fl0)* on FL0.
* For *DATABASE_URL*, specify the first part of the hostname as endpoint for options. For example,<br/>
`postgresql://<USER>:<PASSWORD>@ep-noisy-queen-65812933.eu-central-1.aws.neon.tech:5432/<DATABASE_NAME>?options=endpoint%3Dep-noisy-queen-65812933`


