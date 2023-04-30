## Bot Info

> The aim of the Virtusl-League-Data-Bot is to get all match fixation results per week in a premier league(virtual) by scraping the data from a popular sporting site, formats and cleans the data and then pushes it to a google sheet using Sheety API. This program is containerised using docker, pushed to a private repo in an AWS Container Registry and is run by in an AWS Lambda function, triggered every 4 minutes.

## Requirements
- Docker
- Selenium
- Requests 
- Have at least a free tier account in AWS

## How to use the bot
- Clone the repo

- Create a new google spreadsheet and rename it from "Untitled" to a name of your choosing

- Below the spreadsheet, change the name of the open sheet from "sheet1" to "League Table". Please note that if you decide to use a different sheet name (this is different from the spread sheet name above), then you must update the data dictionary in the function: send_to_google_sheet in main.py like so:

```
    # change "leagueTable" to your desired name, using camel case without a space and the first letter must be lower case even if the name of the sheet starts with an upper case
    body = {
        "leagueTable": final_data 

    }

```
The above step is very essential for use with the API

- To use the Sheety API, click this [link](https://sheety.co/) to create an account:
   - Read the documentation on how to connect the google sheet created above with the API
   - Create a Basic Authentication with a username and password
   - Retrieve your specific url from the API
   - Enable GET,POST and/or PUT requests

- Create environment variables in your local machine if you choose to run the bot locally. Otherwise, do likewise in whatever environment you choose to run the bot
    - Variable name: LEAGUE_SHEETY_ENDPOINT , key: THE URL YOU GET FROM SHEETY API
    - Variable name: LEAGUE_SHEETY_PASSWORD, key: YOUR PASSWORD INPUTED IN THE BASIC AUTHENTICATION PART OF THE SHEETY API
    - Variable name: LEAGUE_SHEETY_USER_NAME, key: YOUR USERNAME INPUTED IN THE BASIC AUTHENTICATION PART OF THE SHEETY API

- Open your terminal and install awscli

- Log in to your AWS account and create a private repo in AWS ECR 

## Running the bot

- In your AWS management console, click on " View push commands "
- Copy and paste the commands in your terminal and click enter one after the other
- Create an AWS Lambda function with the option of container
- Update the general configuration with RAM of 1000 and increase timeout to at least 5 mins
- Update environment variables in the lambda function with the ones created above
- Create a trigger event with 4 minutes 

## Credits

- [umihico](https://github.com/umihico/docker-selenium-lambda.git)