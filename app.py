import streamlit as st
import pandas as pd

# Set page title
st.set_page_config(page_title="Carbon Footprint Calculator", layout="wide")

# Title of the app
st.title("🌍 Carbon Footprint Calculator")
st.write("Calculate the carbon footprint of your shopping cart!")

# Load the CSV file
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('carbon_footprint_data.csv')
        return df
    except FileNotFoundError:
        st.error("Error: carbon_footprint_data.csv file not found! Make sure it's uploaded to your GitHub repository.")
        return None

# Load data
data = load_data()

# Only run the app if data loaded successfully
if data is not None:
    # Initialize shopping cart in session state (this keeps the cart between interactions)
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Add Items to Cart")
        
        # Dropdown to select item
        selected_item = st.selectbox(
            "Select an item:",
            options=data['item'].tolist()
        )
        
        # Input field for weight
        weight = st.number_input(
            "Enter weight (kg):",
            min_value=0.0,
            max_value=1000.0,
            value=1.0,
            step=0.1
        )
        
        # Add to cart button
        if st.button("Add to Cart", type="primary"):
            # Get the carbon footprint value for this item
            item_data = data[data['item'] == selected_item]
            kgco2e_per_kg = item_data['kgCO2e_per_kg'].values[0]
            
            # Calculate total carbon footprint for this item
            total_kgco2e = weight * kgco2e_per_kg
            
            # Add to cart
            st.session_state.cart.append({
                'Item': selected_item,
                'Weight (kg)': weight,
                'kgCO2e per kg': kgco2e_per_kg,
                'Total kgCO2e': round(total_kgco2e, 2)
            })
            
            st.success(f"Added {weight} kg of {selected_item} to cart!")
    
    with col2:
        st.subheader("Shopping Cart")
        
        # Display cart
        if len(st.session_state.cart) > 0:
            # Convert cart to DataFrame for nice display
            cart_df = pd.DataFrame(st.session_state.cart)
            
            # Display the table
            st.dataframe(cart_df, use_container_width=True)
            
            # Calculate and display total
            total_footprint = cart_df['Total kgCO2e'].sum()
            st.metric("Total Carbon Footprint", f"{total_footprint:.2f} kgCO2e")
            
            # Clear cart button
            if st.button("Clear Cart", type="secondary"):
                st.session_state.cart = []
                st.rerun()
        else:
            st.info("Your cart is empty. Add items from the left!")
    
    # Show full item database at the bottom
    st.divider()
    st.subheader("📊 Complete Item Database")
    st.dataframe(data, use_container_width=True)
