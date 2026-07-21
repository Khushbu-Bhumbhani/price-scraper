from models.products import ProductDetails
from database.db import get_or_create_product
from database.db import get_last_price
from services.email_service import send_email
from database.db import save_price_history
import logging

logger = logging.getLogger(__name__)

def track_price(product: ProductDetails, url: str):
    product_id = get_or_create_product(url, product.title)
    latest_price = get_last_price(product_id)
    status = "first_time"
    change_percent = "0.0"
    if latest_price is not None:
        if product.price < latest_price:
            status = "dropped"
            change_percent = ((latest_price - product.price) / latest_price) * 100
            send_email(
                    subject="🔥 Price Drop",
                    body=f"""
                    🔥 Price Drop
                    
                    {product.title}
                    
                    Old Price: ₹{latest_price}
                    New Price: ₹{product.price}
                    Change Percent: {change_percent:.2f}%
                    Link: {url}
                    """,
                )
            logger.info("Price dropped for '%s': ₹%.2f -> ₹%.2f",
            product.title,
            latest_price,
            product.price)
        elif product.price > latest_price:  
            status = "increased"
            change_percent = ((product.price - latest_price) / latest_price) * 100
            
            send_email(
                    subject=f"📈 Price increased: {product.title[:50]}",
                    body=f"""
                    📈 Price increased!
                    
                    {product.title}
                    
                    Old Price: ₹{latest_price}
                    New Price: ₹{product.price}
                    Drop Percent: {change_percent:.2f}%
                    Link: {url}
                    """,
                )
            logger.info("Price increased for '%s': ₹%.2f -> ₹%.2f",
            product.title,
            latest_price,
            product.price)
        else:
            status = "no_change"
            logger.info("No price change for '%s'", product.title)
    else:
        logger.info("Started tracking '%s'", product.title)
        
    
    # Always set the calculated tracking status before saving

    product.status=status
    save_price_history(product_id, product)
    return {
        "status": status,
        "old_price": latest_price,
        "new_price": product.price,
        "change_percent": change_percent,
    }
