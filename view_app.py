# view_users_streamlit.py - Streamlit version to view users
import streamlit as st
import json

st.set_page_config(
    page_title="User Viewer",
    page_icon="👥",
    layout="centered"
)

st.title("👥 User Database Viewer")
st.write("View all registered users and their passwords")

try:
    with open("users_db.json", "r") as f:
        users_db = json.load(f)
    
    if users_db:
        st.success(f"✅ Found {len(users_db)} registered users:")
        
        # Display in a nice formatted way
        for username, password in users_db.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"**👤 {username}**")
            with col2:
                st.code(f"Password: {password}")
            st.divider()
            
        # Show summary
        st.info(f"**Total Users:** {len(users_db)}")
    else:
        st.warning("No users found in the database (file exists but is empty)")
        
except FileNotFoundError:
    st.error("❌ users_db.json not found - No users have registered yet")
except Exception as e:
    st.error(f"❌ Error loading users_db.json: {str(e)}")
