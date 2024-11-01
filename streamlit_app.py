import streamlit as st
import pandas as pd

# Initialize session state for storing user profiles and matches
if 'profiles' not in st.session_state:
    st.session_state['profiles'] = []

if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

# Title
st.title("Skill-Swap Platform for Professionals")

# Sidebar for user profile creation
with st.sidebar:
    st.header("Create Your Profile")
    name = st.text_input("Name")
    skills_offered = st.text_area("Skills You Offer (comma-separated)")
    skills_needed = st.text_area("Skills You're Looking For (comma-separated)")
    submit = st.button("Create Profile")

    # Adding user to profile list
    if submit:
        if name and skills_offered and skills_needed:
            profile = {
                "Name": name,
                "Skills Offered": [skill.strip().lower() for skill in skills_offered.split(',')],
                "Skills Needed": [skill.strip().lower() for skill in skills_needed.split(',')]
            }
            st.session_state['profiles'].append(profile)
            st.session_state['current_user'] = profile
            st.success(f"Profile for {name} created!")
        else:
            st.error("Please fill in all fields.")

# Main Page for Skill Matching and Messaging
st.subheader("Find Your Skill Match")

# Display current user profile
current_user = st.session_state.get('current_user')
if current_user:
    st.write("### Your Profile")
    st.write(f"**Name**: {current_user['Name']}")
    st.write(f"**Skills Offered**: {', '.join(current_user['Skills Offered'])}")
    st.write(f"**Skills Needed**: {', '.join(current_user['Skills Needed'])}")

    # Find matches based on skills
    st.write("### Available Matches")
    matches = []
    for profile in st.session_state['profiles']:
        if profile != current_user:
            # Check if this user has needed skills
            if any(skill in profile['Skills Offered'] for skill in current_user['Skills Needed']):
                matches.append(profile)
    
    if matches:
        for match in matches:
            st.write(f"**{match['Name']}** offers **{', '.join(match['Skills Offered'])}**")
            st.write(f"Skills they are looking for: {', '.join(match['Skills Needed'])}")
            if st.button(f"Connect with {match['Name']}"):
                st.write(f"You connected with {match['Name']}!")
    else:
        st.write("No matches found for your skills at the moment.")

else:
    st.write("Please create a profile to find skill matches.")

# Mock Chat and Schedule
st.subheader("Messaging and Scheduling")

if current_user:
    chat_user = st.selectbox("Select a user to chat with", [profile["Name"] for profile in st.session_state['profiles'] if profile != current_user])
    if chat_user:
        st.write(f"Chat with {chat_user}")
        message = st.text_input("Your Message")
        send = st.button("Send")
        if send:
            st.write(f"Message to {chat_user}: {message}")
    
    st.write("### Schedule a Session")
    session_date = st.date_input("Select a date")
    session_time = st.time_input("Select a time")
    confirm_session = st.button("Confirm Session")
    if confirm_session:
        st.success(f"Session scheduled on {session_date} at {session_time}!")
else:
    st.write("Please create a profile to start messaging and scheduling.")
