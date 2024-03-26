import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

name, authentication_status, username = authenticator.login()

# Authenticated Content
if authentication_status:
    authenticator.logout("Logout", "main", key="unique_key")
    st.write(f"Welcome *{name}*")
    st.title("Some content")
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")

# Reset password
if authentication_status:
    try:
        if authenticator.reset_password(username):
            st.success("Password modified successfully")
            with open("../config.yaml", "w") as file:
                yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)
