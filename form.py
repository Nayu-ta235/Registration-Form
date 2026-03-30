import streamlit as st

# Page title
st.title("Registration Form")

# Create form
with st.form("register_form"):
    st.write("### Please register")
    
    # Input fields
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    
    # Checkbox
    agree = st.checkbox("I agree to the terms")
    
    # Submit button
    submit = st.form_submit_button("Register")
    
    # What happens when submitted
    if submit:
        if name and email and password and agree:
            st.success(f"Welcome {name}! You're now registered.")
            st.info(f"We'll send updates to {email}")
        else:
            st.error("Please fill all fields and agree to terms")