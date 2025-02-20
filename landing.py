import streamlit as st

st.title("Solar System Simulation")
st.write("This is an interactive 3D simulation of the solar system built with Pygame and OpenGL.")
st.write("Download the desktop app below to experience it fully:")
download_link = "https://drive.google.com/uc?export=download&id=1rhrAQ7DtaeHm0wjmyfrWu5Ne8H8QRE6Z"  # Replace with your link
st.markdown(f"[Download Solar System Simulation]({download_link})")
st.write("**Requirements**: Windows with OpenGL support.")
st.write("**Controls**:")
st.write("- Left Drag: Rotate camera")
st.write("- Right Click: Toggle labels")
st.write("- Mouse Wheel: Zoom")
st.write("- 1-8: Select planet")
st.write("- P: Pause/unpause")
st.write("- Left/Right Arrow: Adjust time scale")
st.write("- R: Reset camera")