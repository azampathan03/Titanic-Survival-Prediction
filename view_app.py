import streamlit as st
import json

st.set_page_config(page_title="User Viewer", page_icon="🔍")

def main():
    st.title("🔍 User Data Viewer")
    st.write("This shows all registered users and their passwords")

    try:
        with open('users_db.json', 'r') as f:
            users = json.load(f)

        st.success(f"Found {len(users)} registered users:")

        for username, password in users.items():
            st.write(f"**👤 Username:** `{username}`")
            st.write(f"**🔑 Password:** `{password}`")
            st.write("---")

    except FileNotFoundError:
        st.error("No users registered yet - users_db.json not found")
    except Exception as e:
        st.error(f"Error reading file: {e}")

if __name__ == "__main__":
    main()

