import streamlit as st
from datetime import datetime, timedelta

# Define the storage fee rates
storage_fees = {
    4: 5,   # Day 4
    5: 10,  # Day 5
    6: 15,  # Day 6
    7: 20,  # Day 7
    8: 25,  # Day 8
    9: 25,  # Day 9
    10: 30  # Day 10 and beyond
}

def calculate_storage_fee(purchase_date_str, supposed_pickup_date_str, actual_pickup_date_str):
    # Parse the dates from string to datetime
    purchase_date = datetime.strptime(purchase_date_str, '%m/%d/%Y')
    supposed_pickup_date = datetime.strptime(supposed_pickup_date_str, '%m/%d/%Y')
    actual_pickup_date = datetime.strptime(actual_pickup_date_str, '%m/%d/%Y')

    company_fee = 0
    driver_fee = 0
    
    # Calculate company's fee (days 4 to 10 up to supposed pick-up date)
    for day in range(4, 11):
        fee_day = purchase_date + timedelta(days=day-1)
        if fee_day <= supposed_pickup_date:
            company_fee += storage_fees.get(day, 30)
        else:
            break

    # Calculate driver's fee (days after supposed pick-up date)
    current_date = supposed_pickup_date + timedelta(days=1)
    while current_date <= actual_pickup_date:
        days_since_purchase = (current_date - purchase_date).days + 1  # +1 because purchase day is day 1
        fee = storage_fees.get(days_since_purchase, 30)  # Default $30 if day >10
        driver_fee += fee
        current_date += timedelta(days=1)
    
    return driver_fee, company_fee

# ... (rest of the Streamlit app code remains the same)


# Streamlit App UI
def main():
    # Set the page configuration with an icon
    st.set_page_config(
        page_title="Copart Storage Fee Calculator",
        page_icon="🚛",  # You can change this to a custom .ico or .png icon if you have one
        layout="centered"
    )

    st.title("Copart Storage Fee Calculator")
    st.markdown(""" 
    This simple app helps calculate the storage fee for cars based on the **Purchase Date**, **Supposed Pick-Up Date**, and **Actual Pick-Up Date**.
    - **3 days of free storage**.
    - After 3 days, charges apply according to the fee schedule below:
      - Day 4: $5
      - Day 5: $10
      - Day 6: $15
      - Day 7: $20
      - Day 8: $25
      - Day 9: $25
      - Day 10+: $30 per day
    """)

    # Input for purchase date using the calendar picker
    purchase_date = st.date_input("Select the Purchase Date", min_value=datetime(2000, 1, 1), max_value=datetime.today(), value=None)

    # Input for supposed pick-up date using the calendar picker
    supposed_pickup_date = st.date_input("Select the Supposed Pick-Up Date", min_value=purchase_date, max_value=datetime.today(), value=None)

    # Input for actual pick-up date using the calendar picker (must be on or after the supposed pick-up date)
    actual_pickup_date = st.date_input("Select the Actual Pick-Up Date", min_value=supposed_pickup_date, max_value=datetime.today(), value=None)

    # Add a "Calculate" button
    calculate_button = st.button("Calculate Storage Fees")

    if calculate_button:
        # Convert the selected dates into the correct string format
        purchase_date_str = purchase_date.strftime('%m/%d/%Y')
        supposed_pickup_date_str = supposed_pickup_date.strftime('%m/%d/%Y')
        actual_pickup_date_str = actual_pickup_date.strftime('%m/%d/%Y')  # Corrected this line

        # If the actual pick-up date is after the purchase date, calculate storage fees
        if actual_pickup_date >= purchase_date:
            driver_fee, company_fee = calculate_storage_fee(purchase_date_str, supposed_pickup_date_str, actual_pickup_date_str)

            # Display the results
            st.subheader(f"Storage Fee Calculation from {purchase_date_str} to {actual_pickup_date_str}")
            st.write(f"**Driver's Storage Fee** (for late pick-up after supposed date): ${driver_fee}")
            st.write(f"**Company's Storage Fee** (on Supposed Pick-Up Date): ${company_fee}")
            st.write(f"**Total Storage Fee** : ${company_fee + driver_fee}")
        else:
            st.error("Actual Pick-Up Date should be on or after the Purchase Date.")

if __name__ == "__main__":
    main()
