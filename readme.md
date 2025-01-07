# NBA Game Day Notifications 🏀

Never miss an NBA game again! This AWS-powered system automatically sends you real-time NBA game updates through text messages or email.

## What Does It Do?

- Sends you live NBA game scores and updates
- Works automatically on game days
- Delivers updates through text or email
- Shows you quarter-by-quarter scores
- Tells you what channel the game is on
- Keeps you updated on game status (scheduled, in progress, or final)

## What You'll Need

1. An AWS account
2. An API key from SportsData.io (they have a free tier)
3. Basic Python knowledge
4. About 15 minutes to set everything up

## Quick Setup Guide

### Step 1: Set Up AWS SNS (for notifications)

1. Go to AWS SNS console
2. Create a new topic
3. Add your phone number or email as a subscriber
4. Save the topic ARN - you'll need it later

### Step 2: Create the Lambda Function

1. Create a new Python Lambda function
2. Copy the code from `lambda_function.py`
3. Add these environment variables:
   - `NBA_API_KEY`: Your SportsData.io API key
   - `SNS_TOPIC_ARN`: The SNS topic ARN from Step 1

### Step 3: Set Up Regular Updates

1. Go to EventBridge
2. Create a new rule
3. Set it to run every hour (or however often you want updates)
4. Point it to your Lambda function

## How the Updates Look

You'll get messages that look like this:

For a finished game:

```
Game Status: Final
Away Team: GSW
Home Team: LAL
Final Score: 120-115
Start Time: 2024-01-07T19:30:00
Channel: ESPN
Quarters: Q1: 30-28, Q2: 25-27, Q3: 32-30, Q4: 33-30
```

For a game in progress:

```
Game Status: In Progress
Away Team: GSW
Home Team: LAL
Start Time: 2024-01-07T19:30:00
Channel: ESPN
Quarters: Q1: 30-28, Q2: 25-27
```

For an upcoming game:

```
Game Status: Scheduled
Away Team: GSW
Home Team: LAL
Start Time: 2024-01-07T19:30:00
Channel: ESPN
```

## Main Files

- `lambda_function.py`: The main Lambda function that handles everything

## What's Happening Behind the Scenes?

1. EventBridge triggers your Lambda function
2. Lambda checks SportsData.io for today's games
3. The code formats the game data nicely
4. AWS SNS sends you the formatted updates
5. All times are handled in Central Time

## Common Issues and Fixes

- Not getting updates? Check your SNS subscription
- Error messages? Verify your API key
- Wrong times? The system uses Central Time
- Missing data? The API might be having issues - the code will retry automatically
