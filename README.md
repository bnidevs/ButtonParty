# ButtonParty

## Stack
### Frontend
 - React Native
### Backend
 - AWS
   - EC2
   - SNS
   - SQS
   - API Gateway
   - RDS (Aurora)
   - Lambda
 - Python3

## AWS Details
See [`cftemplate.json`](https://github.com/bnidevs/ButtonParty/blob/main/cftemplate.json) (CloudFormation template) for more configuration details

### Flow Diagram
![](https://github.com/bnidevs/ButtonParty/blob/documentation/docs/backend-flowchart.png?raw=true)

#### API Gateway
The API Gateway is set up with 3 routes:
 - `add` - POST

   - This route handles adding user accounts to the database (and by extension, the leaderboard).

   - It takes a user identifier (email, OpenID, or some other form of unique identification token), and a registration token for cloud messaging + push notifications.

   - This route redirects requests into an SQS which is polled by the incoming traffic handler.

 - `press` - POST

   - This route handles button presses from users and score increases.

   - It takes a user identifier, and a streak number for score incrementing.

   - This route redirects requests into an SQS which is polled by the incoming traffic handler.

 - `powerups` - POST

   - This route handles powerup purchasing and usage.

   - It takes a user identifier, powerup type, and powerup level for usage.

   - This route redirects requests into an SQS which is polled by the incoming traffic handler.

 - `fetch`

   - This route is split into 2 subroutes for leaderboard fetching and user data fetching.

   - `self` - GET
   
     - This route handles fetching user data: button press streak, and score.

     - It takes a user identifier.
   
     - This route redirects requests into the [lambda function](https://github.com/bnidevs/ButtonParty/blob/documentation/backend/fetch/lambda_handler.py) responsible for returning this data pulled from the database.
   
   - `lb` - GET

     - This route handles fetching the top 10 scores.
   
     - This route redirects requests into the same lambda function mentioned above.

#### RDS
The RDS consists of a serverless Aurora cluster with a minimum allocation of 1 compute unit and a maximum allocation of 2 compute units (subject to production conditions).

**Schemas**

*Users*

| username | score | streak | pressed |
|----------|-------|--------|---------|
| robocop  | 12890 | 4      | false   |
| loki     | 5     | 0      | false   |
| dumbledore | 320 | 8      | false   |

