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


def sleep_advice(hour: int) -> str:
    if 0 <= hour < 5:
        return "It is very late in Sydney. Donna should wind down and prioritize sleep now."
    if 5 <= hour < 8:
        return "It is early morning. Donna should wake gently, get light, and avoid rushing if sleep was short."
    if 8 <= hour < 21:
        return "It is daytime or early evening. Donna should protect tonight's sleep by avoiding very late caffeine and planning a reasonable bedtime."
    return "It is late evening. Donna should start winding down and avoid pushing study or screen time too far into the night."


def meal_advice(hour: int) -> str:
    if 5 <= hour < 10:
        return "Good time for breakfast or water if Donna has not eaten yet."
    if 10 <= hour < 12:
        return "A light snack may help if Donna is hungry before lunch."
    if 12 <= hour < 15:
        return "Good time for lunch and hydration."
    if 15 <= hour < 18:
        return "A small snack or water break may help maintain focus."
    if 18 <= hour < 21:
        return "Good time for dinner, ideally not too heavy if bedtime is soon."
    return "It is late. Donna should avoid a heavy meal; water or a small gentle snack is better if needed."


def eye_rest_advice(hour: int) -> str:
    if hour >= 22 or hour < 5:
        return "Late night screen use is harder on the eyes. Donna should dim screens, reduce brightness, and take a real break if possible."
    return "For long screen use, Donna should use regular eye breaks, look into the distance, blink often, and adjust brightness."


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


def conversation_signal(hour: int) -> str:
    if is_late_night(hour):
        return "late_night_care"
    if is_sleep_time(hour):
        return "sleep_wind_down"
    meal = meal_window(hour)
    if meal:
        return f"{meal}_time"
    if hour >= 20:
        return "evening_routine"
    if 5 <= hour < 7:
        return "early_morning"
    return "daytime_check_in"


def response_hint(hour: int) -> str:
    if is_late_night(hour):
        return "Donna may need a softer, shorter reply that acknowledges tiredness and gently encourages sleep."
    if is_sleep_time(hour):
        return "Donna may be winding down; keep the reply calm and avoid pushing demanding tasks."
    meal = meal_window(hour)
    if meal:
        return f"It is {meal} time in Sydney; a casual reply can naturally check whether Donna has eaten or had water."
    if hour >= 20:
        return "It is evening in Sydney; a reply can be warm, low-pressure, and mindful of rest."
    return "Use a natural casual tone while staying aware of Donna's day, study, meals, eyes, and routine."


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
def get_donna_context() -> dict[str, str]:
    """Use this tool whenever replying to Donna in casual conversation, especially when the reply may depend on time, sleep, meals, study, eye strain, weather, or daily routine. This tool returns Donna's current Sydney date/time context plus practical sleep, meal, and eye-rest advice."""
    payload = current_time_payload(DEFAULT_TIMEZONE)
    hour = datetime.now(ZoneInfo(DEFAULT_TIMEZONE)).hour
    payload.update(
        {
            "sleep_advice": sleep_advice(hour),
            "meal_advice": meal_advice(hour),
            "eye_rest_advice": eye_rest_advice(hour),
            "preferred_name": "Donna",
        }
    )
    return payload


@mcp.tool()
def get_conversation_context() -> dict[str, str | bool]:
    """Use this tool before replying to Donna in everyday casual conversation, especially when Donna says she is tired, sad, sleepy, has eye strain, says hi, says good morning/night, or talks about meals, study, sleep, daily routine, or time."""
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
        "current_date": now.strftime("%Y-%m-%d"),
        "weekday": now.strftime("%A"),
        "timezone": timezone,
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
