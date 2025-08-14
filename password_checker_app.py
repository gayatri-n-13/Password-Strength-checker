import math
import re
import streamlit as st

def calculate_entropy(password):
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in '!@#$%^&*()-_=+[]{};:,.<>/?' for c in password):
        charset += 32  # Approximation for special characters

    if charset == 0:
        return 0

    entropy = math.log2(charset) * len(password)
    return entropy

def check_password_strength(password):
    entropy = calculate_entropy(password)
    feedback = []

    if len(password) < 8:
        feedback.append("Password should be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        feedback.append("Add uppercase letters.")
    if not re.search(r'[a-z]', password):
        feedback.append("Add lowercase letters.")
    if not re.search(r'\d', password):
        feedback.append("Include at least one number.")
    if not re.search(r'[!@#$%^&*()-_=+\[\]{};:,.<>/?]', password):
        feedback.append("Include at least one special character.")

    if entropy < 28:
        strength = "Very Weak"
    elif entropy < 36:
        strength = "Weak"
    elif entropy < 60:
        strength = "Moderate"
    elif entropy < 128:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return entropy, strength, feedback

# --- Streamlit UI ---
st.title("🔐 Password Strength Checker")

password = st.text_input("Enter your password:", type="password")

if password:
    entropy, strength, tips = check_password_strength(password)

    st.write(f"**Password Entropy:** {entropy:.2f} bits")
    st.write(f"**Password Strength:** {strength}")

    if tips:
        st.warning("Suggestions:")
        for tip in tips:
            st.write(f"- {tip}")
    else:
        st.success("Your password looks solid!")
