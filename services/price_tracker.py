from models.products import ProductDetails
from database.db import get_or_create_product
from database.db import get_last_price
from services.email_service import send_email
from database.db import save_price_history


def track_price(product: ProductDetails, url: str):
    product_id = get_or_create_product(url, product.title)
    latest_price = get_last_price(product_id)
    status = "same"
    change_percent = "0.0%"
    if latest_price is not None:
        if product.price < latest_price:
            print("🔥 PRICE DROPPED!")
            status = "dropped"
            change_percent = ((latest_price - product.price) / latest_price) * 100
            send_email(
                    subject="📈 Price increased",
                    body=f"""
                    📈 Price increased
                    
                    {product.title}
                    
                    Old Price: ₹{product.price}
                    New Price: ₹{latest_price}
                    Change Percent: {change_percent:.2f}%
                    Link: {url}
                    """,
                )
        elif product.price > latest_price:
            print("📈 Price increased")
            status = "increased"
            change_percent = ((product.price - latest_price) / latest_price) * 100
            
            send_email(
                    subject=f"🔥 Price Drop: {product.title[:50]}",
                    body=f"""
                    🔥 Price Dropped!
                    
                    {product.title}
                    
                    Old Price: ₹{product.price}
                    New Price: ₹{latest_price}
                    Drop Percent: {change_percent:.2f}%
                    Link: {url}
                    """,
                )
        else:
            print("Same Price")
            status = "no_change"
    else:
        print("First time tracking")
    product.status=status
    save_price_history(product_id, product)
    return {
        "status": status,
        "old_price": latest_price,
        "new_price": product.price,
        "change_percent": change_percent,
    }
