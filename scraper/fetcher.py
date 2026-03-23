import asyncio

import aiohttp


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}


async def fetch_html(
    url: str,
    retries: int = 3,
    timeout: int = 20,
    retry_delay: float = 1.0,
) -> str:
    last_error: Exception | None = None
    client_timeout = aiohttp.ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(headers=DEFAULT_HEADERS, timeout=client_timeout) as session:
        for attempt in range(1, retries + 1):
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.text()
            except (aiohttp.ClientError, asyncio.TimeoutError) as error:
                last_error = error
                if attempt == retries:
                    break
                await asyncio.sleep(retry_delay)

    if last_error is not None:
        raise last_error
    raise RuntimeError("Failed to fetch HTML.")
