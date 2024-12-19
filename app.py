# Import Libraries
import streamlit as st
import eda
import chatme

# Navigation Section
navigation = st.sidebar.selectbox("Choose Page", ("JobMate", "EDA"))

# Pages
if navigation == "JobMate":
    chatme.run()
else:
    eda.run()