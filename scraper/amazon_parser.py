from bs4 import BeautifulSoup
from models.products import ProductDetails
import logging

logger = logging.getLogger(__name__)

def get_text(soup,**kwargs):
    tag=soup.find(**kwargs)
    return tag.text.strip() if tag else None

def get_attr(soup,attr,**kwargs):
    tag=soup.find(**kwargs)
    return tag.get(attr) if tag else None

def parse_product(html:str) -> ProductDetails:
    """extrat product info from Amazon webpage

    Args:
        html (str): HTML body of webpage
    """
    soup=BeautifulSoup(html,"html.parser")
  
    title=get_text(soup,id="productTitle")
    if not title:
        logger.warning("Product title not found while parsing page")
    rating_text=get_text(soup,id="averageCustomerReviews")
    rating=float(rating_text.split()[0]) if rating_text else None
    
    price=get_attr(soup,"value",id="priceValue")
    price=float(price) if price else None
    if price is None:
     logger.warning("Price not found for '%s'", title or "Unknown Product")
    
    return ProductDetails(title,price,rating)
 