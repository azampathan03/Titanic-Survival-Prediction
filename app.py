import streamlit as st
import json
import os
from pathlib import Path
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from PIL import Image  


# Constants
DB_FILE = "users_db.json"

# Initialize session state
def init_session():
    if "auth" not in st.session_state:
        st.session_state.auth = {
            "logged_in": False,
            "username": "",
            "last_activity": None
        }

# Database functions
def load_db():
    try:
        if Path(DB_FILE).exists():
            with open(DB_FILE, "r") as f:
                return json.load(f)
        return {}
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return {}

def save_db(db):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(db, f)
    except Exception as e:
        st.error(f"Failed to save database: {str(e)}")

# Authentication functions
def validate_credentials(username, password):
    if not username or not password:
        return False, "All fields are required"
    if len(username) < 4:
        return False, "Username must be at least 4 characters"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""

def login_user(username, password):
    users_db = load_db()
    if username in users_db and users_db[username] == password:
        st.session_state.auth = {
            "logged_in": True,
            "username": username,
            "last_activity": st.session_state.get("_last_activity")
        }
        return True
    return False

def register_user(username, password, confirm_password):
    users_db = load_db()
    if username in users_db:
        return False, "Username already exists"
    if password != confirm_password:
        return False, "Passwords didn't match"

    valid, msg = validate_credentials(username, password)
    if not valid:
        return False, msg

    users_db[username] = password
    save_db(users_db)
    return True, ""


# UI Components
auth_styles = """
<style>
    /* Main container styling */
    .auth-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background-color: white;
    }

    /* Form styling */
    .auth-form {
        margin-top: 1.5rem;
    }

    /* Input field styling */
    .stTextInput>div>div>input,
    .stTextInput>div>div>input:focus {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
    }

    /* Button styling */
    .auth-button {
        width: 100%;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }

    /* Login button */
    .auth-button.login {
        background-color: #4CAF50;
        color: white;
        border: none;
    }

    /* Signup button */
    .auth-button.signup {
        background-color: #4285F4;
        color: white;
        border: none;
    }

    /* Title styling */
    .auth-title {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Error message styling */
    .stAlert {
        border-radius: 8px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        flex: 1;
        border-radius: 8px !important;
        padding: 10px 0;
        transition: all 0.3s;
    }

    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: white !important;
    }
</style>
"""


AUTH_CSS = """
<style>
    .auth-wrapper {
        max-width: 420px;
        margin: 2rem auto;
        padding: 2.5rem;
        border-radius: 16px;
        background: #ffffff;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
        font-family: 'Roboto', sans-serif;
    }

    .auth-wrapper h2 {
        text-align: center;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1.5rem;
    }

    .auth-wrapper label {
        font-weight: 500;
        color: #34495e;
    }

    .stTextInput>div>input {
        background-color: #f3f1ff;
        border: 1px solid #ccc;
        border-radius: 12px;
        padding: 12px 16px;
        color: #1e1e1e;
    }

    .stTextInput>div>input:focus {
        border-color: #6F5BF0;
        box-shadow: 0 0 0 3px rgba(111, 91, 240, 0.2);
    }

    .stButton>button {
        background: linear-gradient(270deg, #6F5BF0, #9d89fd);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        margin-top: 10px;
        cursor: pointer;
    }

    .stButton>button:hover {
        background: linear-gradient(270deg, #9d89fd, #6F5BF0);
    }
</style>
"""




def login_form():
    with st.form("login_form"):
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.form_submit_button("Login"):
            users_db = load_db()
            if login_user(username, password):
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

def signup_form():
    with st.form("signup_form"):
        st.subheader("Create Account")
        new_username = st.text_input("Choose Username", key="signup_username")
        new_password = st.text_input("Choose Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

        if st.form_submit_button("Sign Up"):
            success, message = register_user(new_username, new_password, confirm_password)
            if success:
                st.success("Account created successfully! Please login.")
            else:
                st.error(message)





# Auth Page
def auth_page():
    st.title("🔐 User Authentication")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        login_form()
    with tab2:
        signup_form()





# Titanic App
def titanic_app():
    # CSS styling
    st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }
        .stSelectbox, .stSlider {
            margin-bottom: 20px;
        }
        .prediction-card {
            border-radius: 10px;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
            padding: 20px;
            margin: 10px 0;
            background-color: white;
        }
        .survived {
            color: #2ecc71;
            font-weight: bold;
        }
        .not-survived {
            color: #e74c3c;
            font-weight: bold;
        }
        .title {
            color: #2c3e50;
            text-align: center;
        }
        .titanic-image {
            width: 100%;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Load your trained model
    @st.cache_resource
    def load_model():
        with open('titanic_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model

    model = load_model()

    # App header with HTML
    st.markdown("""
    <div class="title">
        <h1>🚢 Titanic Survival Prediction Web App</h1>
        <p>Step back in time to 1912 and discover your fate aboard the legendary RMS Titanic. This interactive app uses authentic passenger data and machine learning to predict whether you would have survived one of history's most famous maritime disasters.</p>
    </div>
    """, unsafe_allow_html=True)

    # Titanic image
    image= Image.open('titanic.jpg')
    st.image(image, caption="RMS Titanic", use_container_width=True)

    # Input features in sidebar
    st.sidebar.header('Passenger Details')

    def user_input_features():
        col1, col2 = st.sidebar.columns(2)

        with col1:
            pclass = st.selectbox('Passenger Class', [1, 2, 3], help="1 = First Class, 2 = Second Class, 3 = Third Class")
            sex = st.selectbox('Sex', ['female', 'male'])

        with col2:
            age = st.slider('Age', 0, 100, 30)
            fare = st.slider('Fare (£)', 0, 200, 30, help="Ticket fare in British pounds")

        embarked = st.sidebar.selectbox('Port of Embarkation',
                                      ['Southampton', 'Cherbourg', 'Queenstown'],
                                      help="S = Southampton, C = Cherbourg, Q = Queenstown")

        # Convert to model input format
        sex_encoded = 1 if sex == 'male' else 0
        embarked_encoded = {'Southampton': 0, 'Cherbourg': 1, 'Queenstown': 2}.get(embarked, 0)

        data = {
            'Pclass': pclass,
            'Sex': sex_encoded,
            'Age': age,
            'Fare': fare,
            'Embarked': embarked_encoded
        }

        return pd.DataFrame(data, index=[0])

    input_df = user_input_features()

    # Display prediction
    st.subheader('Prediction')
    if st.sidebar.button('Predict Survival'):
        prediction = model.predict(input_df)
        prediction_proba = model.predict_proba(input_df)

        survival_prob = prediction_proba[0][1] * 100

        # Save prediction to user history
        if st.session_state.auth["logged_in"]:
            record = {
                "Pclass": int(input_df["Pclass"][0]),
                "Sex": "male" if input_df["Sex"][0] == 1 else "female",
                "Age": int(input_df["Age"][0]),
                "Fare": float(input_df["Fare"][0]),
                "Embarked": int(input_df["Embarked"][0]),
                "Prediction": "Survived" if prediction[0] == 1 else "Did Not Survive",
                "Survival Probability (%)": round(survival_prob, 1),
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_prediction_history(st.session_state.auth["username"], record)

        survival_message = "🚢 TITANIC: SANK | YOU: FLOATED" if prediction[0] == 1 else "💀WELCOME TO THE BOTTOM OF THE OCEAN "
        sub_message = "You survived! The only thing sinking faster than the ship was Jack's dating profile!" if prediction[0] == 1 else "Your survival chances sank faster than the Titanic. Should've learned to swim!"
            
        st.markdown(f"""
            <div class="prediction-card">
                <h2>Prediction Result</h2>
                <p>Based on the passenger details, this person would have:</p>
                <h3 class="{'survived' if prediction[0] == 1 else 'not-survived'}">
                    {survival_message}
                </h3>
                <p>{sub_message}</p>
                <div style="margin-top: 20px;">
                    <p>Survival probability: <strong>{survival_prob:.1f}%</strong></p>
                    <div style="background: #ecf0f1; height: 20px; border-radius: 10px;">
                        <div style="background: {'#2ecc71' if prediction[0] == 1 else '#e74c3c'};
                            width: {survival_prob}%; height: 100%; border-radius: 10px;"></div>
                    </div>
                </div>
            </div>

                    
            <div style="margin-top: 20px;">
                <p>Survival probability: <strong>{survival_prob:.1f}%</strong></p>
                <div style="background: #ecf0f1; height: 20px; border-radius: 10px;">
                    <div style="background: {'#2ecc71' if prediction[0] == 1 else '#e74c3c'};
                        width: {survival_prob}%; height: 100%; border-radius: 10px;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)



# Path for storing user prediction history and feedback

PREDICTION_HISTORY_DIR = "user_prediction_history"
FEEDBACK_FILE = "feedback.json"

os.makedirs(PREDICTION_HISTORY_DIR, exist_ok=True)

def get_prediction_history(username):
    path = Path(PREDICTION_HISTORY_DIR) / f"{username}_history.json"
    if path.exists():
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_prediction_history(username, record):
    history = get_prediction_history(username)
    history.append(record)
    path = Path(PREDICTION_HISTORY_DIR) / f"{username}_history.json"
    with open(path, "w") as f:
        json.dump(history, f, indent=2)

def save_feedback(username, feedback_text):
    feedback_entry = {
        "username": username,
        "feedback": feedback_text,
        "timestamp": pd.Timestamp.now().isoformat()
    }
    if Path(FEEDBACK_FILE).exists():
        with open(FEEDBACK_FILE, "r") as f:
            all_feedback = json.load(f)
    else:
        all_feedback = []
    all_feedback.append(feedback_entry)
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(all_feedback, f, indent=2)

def dashboard():
    st.title(f"👤 Dashboard - Welcome {st.session_state.auth['username']}")

    st.subheader("User Profile")
    st.markdown(f"- **Username:** {st.session_state.auth['username']}")
    st.markdown(f"- **Logged in since:** {st.session_state.auth.get('last_activity', 'Unknown')}")

    st.markdown("---")
    st.subheader("📝 Prediction History")
    history = get_prediction_history(st.session_state.auth['username'])

    if history:
        df_history = pd.DataFrame(history)
        st.dataframe(df_history)
    else:
        st.info("No prediction history found.")

    st.markdown("---")
    st.subheader("📬 Feedback / Contact Form")
    feedback_input = st.text_area("Your feedback or message")
    if st.button("Submit Feedback"):
        if feedback_input.strip():
            save_feedback(st.session_state.auth['username'], feedback_input.strip())
            st.success("Thank you for your feedback!")
        else:
            st.error("Please enter some feedback before submitting.")



# Main App Router
init_session()

if st.session_state.auth["logged_in"]:
    page = st.sidebar.selectbox("Choose Page", ["Titanic Prediction", "Dashboard"])
    if page == "Titanic Prediction":
        titanic_app()
    elif page == "Dashboard":
        dashboard()

    if st.button("Logout"):
        st.session_state.auth["logged_in"] = False
        st.rerun()
else:
    auth_page()
