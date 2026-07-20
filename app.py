import streamlit as st
import asyncio
from scraper.amazon_parser import parse_product
from utils.retry import retry_async
from scraper.fetcher import fetch_html
from services.price_tracker import track_price
from database.db import create_table
from database.db import get_all_products, delete_product
import pandas as pd
import traceback
import logging
from datetime import datetime



# =========================
#  SETUP
# =========================
st.set_page_config(page_title="Price Tracker", layout="wide")
st.title("📦 Price Tracker Dashboard")
st.caption("Monitor Amazon product prices and receive alerts when prices change.")
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
                #st.write(get_all_products())
                st.success("✅ Product added successfully!")

                col1, col2 = st.columns([5, 1])

                with col1:
                  st.markdown(f"**{product.title}**")

                with col2:
                    st.metric("Current Price", f"₹{product.price:,.0f}")
                st.write(f"Price: ₹{product.price}")
            except Exception as e:
                st.error(f"Error:{e}")
                st.text(traceback.format_exc())

# =========================
# TABLE SECTION
# =========================
st.markdown("## 📈 Tracked Products")
st.caption("Monitor price history for all tracked products.")

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
        dt = datetime.fromisoformat(latest["Last Updated"])

        with st.container(border=True):

            col1, col2 = st.columns([6,1])

            with col1:
                title = latest["Title"]

                if len(title) > 90:
                    title = title[:90] + "..."

                st.markdown(f"### 📦 {title}")
                st.markdown(f"🔗 [Open Product]({latest['URL']})")

            with col2:
                if st.button("🗑 Delete", key=f"del_{product_id}"):
                    delete_product(latest["URL"])
                    st.rerun()


            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Current Price", f"₹{latest['Price']:,.0f}")

            with c2:
                emoji = {
                    "dropped":"🟢",
                    "increased":"🔴",
                    "no_change":"🔵",
                    "same":"🔵"
                }.get(latest["Status"],"⚪")

                st.metric("Status", f"{emoji} {latest['Status'].replace('_',' ').title()}")

            with c3:
                st.metric("Last Checked",  dt.strftime("%d %b %I:%M %p")[:16])

            chart_df = group.sort_values("Last Updated")

            if len(chart_df) > 1:
                st.line_chart(
                    chart_df.set_index("Last Updated")["Price"],
                    height=220
                )
            else:
                st.info("Track this product again to build price history.")
        
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
           # st.write(get_all_products())
            st.success("✅ Product added successfully!")

            col1, col2 = st.columns([5, 1])

            with col1:
                st.markdown(f"**{product.title}**")

            with col2:
                st.metric("Current Price", f"₹{product.price:,.0f}")
            st.write(f"Price: ₹{product.price}")
        except Exception as e:
            st.error(f"Error:{e}")
            st.text(traceback.format_exc())
    st.success("Done!")
