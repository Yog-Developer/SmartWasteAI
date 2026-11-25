
import streamlit as st
import pandas as pd
import time
from datetime import date, timedelta, datetime

from ai_engine import (
    analyse_inventory,
    get_summary,
    generate_advice
)

# Page configuration
st.set_page_config(
    page_title="SmartWaste AI",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state
if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "results" not in st.session_state:
    st.session_state.results = {}

if "test_logs" not in st.session_state:
    st.session_state.test_logs = []


# Application heading
st.title("🌱 SmartWaste AI")
st.subheader("Intelligent Restaurant Inventory Management")

st.write(
    "Manage ingredients, identify items nearing expiry "
    "and generate AI-powered food waste reduction suggestions."
)

st.caption("Powered by Microsoft Azure and GPT-5 mini")

st.divider()


# Sidebar
with st.sidebar:
    st.header("Add Ingredient")

    with st.form("ingredient_form", clear_on_submit=True):

        name = st.text_input("Ingredient Name")

        quantity = st.number_input(
            "Quantity",
            min_value=0.01,
            value=1.0,
            step=0.5
        )

        unit = st.selectbox(
            "Unit",
            ["kg", "grams", "litres", "pieces"]
        )

        expiry = st.date_input("Expiry Date")

        submitted = st.form_submit_button(
            "Add Ingredient",
            use_container_width=True
        )

        if submitted:
            if not name.strip():
                st.error("Please enter an ingredient name.")
            else:
                st.session_state.inventory.append({
                    "name": name.strip(),
                    "quantity": quantity,
                    "unit": unit,
                    "expiry": str(expiry)
                })

                st.session_state.results = {}
                st.success("Ingredient added successfully.")

    st.divider()

    # Fictional demonstration dataset
    if st.button("Load Sample Inventory",
                 use_container_width=True):

        today = date.today()

        st.session_state.inventory = [
            {
                "name": "Tomatoes",
                "quantity": 2,
                "unit": "kg",
                "expiry": str(today + timedelta(days=1))
            },
            {
                "name": "Paneer",
                "quantity": 1,
                "unit": "kg",
                "expiry": str(today)
            },
            {
                "name": "Rice",
                "quantity": 5,
                "unit": "kg",
                "expiry": str(today + timedelta(days=15))
            },
            {
                "name": "Potatoes",
                "quantity": 3,
                "unit": "kg",
                "expiry": str(today + timedelta(days=7))
            },
            {
                "name": "Milk",
                "quantity": 2,
                "unit": "litres",
                "expiry": str(today - timedelta(days=1))
            },
            {
                "name": "Spinach",
                "quantity": 1.5,
                "unit": "kg",
                "expiry": str(today + timedelta(days=2))
            }
        ]

        st.session_state.results = {}
        st.success("Fictional sample inventory loaded.")

    if st.button("Clear Inventory",
                 use_container_width=True):

        st.session_state.inventory = []
        st.session_state.results = {}

    st.caption(
        "Inventory is stored temporarily for the current session."
    )


# Analyse inventory
inventory = analyse_inventory(
    st.session_state.inventory
)

summary = get_summary(inventory)


# Dashboard metrics
st.header("Inventory Overview")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Entries", summary["total"])
c2.metric("OK", summary["ok"])
c3.metric("Use Soon", summary["use_soon"])
c4.metric("Use Today", summary["use_today"])
c5.metric("Expired", summary["expired"])


# Inventory table
st.divider()
st.header("Ingredient Inventory")

if inventory:

    df = pd.DataFrame(inventory)

    df = df[
        [
            "name",
            "quantity",
            "unit",
            "expiry",
            "days_left",
            "status"
        ]
    ]

    df.columns = [
        "Ingredient",
        "Quantity",
        "Unit",
        "Expiry Date",
        "Days Left",
        "Status"
    ]

    # Apply expiry status colours
    def colour_status(value):
        colours = {
            "Expired": "#dc2626",
            "Use today": "#ea580c",
            "Use soon": "#ca8a04",
            "OK": "#16a34a"
        }

        return (
            f"color: {colours.get(value, '')};"
            "font-weight: bold"
        )

    st.dataframe(
        df.style.applymap(
            colour_status,
            subset=["Status"]
        ) if not hasattr(df.style, "map")
        else df.style.map(
            colour_status,
            subset=["Status"]
        ),
        use_container_width=True,
        hide_index=True
    )

    # Download inventory dataset
    st.download_button(
        "Download Inventory CSV",
        data=df.to_csv(index=False),
        file_name="smartwaste_inventory.csv",
        mime="text/csv"
    )

    # Delete ingredient
    selected = st.selectbox(
        "Select an ingredient to remove",
        options=list(range(len(inventory))),
        format_func=lambda i: (
            f"{inventory[i]['name']} - "
            f"{inventory[i]['quantity']} "
            f"{inventory[i]['unit']}"
        )
    )

    if st.button("Remove Selected Ingredient"):
        st.session_state.inventory.pop(selected)
        st.session_state.results = {}
        st.rerun()

else:
    st.info(
        "Add ingredients using the sidebar or "
        "load the sample inventory."
    )


# Expiry alerts
if summary["expired"] > 0:
    st.error(
        f"{summary['expired']} expired inventory entries. "
        "Do not use expired ingredients."
    )

if summary["use_today"] + summary["use_soon"] > 0:
    st.warning(
        "Some ingredients are nearing expiry. "
        "Review and prioritise them only if safe to use."
    )


# AI features
st.divider()
st.header("AI-Powered Assistant")


def run_ai(task):

    start = time.perf_counter()
    success = False

    try:
        with st.spinner("Generating recommendations..."):

            result = generate_advice(
                st.session_state.inventory,
                task
            )

        st.session_state.results[task] = result
        success = True

    except Exception as e:

        st.session_state.results.pop(task, None)

        st.error(
            f"AI request failed: {type(e).__name__}. "
            "Check the Azure configuration and connectivity."
        )

    elapsed = round(time.perf_counter() - start, 2)

    st.session_state.test_logs.append({
        "timestamp": datetime.now().isoformat(),
        "feature": task,
        "response_time_seconds": elapsed,
        "success": success
    })


tab1, tab2, tab3 = st.tabs([
    "🍽️ AI Recipe Generator",
    "♻️ Waste Reduction",
    "📋 Daily Inventory Report"
])

usable_count = summary["total"] - summary["expired"]


with tab1:

    st.write(
        "Generate recipe ideas using available "
        "non-expired ingredients."
    )

    if st.button(
        "Generate Recipes",
        disabled=usable_count == 0
    ):
        run_ai("recipes")

    if "recipes" in st.session_state.results:
        st.markdown(st.session_state.results["recipes"])


with tab2:

    st.write(
        "Get practical recommendations for ingredients "
        "nearing expiry."
    )

    if st.button(
        "Generate Waste Reduction Suggestions",
        disabled=usable_count == 0
    ):
        run_ai("waste")

    if "waste" in st.session_state.results:
        st.markdown(st.session_state.results["waste"])


with tab3:

    st.write(
        "Generate a daily inventory report with "
        "priorities and recommended actions."
    )

    expired_names = [
        item["name"] for item in inventory
        if item["status"] == "Expired"
    ]

    if expired_names:
        st.write(
            "**Expired ingredients:** "
            + ", ".join(expired_names)
        )

    if st.button(
        "Generate Daily Report",
        disabled=not inventory
    ):
        run_ai("report")

    if "report" in st.session_state.results:
        st.markdown(st.session_state.results["report"])


# Testing and performance metrics
st.divider()

with st.expander("Application Performance & Testing"):

    if st.session_state.test_logs:

        logs = pd.DataFrame(
            st.session_state.test_logs
        )

        m1, m2, m3 = st.columns(3)

        m1.metric("AI Requests", len(logs))

        m2.metric(
            "Average Response Time",
            f"{logs['response_time_seconds'].mean():.2f} s"
        )

        m3.metric(
            "AI Success Rate",
            f"{logs['success'].mean() * 100:.1f}%"
        )

        st.dataframe(
            logs,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Test Results",
            data=logs.to_csv(index=False),
            file_name="smartwaste_test_results.csv",
            mime="text/csv"
        )

    else:
        st.info("No AI requests have been recorded yet.")


# Disclaimer
st.divider()

st.caption(
    "Academic prototype using fictional demonstration data. "
    "Expiry dates are user-entered. This application is not "
    "a food-safety verification system. Never consume spoiled "
    "or expired food. AI recommendations require human review."
)
