import streamlit as st
import pandas as pd
import re
import hashlib
import sqlite3
from datetime import datetime
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Registration System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-radius: 10px;
        border-left: 5px solid #28a745;
    }
    .error-box {
        padding: 20px;
        background-color: #f8d7da;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
def init_database():
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  first_name TEXT,
                  last_name TEXT,
                  email TEXT UNIQUE,
                  username TEXT UNIQUE,
                  password TEXT,
                  user_type TEXT,
                  phone TEXT,
                  company TEXT,
                  designation TEXT,
                  country TEXT,
                  interests TEXT,
                  created_at TIMESTAMP)''')
    conn.commit()
    conn.close()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Email validation
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Save to database
def save_user(data):
    try:
        conn = sqlite3.connect('registration.db')
        c = conn.cursor()
        c.execute('''INSERT INTO users 
                     (first_name, last_name, email, username, password, user_type, 
                      phone, company, designation, country, interests, created_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data['first_name'], data['last_name'], data['email'], 
                   data['username'], hash_password(data['password']), data['user_type'],
                   data['phone'], data['company'], data['designation'], 
                   data['country'], data['interests'], datetime.now()))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Main app
def main():
    # Header with logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🔐 Professional Registration System")
        st.markdown("---")

    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📝 Register", "📊 Statistics", "👥 View Users"])
    
    with tab1:
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Personal Information")
                first_name = st.text_input("First Name *", placeholder="John")
                last_name = st.text_input("Last Name *", placeholder="Doe")
                email = st.text_input("Email Address *", placeholder="john.doe@example.com")
                phone = st.text_input("Phone Number", placeholder="+1 234 567 8900")
                
            with col2:
                st.markdown("### Account Details")
                username = st.text_input("Username *", placeholder="johndoe123")
                password = st.text_input("Password *", type="password", 
                                        placeholder="Minimum 8 characters")
                confirm_password = st.text_input("Confirm Password *", type="password")
                
                user_type = st.selectbox(
                    "User Type *",
                    ["Select Type", "Individual", "Business", "Student", "Professional"]
                )
            
            st.markdown("---")
            st.markdown("### Professional Information")
            
            col3, col4 = st.columns(2)
            
            with col3:
                company = st.text_input("Company/Organization", placeholder="Company Name")
                designation = st.text_input("Designation", placeholder="Job Title")
                
            with col4:
                countries = ["Select Country", "United States", "United Kingdom", "Canada", 
                           "Australia", "Germany", "France", "India", "Singapore", "Other"]
                country = st.selectbox("Country", countries)
                
                interests = st.multiselect(
                    "Areas of Interest",
                    ["Technology", "Business", "Education", "Healthcare", 
                     "Finance", "Marketing", "Design", "Development"]
                )
            
            st.markdown("---")
            
            # Terms and conditions
            col5, col6 = st.columns([3, 1])
            with col5:
                terms = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
                newsletter = st.checkbox("Subscribe to newsletter for updates")
                
            with col6:
                submit = st.button("🚀 Register Now", use_container_width=True)
            
            # Form validation and submission
            if submit:
                errors = []
                
                # Validation
                if not first_name:
                    errors.append("First name is required")
                if not last_name:
                    errors.append("Last name is required")
                if not email:
                    errors.append("Email is required")
                elif not validate_email(email):
                    errors.append("Invalid email format")
                if not username:
                    errors.append("Username is required")
                if not password:
                    errors.append("Password is required")
                elif len(password) < 8:
                    errors.append("Password must be at least 8 characters")
                if password != confirm_password:
                    errors.append("Passwords do not match")
                if user_type == "Select Type":
                    errors.append("Please select user type")
                if not terms:
                    errors.append("You must agree to Terms of Service")
                
                if errors:
                    st.markdown('<div class="error-box">', unsafe_allow_html=True)
                    for error in errors:
                        st.error(f"❌ {error}")
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    # Prepare data
                    user_data = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'username': username,
                        'password': password,
                        'user_type': user_type,
                        'phone': phone,
                        'company': company if company else "N/A",
                        'designation': designation if designation else "N/A",
                        'country': country if country != "Select Country" else "Not Specified",
                        'interests': ", ".join(interests) if interests else "None"
                    }
                    
                    # Save to database
                    if save_user(user_data):
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.success("✅ Registration Successful!")
                        st.balloons()
                        st.info(f"Welcome {first_name} {last_name}! A confirmation email has been sent to {email}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Show registration summary
                        with st.expander("View Registration Summary"):
                            st.json(user_data)
                    else:
                        st.error("❌ Username or email already exists. Please try different credentials.")
    
    with tab2:
        st.markdown("### Registration Statistics")
        
        # Load data for statistics
        conn = sqlite3.connect('registration.db')
        df = pd.read_sql_query("SELECT user_type, country, created_at FROM users", conn)
        conn.close()
        
        if not df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # User type distribution
                type_counts = df['user_type'].value_counts()
                fig1 = px.pie(values=type_counts.values, names=type_counts.index, 
                             title="User Type Distribution")
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Country distribution
                country_counts = df['country'].value_counts().head(5)
                fig2 = px.bar(x=country_counts.values, y=country_counts.index, 
                             orientation='h', title="Top 5 Countries")
                st.plotly_chart(fig2, use_container_width=True)
            
            # Registration trends
            df['date'] = pd.to_datetime(df['created_at']).dt.date
            daily_counts = df.groupby('date').size().reset_index(name='count')
            fig3 = px.line(daily_counts, x='date', y='count', title="Registration Trends")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No data available yet. Be the first to register!")
    
    with tab3:
        st.markdown("### Registered Users")
        
        # Load and display users
        conn = sqlite3.connect('registration.db')
        users_df = pd.read_sql_query("SELECT id, first_name, last_name, email, username, user_type, country, created_at FROM users ORDER BY created_at DESC", conn)
        conn.close()
        
        if not users_df.empty:
            # Search functionality
            search = st.text_input("🔍 Search users by name or email", "")
            if search:
                users_df = users_df[users_df['first_name'].str.contains(search, case=False) | 
                                   users_df['email'].str.contains(search, case=False)]
            
            # Display dataframe
            st.dataframe(
                users_df,
                column_config={
                    "id": "ID",
                    "first_name": "First Name",
                    "last_name": "Last Name",
                    "email": "Email",
                    "username": "Username",
                    "user_type": "User Type",
                    "country": "Country",
                    "created_at": "Registered On"
                },
                use_container_width=True,
                hide_index=True
            )
            
            # Export option
            if st.button("📥 Export to CSV"):
                users_df.to_csv('registered_users.csv', index=False)
                st.success("Data exported successfully!")
        else:
            st.info("No users registered yet.")

# Initialize database and run app
if __name__ == "__main__":
    init_database()
    main()