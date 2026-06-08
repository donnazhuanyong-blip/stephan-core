from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from mcp.server.fastmcp import FastMCP


DEFAULT_TIMEZONE = "Australia/Sydney"
HOST = "0.0.0.0"
PORT = 8000
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


@mcp.tool()
def get_current_time(timezone: str = DEFAULT_TIMEZONE) -> dict[str, str]:
    """Return the current local date and time for a timezone."""
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


if __name__ == "__main__":
    print("Time MCP running at http://localhost:8000/mcp", flush=True)
    mcp.run(transport="streamable-http")
