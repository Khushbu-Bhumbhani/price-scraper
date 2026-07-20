from bs4 import BeautifulSoup
from models.products import ProductDetails

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
    
    rating_text=get_text(soup,id="averageCustomerReviews")
    rating=float(rating_text.split()[0]) if rating_text else None
    
    price=get_attr(soup,"value",id="priceValue")
    price=float(price) if price else None
    #print(f"Title: {title}")
    #print(f"Price: {price}")
    #print(f"Ratings: {rating}")
    
    return ProductDetails(title,price,rating)
    #title=soup.find(id="productTitle").text
   #price=soup.find(id="priceValue")["value"]    
   #ratings=soup.find(id="averageCustomerReviews").text
   #ratings=ratings.split()[0]