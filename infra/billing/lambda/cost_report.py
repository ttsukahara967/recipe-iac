"""Daily AWS cost report.

Triggered by EventBridge once a day. Reads month-to-date and previous-day cost from
Cost Explorer and publishes a short summary to an SNS topic (delivered by email).
Cost Explorer is only available through the us-east-1 endpoint, regardless of where
this function runs.
"""

import datetime
import os

import boto3

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
PROJECT = os.environ.get("PROJECT", "recipe-iac")

ce = boto3.client("ce", region_name="us-east-1")
sns = boto3.client("sns")


def _jst_today() -> datetime.date:
    # Lambda runs in UTC; the report is framed in JST (the user's timezone).
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).date()


def _month_to_date(today: datetime.date):
    # End is exclusive, so add a day to include today's (still-accruing) cost.
    start = today.replace(day=1)
    end = today + datetime.timedelta(days=1)
    resp = ce.get_cost_and_usage(
        TimePeriod={"Start": start.isoformat(), "End": end.isoformat()},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )
    total = 0.0
    unit = "USD"
    services = []
    for period in resp["ResultsByTime"]:
        for group in period["Groups"]:
            metric = group["Metrics"]["UnblendedCost"]
            amount = float(metric["Amount"])
            unit = metric["Unit"]
            total += amount
            if amount > 0:
                services.append((group["Keys"][0], amount))
    services.sort(key=lambda item: item[1], reverse=True)
    return total, unit, services


def _previous_day(today: datetime.date):
    start = today - datetime.timedelta(days=1)
    resp = ce.get_cost_and_usage(
        TimePeriod={"Start": start.isoformat(), "End": today.isoformat()},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
    )
    results = resp["ResultsByTime"]
    if not results:
        return 0.0, "USD"
    metric = results[0]["Total"]["UnblendedCost"]
    return float(metric["Amount"]), metric["Unit"]


def handler(event, context):
    today = _jst_today()
    total, unit, services = _month_to_date(today)
    prev_amount, prev_unit = _previous_day(today)

    # Email body is user-facing, so it is written in Japanese (like the site content).
    lines = [
        f"{PROJECT} AWS 利用料金レポート（{today.isoformat()} JST 時点）",
        "",
        f"今月ここまでの合計: {total:.2f} {unit}",
        f"前日の利用額:       {prev_amount:.2f} {prev_unit}",
    ]
    if services:
        lines.append("")
        lines.append("サービス別（今月・上位5件）:")
        for name, amount in services[:5]:
            lines.append(f"  {name}: {amount:.2f} {unit}")
    lines.append("")
    lines.append("※ Cost Explorer のデータは確定まで最大1日ほど遅れる場合があります。")
    message = "\n".join(lines)

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"[{PROJECT}] AWS cost {today.isoformat()}: {total:.2f} {unit}",
        Message=message,
    )
    return {"total": round(total, 2), "unit": unit}
