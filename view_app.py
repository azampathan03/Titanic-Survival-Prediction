# view_users_detailed.py - More detailed user viewer
import streamlit as st
import json
import pandas as pd

st.set_page_config(
    page_title="User Manager",
    page_icon="🔐", 
    layout="wide"
)

st.title("🔐 User Management Dashboard")

try:
    with open("users_db.json", "r") as f:
        users_db = json.load(f)
    
    if users_db:
        # Display as table
        st.subheader("📊 Users Table")
        users_df = pd.DataFrame({
            'Username': list(users_db.keys()),
            'Password': list(users_db.values())
        })
        st.dataframe(users_df, use_container_width=True)
        
        # Display as cards
        st.subheader("👥 User Details")
        cols = st.columns(3)
        for i, (username, password) in enumerate(users_db.items()):
            with cols[i % 3]:
                st.markdown(f"""
                <div style='border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                    <h4>👤 {username}</h4>
                    <p><strong>Password:</strong> <code>{password}</code></p>
                </div>
                """, unsafe_allow_html=True)
                
        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", len(users_db))
        with col2:
            avg_password_len = sum(len(pwd) for pwd in users_db.values()) / len(users_db)
            st.metric("Avg Password Length", f"{avg_password_len:.1f} chars")
        with col3:
            st.metric("Database Status", "✅ Loaded")
            
    else:
        st.warning("The user database exists but is empty")
        
except FileNotFoundError:
    st.error("""
    ❌ users_db.json not found
    
    This means:
    - No users have registered yet, OR
    - The file doesn't exist in the current deployment
    
    **Solution:** Go to your main app and register a user first.
    """)
except Exception as e:
    st.error(f"Error: {str(e)}")
