import os
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from mcp.server.fastmcp import FastMCP


DEFAULT_TIMEZONE = "Australia/Sydney"
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8000"))
MCP_PATH = "/mcp"

mcp = FastMCP(
    "chatgpt-devmode-time-server",
    host=HOST,
    port=PORT,
    streamable_http_path=MCP_PATH,
)


def period_label(hour: int) -> str:
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    if 17 <= hour < 21:
        return "evening"
    return "night"


def is_late_night(hour: int) -> bool:
    return 0 <= hour < 5


def is_sleep_time(hour: int) -> bool:
    return hour >= 23 or hour < 5


def meal_window(hour: int) -> str | None:
    if 7 <= hour < 10:
        return "breakfast"
    if 12 <= hour < 14:
        return "lunch"
    if 18 <= hour < 20:
        return "dinner"
    return None


def response_hint(hour: int) -> str:
    if is_late_night(hour):
        return "Be gentle; suggest rest."
    if is_sleep_time(hour):
        return "Keep it calm and brief."
    meal = meal_window(hour)
    if meal:
        return f"Check {meal} or hydration."
    if hour >= 20:
        return "Keep it warm and low-pressure."
    return "Reply naturally and briefly."


def current_time_payload(timezone: str) -> dict[str, str]:
    try:
        tz = ZoneInfo(timezone)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unknown timezone: {timezone}") from exc

    now = datetime.now(tz)
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": now.strftime("%A"),
        "timezone": timezone,
        "period": period_label(now.hour),
    }


@mcp.tool()
def get_current_time(timezone: str = DEFAULT_TIMEZONE) -> dict[str, str]:
    """Return the current local date, time, weekday, timezone, and period label for a requested IANA timezone."""
    return current_time_payload(timezone)


@mcp.tool()
def get_conversation_context() -> dict[str, str | bool]:
    """Use this tool only when Donna’s message clearly depends on local time, daily routine, sleep, meals, eye strain, study schedule, weather, or date context. Do not use it for simple affection, jokes, short emotional replies, or casual messages like ‘宝宝’, ‘我爱你’, ‘哈哈’, unless Donna mentions tiredness, sleep, eyes, meals, study, morning/night, or asks about time/date."""
    timezone = DEFAULT_TIMEZONE
    tz = ZoneInfo(timezone)
    now = datetime.now(tz)
    hour = now.hour
    meal = meal_window(hour)
    late_night = is_late_night(hour)
    sleep_time = is_sleep_time(hour)
    eye_rest_needed = hour >= 21 or late_night

    return {
        "current_time": now.strftime("%H:%M:%S"),
        "period": period_label(hour),
        "is_late_night": late_night,
        "is_meal_time": meal is not None,
        "is_sleep_time": sleep_time,
        "eye_rest_needed": eye_rest_needed,
        "response_hint": response_hint(hour),
    }


if __name__ == "__main__":
    print(f"Time MCP running at http://localhost:{PORT}/mcp", flush=True)
    mcp.run(transport="streamable-http")
