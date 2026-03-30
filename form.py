import streamlit as st
import pandas as pd
import re
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Registration System",
    page_icon="📝",
    layout="centered"
)

# Title
st.title("📝 User Registration System")
st.markdown("---")

# Initialize session state for storing data
if 'registered_users' not in st.session_state:
    st.session_state.registered_users = []

# Form validation functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def validate_phone(phone):
    pattern = r'^[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{4}$'
    return re.match(pattern, phone) if phone else True

# Create form
with st.form("registration_form", clear_on_submit=False):
    st.subheader("👤 Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name *", placeholder="Enter your first name")
        email = st.text_input("Email Address *", placeholder="example@email.com")
        phone = st.text_input("Phone Number", placeholder="+1234567890")
        
    with col2:
        last_name = st.text_input("Last Name *", placeholder="Enter your last name")
        dob = st.date_input("Date of Birth", min_value=datetime(1950, 1, 1), 
                           max_value=datetime.now())
        gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
    
    st.markdown("---")
    st.subheader("🔐 Account Information")
    
    col3, col4 = st.columns(2)
    
    with col3:
        username = st.text_input("Username *", placeholder="Choose a username")
        password = st.text_input("Password *", type="password", placeholder="Minimum 6 characters")
        
    with col4:
        user_type = st.selectbox(
            "User Type *",
            ["Select Type", "Student", "Professional", "Business", "Individual"]
        )
        confirm_password = st.text_input("Confirm Password *", type="password", 
                                        placeholder="Confirm your password")
    
    st.markdown("---")
    st.subheader("📍 Address Information")
    
    address = st.text_area("Address", placeholder="Enter your full address", height=100)
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        city = st.text_input("City", placeholder="City")
    with col6:
        state = st.text_input("State/Province", placeholder="State")
    with col7:
        zip_code = st.text_input("ZIP Code", placeholder="ZIP Code")
    
    country = st.selectbox(
        "Country",
        ["Select Country", "United States", "Canada", "United Kingdom", 
         "Australia", "India", "Germany", "France", "Other"]
    )
    
    st.markdown("---")
    st.subheader("📧 Preferences")
    
    col8, col9 = st.columns(2)
    
    with col8:
        newsletter = st.checkbox("Subscribe to newsletter")
        updates = st.checkbox("Receive product updates")
        
    with col9:
        terms = st.checkbox("I agree to the Terms and Conditions *")
        privacy = st.checkbox("I accept the Privacy Policy *")
    
    # Submit button
    submitted = st.form_submit_button("Register Now", use_container_width=True)
    
    # Process form
    if submitted:
        # Validation
        errors = []
        
        if not first_name:
            errors.append("First name is required")
        if not last_name:
            errors.append("Last name is required")
        if not username:
            errors.append("Username is required")
        if not email:
            errors.append("Email is required")
        elif not validate_email(email):
            errors.append("Please enter a valid email address")
        if not password:
            errors.append("Password is required")
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters")
        if password != confirm_password:
            errors.append("Passwords do not match")
        if user_type == "Select Type":
            errors.append("Please select a user type")
        if not terms or not privacy:
            errors.append("You must agree to Terms and Privacy Policy")
        if not validate_phone(phone):
            errors.append("Please enter a valid phone number")
        
        # Check for duplicate username
        for user in st.session_state.registered_users:
            if user['username'] == username:
                errors.append("Username already exists")
                break
        
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            # Save user data
            user_data = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'user_type': user_type,
                'phone': phone if phone else "Not provided",
                'dob': dob.strftime("%Y-%m-%d"),
                'gender': gender,
                'address': address if address else "Not provided",
                'city': city if city else "Not provided",
                'state': state if state else "Not provided",
                'zip_code': zip_code if zip_code else "Not provided",
                'country': country if country != "Select Country" else "Not provided",
                'newsletter': newsletter,
                'updates': updates,
                'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            st.session_state.registered_users.append(user_data)
            
            # Success message
            st.balloons()
            st.success(f"✅ Registration Successful! Welcome {first_name} {last_name}!")
            
            # Show registration summary
            with st.expander("📋 View Registration Summary"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Personal Info:**")
                    st.write(f"• Name: {first_name} {last_name}")
                    st.write(f"• Email: {email}")
                    st.write(f"• Phone: {phone if phone else 'Not provided'}")
                    st.write(f"• DOB: {dob.strftime('%Y-%m-%d')}")
                    st.write(f"• Gender: {gender}")
                    
                with col_b:
                    st.write("**Account Info:**")
                    st.write(f"• Username: {username}")
                    st.write(f"• User Type: {user_type}")
                    st.write(f"• Newsletter: {'Yes' if newsletter else 'No'}")
                    st.write(f"• Updates: {'Yes' if updates else 'No'}")
                
                st.write("**Address:**")
                st.write(f"{address if address else 'Not provided'}")
                st.write(f"{city}, {state} {zip_code}")
                st.write(f"{country if country != 'Select Country' else 'Not provided'}")

# Display registered users in sidebar
with st.sidebar:
    st.header("📊 Dashboard")
    st.metric("Total Registered Users", len(st.session_state.registered_users))
    
    if st.session_state.registered_users:
        st.markdown("---")
        st.subheader("Recent Users")
        for user in st.session_state.registered_users[-5:]:
            st.write(f"• {user['first_name']} {user['last_name']}")
            st.caption(f"  {user['user_type']} | {user['registration_date']}")
    
    st.markdown("---")
    if st.button("📥 Export Data", use_container_width=True):
        if st.session_state.registered_users:
            df = pd.DataFrame(st.session_state.registered_users)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="registered_users.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data to export")
    
    if st.button("🗑️ Clear All Data", use_container_width=True):
        st.session_state.registered_users = []
        st.success("All data cleared!")
        st.rerun()

# Footer
st.markdown("---")
st.markdown("© 2024 Registration System | All rights reserved")