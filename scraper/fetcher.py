import aiohttp

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
    async with aiohttp.ClientSession(headers=HEADERS,timeout=timeout) as session:
        # make the request
        async with session.get(url) as response:
            #read the body
            if response.status != 200:
                raise Exception(f"Failed to fetch url: {url}, Status code: {response.status}")
            return await response.text()
 
       