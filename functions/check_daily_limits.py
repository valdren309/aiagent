import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("Set the OPENROUTER_API_KEY environment variable first.")

request = Request(
    "https://openrouter.ai/api/v1/key",
    headers={"Authorization": f"Bearer {api_key}"},
)

try:
    with urlopen(request, timeout=20) as response:
        data = json.load(response).get("data", {})
except HTTPError as error:
    print(f"OpenRouter returned HTTP {error.code}: {error.read().decode()}")
    raise
except URLError as error:
    raise RuntimeError(f"Could not reach OpenRouter: {error.reason}") from error

free_daily = data.get("free_model_daily_requests")
if free_daily:
    remaining = free_daily.get("remaining")
    limit = free_daily.get("limit")
    print(f"Free-model daily requests: {remaining} remaining of {limit}")
    if remaining == 0:
        print("Daily free-model request limit is exhausted.")
else:
    print("No free-model daily request count was returned for this key.")

budget = data.get("effective_budget")
if budget:
    remaining_usd = budget.get("remaining_usd")
    limit_usd = budget.get("limit_usd")
    print(f"Configured budget: ${remaining_usd} remaining of ${limit_usd}")
    if remaining_usd is not None and remaining_usd <= 0:
        print(f"Configured budget is exhausted. Reset: {budget.get('resets_at')}")
else:
    print("No effective budget was returned for this key.")
