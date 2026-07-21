import aiohttp
import logging

logger = logging.getLogger(__name__)
HEADERS={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

async def fetch_html(url:str)->str:
    """Fetch html content of url

    Args:
        url (str): Target webpage url

    Returns:
        str: HTML content of page
    """
    timeout=aiohttp.ClientTimeout(total=60)
    #open session
    try:
        async with aiohttp.ClientSession(headers=HEADERS,timeout=timeout) as session:
            # make the request
            logger.info("Fetching %s", url)
            async with session.get(url) as response:
                #read the body
                logger.info("Successfully fetched %s", url)
                if response.status != 200:
                    logger.error("HTTP %s returned for %s", response.status, url)
                    raise Exception(f"Failed to fetch url: {url}, Status code: {response.status}")
                return await response.text()
    except Exception:
        logger.exception("Error fetching %s", url)
        raise
 
       