import os
import json
from datetime import date, timedelta

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from google.oauth2 import service_account
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
GA_PROPERTY_ID = os.environ["GA_PROPERTY_ID"]

def get_ga_client():
    creds_json = os.environ.get("GA_CREDENTIALS")
    if creds_json:
        info = json.loads(creds_json)
        creds = service_account.Credentials.from_service_account_info(info)
    else:
        creds = service_account.Credentials.from_service_account_file(
            os.environ["GA_CREDENTIALS_FILE"]
        )
    return BetaAnalyticsDataClient(credentials=creds)

def fetch_ga_data(client, days=7):
    today = date.today()
    request = RunReportRequest(
        property=f"properties/{GA_PROPERTY_ID}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(
            start_date=(today - timedelta(days=days)).isoformat(),
            end_date=today.isoformat(),
        )],
    )
    return client.run_report(request)

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

def report():
    client = get_ga_client()
    response = fetch_ga_data(client)

    lines = ["*AI Tools Hub — Weekly Report*", f"Period: Last 7 days\n"]
    total = 0
    page_data = []

    for row in response.rows:
        page = row.dimension_values[0].value
        views = int(row.metric_values[0].value)
        total += views
        if views > 0:
            page_data.append((page, views))

    if not page_data:
        lines.append("No traffic data yet.")
    else:
        page_data.sort(key=lambda x: x[1], reverse=True)
        for page, views in page_data:
            lines.append(f"  {page} — {views} views")
        lines.append("")

    lines.append(f"*Total Views: {total}*")
    lines.append(f"\nReport generated: {date.today()}")

    message = "\n".join(lines)
    send_telegram(message)
    print("Weekly report sent to Telegram.")

if __name__ == "__main__":
    report()
