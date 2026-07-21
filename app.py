import streamlit as st
import asyncio
from scraper.amazon_parser import parse_product
from utils.retry import retry_async
from scraper.fetcher import fetch_html
from services.price_tracker import track_price
from database.db import create_table
from database.db import get_all_products, delete_product
import pandas as pd
from datetime import datetime
from utils.logger import setup_logger
import logging

# =========================
#  SETUP
# =========================
setup_logger()
logger = logging.getLogger(__name__)
st.set_page_config(page_title="Price Tracker", layout="wide")
st.title("📦 Price Tracker Dashboard")
st.caption("Monitor Amazon product prices and receive alerts when prices change.")

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
            logger.info("Fetching product: %s", url)
            try:

                html = asyncio.run(retry_async(fetch_html, 3, 2, url))

                product = parse_product(html)
                if product.price is None:
                    st.warning(f"⚠️ Could not fetch price for: {product.title or url}")
                    logger.warning(
                        "Price unavailable for '%s'",
                        product.title or url,
                    )
                else:
                    track_price(product, url)
                    # st.write(get_all_products())
                    st.success("✅ Product added successfully!")
                    logger.info("Product added successfully '%s'", product.title)

                    col1, col2 = st.columns([5, 1])

                    with col1:
                        st.markdown(f"**{product.title}**")

                    with col2:
                        st.metric("Current Price", f"₹{product.price:,.0f}")
                #  st.write(f"Price: ₹{product.price}")
            except Exception as e:
                st.error("Failed to track product")
                # st.text(traceback.format_exc())
                logger.exception(f"Error:{e}")

# =========================
# TABLE SECTION
# =========================
st.markdown("## 📈 Tracked Products")
st.caption("Monitor price history for all tracked products.")

products = get_all_products()

if products:

    df = pd.DataFrame(
        products,
        columns=["Product ID", "URL", "Title", "Price", "Status", "Last Updated"],
    )
    df["Delete"] = False

    grouped = df.groupby("Product ID", sort=False)
    for product_id, group in grouped:
        group = group.sort_values("Last Updated", ascending=False)
        latest = group.iloc[0]
        dt = datetime.fromisoformat(latest["Last Updated"])

        with st.container(border=True):

            col1, col2, col3 = st.columns([6, 1.2, 1])

            with col1:
                title = latest["Title"]

                if len(title) > 65:
                    title = title[:65] + "..."

                st.markdown(f"#### 📦 {title}")

            with col2:
                st.markdown(f"🔗 [Open Product]({latest['URL']})")

            with col3:
                if st.button("🗑 Delete", key=f"del_{product_id}"):
                    logger.info("Deleting product: %s", latest["Title"])
                    delete_product(latest["URL"])
                    st.rerun()

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Current Price", f"₹{latest['Price']:,.0f}")

            with c2:
                emoji = {
                    "dropped": "🟢",
                    "increased": "🔴",
                    "no_change": "🔵",
                    "same": "🔵",
                }.get(latest["Status"], "⚪")

                st.metric(
                    "Status", f"{emoji} {latest['Status'].replace('_',' ').title()}"
                )

            with c3:
                st.metric("Last Checked", dt.strftime("%d %b %I:%M %p")[:16])

            chart_df = group.copy()
            chart_df["Last Updated"] = pd.to_datetime(
                chart_df["Last Updated"], format="mixed"
            )
            chart_df = chart_df.sort_values("Last Updated", ascending=False)

            with st.expander("📜 View Price History"):

                history = chart_df[["Last Updated", "Price", "Status"]].copy()

                history["Last Updated"] = history["Last Updated"].dt.strftime(
                    "%d %b %Y %I:%M %p"
                )
                history["Price"] = history["Price"].apply(lambda x: f"₹{x:,.0f}")
                history["Status"] = history["Status"].str.replace("_", " ").str.title()
                history.rename(
                    columns={
                        "Last Updated": "Date",
                        "Price": "Price",
                        "Status": "Status",
                    },
                    inplace=True,
                )

                st.dataframe(history, width="stretch", hide_index=True)

else:
    st.info("No products tracked yet")

# =========================
# ▶RUN TRACKER SECTION
# =========================
st.markdown("### 🔄 Update Prices")

run_btn = st.button("Update All Tracked Products")

if run_btn:

    products = get_all_products()

    # Keep only one record per product URL
    unique_products = {}

    for p in products:
        url = p[1]
        unique_products[url] = p

    products = list(unique_products.values())

    progress_bar = st.progress(0)
    status_text = st.empty()

    total = len(products)
    updated = 0
    unavailable = 0
    logger.info("Updating %d tracked products", total)
    for index, p in enumerate(products):

        url = p[1]
        logger.info("Checking latest price for %s", url)
        status_text.write(f"Checking latest price for product {index + 1} of {total}...")

        try:
            html = asyncio.run(retry_async(fetch_html, 3, 2, url))

            product = parse_product(html)

            if product.price is None:
                unavailable += 1
                st.warning(f"⚠️ Currently unavailable: {product.title or url}")
                logger.warning(
                    "Product unavailable: %s",
                    product.title or url,
                )
                continue

            track_price(product, url)
            logger.info(
                "Updated '%s' successfully",
                product.title,
            )
            updated += 1
        except Exception as e:
            logger.exception(f"⚠️ Could not update product: {e}")
            st.warning("Failed to update %s", url)

        finally:
            progress_bar.progress((index + 1) / total)

    status_text.success(
        f"✅ Update complete — {total} checked • "
        f"{updated} updated • {unavailable} unavailable"
    )
    logger.info(
        "Update completed: %d checked, %d updated, %d unavailable",
        total,
        updated,
        unavailable,
    )
    if st.button("Refresh Dashboard"):
        st.rerun()
