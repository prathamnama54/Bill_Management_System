import streamlit as st

# Set Page Title and Configuration
st.set_page_config(page_title="Billing Management System", layout="wide")

st.title("🍔 Billing Management System")

# ===================== Prices Configuration ===================
PRICES = {
    "Pizza": 149,
    "Burger": 79,
    "Patties": 35,
    "Cold Coffee": 49
}

# Use Streamlit Session State to persist the generated receipt layout
if "receipt_text" not in st.session_state:
    st.session_state.receipt_text = ""

# Layout: Split page into 2 interactive columns
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🛒 Product Details")
    
    # Input section mimicking your table grid
    # Users can change quantities directly with numerical plus/minus selectors
    pizza_qty = st.number_input("Pizza Quantity (₹149/each)", min_value=0, value=0, step=1)
    burger_qty = st.number_input("Burger Quantity (₹79/each)", min_value=0, value=0, step=1)
    patties_qty = st.number_input("Patties Quantity (₹35/each)", min_value=0, value=0, step=1)
    coffee_qty = st.number_input("Cold Coffee Quantity (₹49/each)", min_value=0, value=0, step=1)

    st.markdown("---")
    
    # Live Subtotal Display before printing receipts
    t_pizza = pizza_qty * PRICES["Pizza"]
    t_burger = burger_qty * PRICES["Burger"]
    t_patties = patties_qty * PRICES["Patties"]
    t_coffee = coffee_qty * PRICES["Cold Coffee"]
    
    total_items = pizza_qty + burger_qty + patties_qty + coffee_qty
    total_cash = t_pizza + t_burger + t_patties + t_coffee

    # Display real-time costs right inside your input panel
    st.subheader("💰 Live Item Cost Summary")
    st.write(f"**Pizza Cost:** ₹{t_pizza}")
    st.write(f"**Burger Cost:** ₹{t_burger}")
    st.write(f"**Patties Cost:** ₹{t_patties}")
    st.write(f"**Cold Coffee Cost:** ₹{t_coffee}")
    st.write(f"### **Total Amount:** ₹{total_cash:.2f}")

    # Action Buttons Panel
    st.subheader("⚙️ Control Panel")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    with btn_col1:
        if st.button("📄 Generate Receipt", use_container_width=True, type="primary"):
            if total_items == 0:
                st.error("Error: Please select number of quantity first!")
            else:
                # Formatting textual receipt like your legacy text area
                receipt = " Items\t\tQty\tCost\n"
                receipt += "=" * 35 + "\n"
                
                if pizza_qty > 0:
                    receipt += f"Pizza\t\t{pizza_qty}\t₹ {t_pizza}\n"
                if burger_qty > 0:
                    receipt += f"Burger\t\t{burger_qty}\t₹ {t_burger}\n"
                if patties_qty > 0:
                    receipt += f"Patties\t\t{patties_qty}\t₹ {t_patties}\n"
                if coffee_qty > 0:
                    receipt += f"Coffee\t\t{coffee_qty}\t₹ {t_coffee}\n"
                    
                receipt += "\n" + "=" * 35
                receipt += f"\nTotal Items:\t{total_items}"
                receipt += f"\nTotal Price:\t\t₹ {total_cash:.2f}"
                receipt += "\n" + "=" * 35
                
                st.session_state.receipt_text = receipt
                st.toast("Receipt Generated!", icon="✅")

    with btn_col2:
        if st.button("🔄 Reset Fields", use_container_width=True):
            st.session_state.receipt_text = ""
            # Streamlit resets numerical form states globally when page component reruns
            st.rerun()

    with btn_col3:
        # Web platforms do not have access to client local printers for safety.
        # Added a download button so the user can save the text bill instead!
        if st.session_state.receipt_text:
            st.download_button(
                label="💾 Save/Download Bill",
                data=st.session_state.receipt_text,
                file_name="bill_receipt.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.button("💾 Save/Download Bill", disabled=True, use_container_width=True)

with col2:
    st.header("📋 Receipt Preview")
    if st.session_state.receipt_text:
        # Preformatted block displays tabular layout cleanly without alignment breakage
        st.code(st.session_state.receipt_text, language="text")
    else:
        st.info("Your generated bill receipt output will show up right here.")
