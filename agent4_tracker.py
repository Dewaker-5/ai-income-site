import os
import json
from datetime import date, timedelta

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account

PROPERTY_ID = os.environ.get("GA_PROPERTY_ID")

def get_client():
    creds_json = os.environ.get("GA_CREDENTIALS")
    if creds_json:
        info = json.loads(creds_json)
        creds = service_account.Credentials.from_service_account_info(info)
    else:
        creds = service_account.Credentials.from_service_account_file(
            os.environ["GA_CREDENTIALS_FILE"]
        )
    return BetaAnalyticsDataClient(credentials=creds)

def run_report(client, days=7):
    today = date.today()
    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(
            start_date=(today - timedelta(days=days)).isoformat(),
            end_date=today.isoformat(),
        )],
    )
    return client.run_report(request)

def track():
    if not PROPERTY_ID:
        print("Error: GA_PROPERTY_ID not set")
        return

    client = get_client()
    response = run_report(client)

    print(f"{'Page':<60} {'Views':<8}")
    print("-" * 70)
    total = 0
    for row in response.rows:
        page = row.dimension_values[0].value
        views = int(row.metric_values[0].value)
        total += views
        print(f"{page:<60} {views:<8}")

    print("-" * 70)
    print(f"{'TOTAL':<60} {total:<8}")
    print(f"\nPeriod: last 7 days")

if __name__ == "__main__":
    track()
