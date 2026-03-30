import streamlit as st
import asyncio
from scraper.amazon import parse_product
from utils.retry import retry_async
from scraper.fetcher import fetch_html
from services.price_tracker import track_price
from database.db import create_table
from database.db import get_all_products
import pandas as pd

# =========================
#  SETUP
# =========================
st.set_page_config(page_title="Price Tracker", layout="wide")
st.markdown("## 📦 Price Tracker Dashboard")
st.caption("Track Amazon product prices with alerts")

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
            try:

                html = asyncio.run(retry_async(fetch_html,url))

                product = parse_product(html)
              
                track_price(product, url)

                st.success(f"Tracking: {product.title}")
                st.write(f"Price: ₹{product.price}")
            except Exception as e:
                st.error(f"Error:{e}")

# =========================
# TABLE SECTION
# =========================
st.markdown("### 📊 Tracked Products")

products =get_all_products()

if products:
    df=pd.DataFrame(products,columns=["URL","Title","Price","Last Updated"])
   
    st.dataframe(df,
                 width="stretch",
                 hide_index=True,
                 column_config={
                   "URL": st.column_config.LinkColumn("Product Link")
                     }
                 )
else:
    st.info("No products tracked yet")
    
# =========================
# ▶RUN TRACKER SECTION
# =========================    
st.markdown("### ▶️ Run Tracker")
run_btn = st.button("Run Tracker for All Products")
if run_btn:
    st.info("Running Tracker...")
    products=get_all_products()
    products=list(set(products))
    for p in products:
        url=p.url
        try:

            html = asyncio.run(retry_async(fetch_html,url))

            product = parse_product(html)
            
            track_price(product, url)

            st.success(f"Tracking: {product.title}")
            st.write(f"Price: ₹{product.price}")
        except Exception as e:
            st.error(f"Error:{e}")
    st.success("Done!")