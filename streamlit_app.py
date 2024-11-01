import streamlit as st
from datetime import datetime

# Temporary in-memory storage for posts (will reset each time app restarts)
if 'posts' not in st.session_state:
    st.session_state['posts'] = []

# App title and description
st.title("Anonymous Sharing Platform")
st.write("Share your secrets, confessions, or accomplishments anonymously in a supportive community.")

# Section for posting a new message
st.subheader("Share something anonymously")
user_input = st.text_area("What's on your mind? (secrets, confessions, or accomplishments)", "")
if st.button("Post"):
    if user_input.strip():
        # Add the post with a timestamp to the temporary session state
        st.session_state['posts'].append({
            "text": user_input.strip(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.success("Your post has been shared anonymously!")
        st.experimental_rerun()  # Refresh the page to show the new post
    else:
        st.error("Please write something before posting.")

# Display all posts
st.subheader("Anonymous Posts")
if st.session_state['posts']:
    for post in reversed(st.session_state['posts']):  # Display latest posts first
        st.write("**Posted at:**", post["timestamp"])
        st.write(post["text"])
        st.write("---")
else:
    st.write("No posts yet. Be the first to share something!")
