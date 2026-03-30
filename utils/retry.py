import asyncio
import logging

logger=logging.getLogger(__name__)

async def retry_async(fun,retries=3,delays=2,*args,**kwargs):
    """Retry async function on failure

    Args:
        fun (_type_): async function that needs to be retried
        retries (int, optional): total no of retries. Defaults to 3.
        delays (int, optional): delay between retries. Defaults to 2.
    """
    
    for attempt in range(1,retries+1):
        try:
            return await fun(*args,*kwargs)
        except Exception as e:
            logger.warning(f"Attempt:{attempt} failed:{e}")
            if attempt==retries:
                logger.error("All retry attempts failed ❌")
                raise
        await asyncio.sleep(delays)
        
