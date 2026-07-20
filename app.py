import streamlit as st
import asyncio
from scraper.amazon import parse_product
from utils.retry import retry_async
from scraper.fetcher import fetch_html
from services.price_tracker import track_price
from database.db import create_table
from database.db import get_all_products, delete_product
import pandas as pd
import traceback
import logging


# =========================
#  SETUP
# =========================
st.set_page_config(page_title="Price Tracker", layout="wide")
st.markdown("## 📦 Price Tracker Dashboard")
st.caption("Track Amazon product prices with alerts")
logging.basicConfig(level=logging.INFO)

create_table()

# =========================
# ADD PRODUCT SECTION
# =========================
col1, col2 = st.columns([4, 1])

with col1:
    url = st.text_input("Enter Product URL")

with col2:
    st.write("")
    st.write("")
    track_btn = st.button("➕ Track")


if track_btn:
    # st.success("Product Added")
    if url:
        with st.spinner("Fetching Product...."):
            logging.info("Fetching product")
            try:

                html = asyncio.run(retry_async(fetch_html, 3, 2, url))

                product = parse_product(html)

                track_price(product, url)

                st.success(f"Tracking: {product.title}")
                st.write(f"Price: ₹{product.price}")
            except Exception as e:
                st.error(f"Error:{e}")
                st.text(traceback.format_exc())

# =========================
# TABLE SECTION
# =========================
st.markdown("### 📊 Tracked Products")

products = get_all_products()

if products:
    
    df = pd.DataFrame(
    products,
    columns=["Product ID", "URL", "Title", "Price", "Status", "Last Updated"]
    )
    df["Delete"] = False

    grouped = df.groupby("Product ID")
    for product_id, group in grouped:
        group = group.sort_values("Last Updated", ascending=False)
        latest = group.iloc[0]

        with st.container():
            st.markdown(f"### 📦 {latest['Title']}")
            st.markdown(f"🔗 [Open Product]({latest['URL']})")

            status = latest["Status"]
            price = latest["Price"]

            if status == "DOWN":
                st.success(f"⬇️ Price Dropped: ₹{price}")
            elif status == "UP":
                st.error(f"⬆️ Price Increased: ₹{price}")
            else:
                st.info(f"➖ No Change: ₹{price}")

            chart_df = group.sort_values("Last Updated")
            st.line_chart(chart_df.set_index("Last Updated")["Price"])

            if st.button(f"🗑 Delete", key=f"del_{product_id}"):
                delete_product(latest["URL"])
                st.rerun()

            st.divider()
        
else:
    st.info("No products tracked yet")

# =========================
# ▶RUN TRACKER SECTION
# =========================
st.markdown("### ▶️ Run Tracker")
run_btn = st.button("Run Tracker for All Products")
if run_btn:
    st.info("Running Tracker...")
    products = get_all_products()
    unique_products = {}
    for p in products:
        url = p[1]  # Fist Value
        unique_products[url] = p
    products = list(unique_products.values())
    for p in products:
        url = p[1]
        try:

            html = asyncio.run(retry_async(fetch_html, 3, 2, url))

            product = parse_product(html)

            track_price(product, url)

            st.success(f"Tracking: {product.title}")
            st.write(f"Price: ₹{product.price}")
        except Exception as e:
            st.error(f"Error:{e}")
            st.text(traceback.format_exc())
    st.success("Done!")
