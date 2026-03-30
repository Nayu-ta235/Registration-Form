import streamlit as st
import pandas as pd
from datetime import datetime
import re

# Page configuration
st.set_page_config(page_title="Registration Form", page_icon="📝", layout="centered")

# Title
st.title("📝 User Registration Form")
st.markdown("Please fill in the details below to register")

# Create form
with st.form("registration_form"):
    # Personal Information
    st.subheader("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name *", placeholder="Enter your first name")
        email = st.text_input("Email Address *", placeholder="your@email.com")
        phone = st.text_input("Phone Number", placeholder="+1234567890")
        
    with col2:
        last_name = st.text_input("Last Name *", placeholder="Enter your last name")
        dob = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1), 
                           max_value=datetime.now())
        gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other", "Prefer not to say"])
    
    # Account Information
    st.subheader("Account Information")
    
    username = st.text_input("Username *", placeholder="Choose a username")
    password = st.text_input("Password *", type="password", placeholder="Enter your password")
    confirm_password = st.text_input("Confirm Password *", type="password", 
                                     placeholder="Confirm your password")
    
    # Address Information
    st.subheader("Address Information")
    
    address = st.text_area("Address", placeholder="Enter your full address")
    
    col3, col4 = st.columns(2)
    
    with col3:
        city = st.text_input("City", placeholder="City")
        country = st.selectbox("Country", ["Select Country", "USA", "UK", "Canada", "Australia", 
                                           "India", "Germany", "France", "Other"])
    
    with col4:
        state = st.text_input("State/Province", placeholder="State/Province")
        zip_code = st.text_input("ZIP/Postal Code", placeholder="ZIP Code")
    
    # Preferences
    st.subheader("Preferences")
    
    newsletter = st.checkbox("Subscribe to newsletter")
    terms = st.checkbox("I agree to the Terms and Conditions *")
    
    # Submit button
    submitted = st.form_submit_button("Register")
    
    # Form validation
    if submitted:
        errors = []
        
        # Validation checks
        if not first_name:
            errors.append("First name is required")
        if not last_name:
            errors.append("Last name is required")
        if not username:
            errors.append("Username is required")
        if not email:
            errors.append("Email is required")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errors.append("Please enter a valid email address")
        if not password:
            errors.append("Password is required")
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters")
        if password != confirm_password:
            errors.append("Passwords do not match")
        if not terms:
            errors.append("You must agree to the Terms and Conditions")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Process successful registration
            st.success("✅ Registration successful!")
            
            # Display registration summary
            with st.expander("Registration Summary"):
                st.write(f"**Name:** {first_name} {last_name}")
                st.write(f"**Username:** {username}")
                st.write(f"**Email:** {email}")
                st.write(f"**Phone:** {phone if phone else 'Not provided'}")
                st.write(f"**Date of Birth:** {dob.strftime('%Y-%m-%d')}")
                st.write(f"**Gender:** {gender if gender != 'Select' else 'Not provided'}")
                st.write(f"**Address:** {address if address else 'Not provided'}")
                st.write(f"**City:** {city if city else 'Not provided'}")
                st.write(f"**State:** {state if state else 'Not provided'}")
                st.write(f"**Country:** {country if country != 'Select Country' else 'Not provided'}")
                st.write(f"**ZIP Code:** {zip_code if zip_code else 'Not provided'}")
                st.write(f"**Newsletter:** {'Yes' if newsletter else 'No'}")
            
            # Save data to CSV (optional)
            save_data = st.button("Save to Database")
            if save_data:
                save_registration_data(first_name, last_name, username, email, phone, 
                                      dob, gender, address, city, state, country, 
                                      zip_code, newsletter)

# Function to save registration data
def save_registration_data(first_name, last_name, username, email, phone