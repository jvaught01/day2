import urllib.request
import boto3
from datetime import datetime, timedelta, timezone
import os
import json


def format_game_data(game):
    status = game.get("Status", "Unknown")
    away_team = game.get("AwayTeam", "Unknown")
    home_team = game.get("HomeTeam", "Unknown")
    final_score = game.get("FinalScore", "Unknown")
    start_time = game.get("StartTime", "Unknown")
    channel = game.get("Channel", "Unknown")

    quarters = game.get("Quarters", [])
    quarter_scores = ", ".join(
        [
            f"Q{q['Number']}: {q.get('AwayScore', 'N/A')}-{q.get('HomeScore', 'N/A')}"
            for q in quarters
        ]
    )

    match status:
        case "Final":
            return (
                f"Game Status: {status}\n"
                f"Away Team: {away_team}\n"
                f"Home Team: {home_team}\n"
                f"Final Score: {final_score}\n"
                f"Start Time: {start_time}\n"
                f"Channel: {channel}\n"
                f"Quarters: {quarter_scores}\n"
            )
        case "In Progress":
            return (
                f"Game Status: {status}\n"
                f"Away Team: {away_team}\n"
                f"Home Team: {home_team}\n"
                f"Start Time: {start_time}\n"
                f"Channel: {channel}\n"
                f"Quarters: {quarter_scores}\n"
            )
        case "Scheduled":
            return (
                f"Game Status: {status}\n"
                f"Away Team: {away_team}\n"
                f"Home Team: {home_team}\n"
                f"Start Time: {start_time}\n"
                f"Channel: {channel}\n"
            )
        case _:
            return (
                f"Game Status: {status}\n"
                f"{away_team} vs {home_team}\n"
                f"Details Unavailable at the moment.\n"
            )


def lambda_handler(event, context):
    sns_client = boto3.client("sns")
    topic_arn = os.getenv("SNS_TOPIC_ARN")
    api_key = os.getenv("NBA_API_KEY")

    utc_now = datetime.now(timezone.utc)
    central_time = utc_now - timedelta(hours=6)
    todays_date = central_time.strftime("%Y-%m-%d")

    print(f"Fetching games for {todays_date}")

    url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{todays_date}?key={api_key}"
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching games: {e}")
        return

    formatted_data = [format_game_data(game) for game in data]
    message = "\n\n".join(formatted_data)

    try:
        sns_client.publish(TopicArn=topic_arn, Message=message)
        print("Message sent successfully")
    except Exception as e:
        print(f"Error sending message: {e}")
        return {"statusCode": 500, "body": "Error publishing to SNS"}

    return {"statusCode": 200, "body": "Message sent successfully"}


lambda_handler(None, None)
