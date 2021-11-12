# ButtonParty

Alex Pinkowski, Bill Ni, Brandon George, Sage Charity Griffiths

## Game Logic

Players are given a single button which will light up at random times throughout the day.

If they press this button, they will increase their score (number of points), and their streak.

The higher their streak, the more valuable each button press becomes (point curve: s < 10, y = x; s ≥ 10, y = x<sup>2</sup>).

Each players score is then consumed to calculate the leaderboard, containing the top 10 players by score.

Players can use their points to purchase powerups, which will provide varying kinds of bonuses for the player.

### Powerups

#### Freeze

Players can purchase a freeze to nullify button presses for a certain amount of time.

#### Multiplier

Players can purchase a multiplier to increase the amount of points they receive per button press for a certain amount of time.

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

*FreezePowerup*

| username   | activeUntil      |
|------------|------------------|
| robocop    | 11/20/21 9:00 PM |
| loki       | 9/3/21 11:00 AM  |
| dumbledore | 12/6/21 4:00 PM  |

#### Lambda
We have one Lambda function supporting the `/fetch` route on our API Gateway. This lends itself to even more compartmentalization as our Lambda is not permitted to write to the database in any way, only the EC2 instances, more specifically, just the incoming-traffic-handler (more details in the EC2 section).

The Lambda function is written in Python and will return the client's username, score and streak under `/fetch/self`. It will return the top 10 players' usernames and scores under `/fetch/lb`.

#### Secrets Manager
Our Secrets Manager holds one secret, it being the database username and password.

#### EC2

**Incoming Traffic Handler**

Our incoming traffic handler is a `t3.small` (see more details about instance types [here](https://aws.amazon.com/ec2/instance-types/)).

A production version of our application should wrap this provision of the backend in an auto scaling group + load balancer wrapper because handling API calls and writing to the database can be sped up by parallelizing the message processing. We can also predictably scale because we know exactly when API calls will increase in volume: when we open the client side button for pressing (see below in Outgoing Traffic Handler for more details).

The incoming traffic handler manages user account creation, button pressing, and powerup purchasing. API calls for account creation and powerup purchasing are not dependent on the timestamps passed from the outgoing traffic handler. However, the incoming traffic handler will only accept API calls for button presses sent before the timestamp provided by the outgoing traffic handler.

*Handling Cheating*

We have understood that players can try to bypass our code and increase their score by grabbing our API link directly by tampering with the installation of the app.

We have taken several measures to inhibit this type of cheating.

1. The timestamp queue restricts players from pressing the button outside of the allocated times.
2. In our code, we perform a "pressed-already" verification against the `pressed` column of our database. If the player has already pressed once during the allocated time, any extra presses will not increase score.
3. In previous iterations of our design, we stored some user data, including their score and their streak on the client side, so that the API call for pressing the button would include their new streak and new score. We have now removed this design, and instead opted for a completely server-side data store so that the user cannot make such API calls.
4. As a stretch goal, we plan on adding preflight headers and token based authentication so that all API calls are verified and restrict database modification to solely the user that called the API.

**Outgoing Traffic Handler**

Our outgoing traffic handler is a `t2.micro` (see more details about instance types [here](https://aws.amazon.com/ec2/instance-types/)).

We don't need an auto scaling group + load balancer wrapper on top of this because the notification spooling handled by this instance doesn't need to scale based on how many clients we serve notifications to. Notifications are sent via AWS Proxy on SNS, so we only need to send one message to distribute a notification to an unlimited number of clients.

When the outgoing traffic handler sends a notification, it will also pass a message to the incoming traffic handler via the timestamp SQS so that the incoming traffic handler can begin accepting API calls from pressing the button on the client side.

*Game Statistics*

The outgoing traffic handler will send a notification (open the button for presses) at a random time with a buffer.

The randomness is 1/10000 chance of a notification every second, with a buffer of 1 hour so that the unlikely event of 2 closely occurring events is mitigated. This results in an expected occurrence schedule of 1 notification every ~3.778 hours, or 3 hours and ~47 minutes.

After the outgoing traffic handler opens the button for pressing, users have 100 seconds to press the button. This is controlled by sending a timestamp of the current time + 100 seconds to the incoming traffic handler via the timestamp SQS.

#### SQS

We use SQS as a method of communication from API Gateway to and within provisioned compute instances.

The first 3 queues are meant for API call passthrough. They are linked via AWS proxy to accept API request bodies. 

**Queues**

*Add User*

This queue intakes from our API Gateway `/add` route.

Messages for adding users are passed through to our provisioned instances here.

Messages contain the registration token for adding push notification endpoints to our SNS platform and some form of identification from an OAuth service.

The incoming traffic handler pulls messages from this queue.

*Press Button*

This queue intakes from our API Gateway `/press` route.

Messages contain the streak number and identification token. Calculation of points and tampering verification is done on backend.

Stretch goal is adding an additional layer of authentication using preflight headers to authenticate and providing a federated identity upon security grant.

The incoming traffic handler pulls messages from this queue.

*Powerup*

This queue intakes from our API Gateway `/powerup` route.

Messages contain the powerup type, size, timestamp and identification token.

The incoming traffic handler pulls messages from this queue.

*Timestamp*

This queue intakes from our outgoing traffic handler.

It will be passed timestamps for when to stop accepting button presses.

Example: If button is made available at 3:00 PM, the outgoing traffic handler will pass 3:01 PM to the queue so that the incoming traffic handler knows to stop accepting button presses at 3:01 PM.

The incoming traffic handler pulls messages from this queue.

#### SNS

We have set up an SNS topic for distributing messages from our outgoing traffic handler. We have also set up a Firebase Cloud Messaging application platform for adding application endpoints. 

Our incoming traffic handler automates adding new users to the application platform then adding the endpoints to the designated topic.

### Firebase + GCP Details

We utilize Firebase for logging in users via Google and sending notifications to Android devices.

#### Cloud Messaging

Firebase serves as a midway point for our notification pipeline. We serve notifications from our outgoing traffic handler, then pass it through SNS, and Firebase processes these requests as native app push notifications on the client side.

#### User Authentication

We authenticate users of our app with Google (hopefully more platforms to come) via an OAuth consent screen. We use the identification token that we choose (can be email, openID, etc.) and create a new user account for them on the server side.