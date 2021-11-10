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

### Flow Diagram
![](https://github.com/bnidevs/ButtonParty/blob/documentation/docs/backend-flowchart.png?raw=true)

### AWS Details
See [`cftemplate.json`](https://github.com/bnidevs/ButtonParty/blob/main/cftemplate.json) (CloudFormation template) for more configuration details

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

#### Lambda
We have one Lambda function supporting the `/fetch` route on our API Gateway. This lends itself to even more compartmentalization as our Lambda is not permitted to write to the database in any way, only the EC2 instances, more specifically, just the incoming-traffic-handler (more details in the EC2 section).

The Lambda function is written in Python and will return the client's username, score and streak under `/fetch/self`. It will return the top 10 players' usernames and scores under `/fetch/lb`.

#### Secrets Manager
Our Secrets Manager holds one secret, it being the database username and password.

#### EC2

**Incoming Traffic Handler**



**Outgoing Traffic Handler**

#### SQS

We use SQS as a method of communication from API Gateway to and within provisioned compute instances.

The first 3 queues are meant for API call passthrough. They are linked via AWS proxy to accept API request bodies. 

**Queues**

*Add User*

This queue intakes from our API Gateway `/add` route.

The incoming traffic handler pulls messages from this queue.

*Press Button*

This queue intakes from our API Gateway `/press` route.

The incoming traffic handler pulls messages from this queue.

*Powerup*

This queue intakes from our API Gateway `/powerup` route.

The incoming traffic handler pulls messages from this queue.

*Timestamp*

This queue intakes from our outgoing traffic handler.

It will be passed timestamps for when to stop accepting button presses.

Example: If button is made available at 3:00 PM, the outgoing traffic handler will pass 3:01 PM to the queue so that the incoming traffic handler knows to stop accepting button presses at 3:01 PM.

The incoming traffic handler pulls messages from this queue.

#### SNS

### Firebase + GCP Details

#### Cloud Messaging

#### User Authentication