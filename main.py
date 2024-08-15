import streamlit as st
import anthropic
from matplotlib import pyplot as plt  # type: ignore
import plotly.express as px  # type: ignore

# API KEY 
api_key = st.secrets["claude_api_key"]

# Function to call Claude AI API and get a personalized meal plan
def get_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences, age, weight, height, activity_level):
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = (
        f"I am {age} years old, weigh {weight} kg, and am {height} cm tall. "
        f"My fasting sugar level is {fasting_sugar} mg/dL, "
        f"pre-meal sugar level is {pre_meal_sugar} mg/dL, "
        f"post-meal sugar level is {post_meal_sugar} mg/dL. "
        f"I prefer {dietary_preferences} food and have an {activity_level} activity level. "
        "Please provide a personalized meal plan that can help me manage my blood sugar levels effectively."
    )
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=250,
        temperature=0.7,
        system="You are a world-class nutritionist who specializes in diabetes management.",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    raw_context = message.content
    itinerary = raw_context[0].text
    return itinerary

# Streamlit app
st.set_page_config(page_title="GlucoGuide", page_icon="🍎", layout="centered")

st.title("GlucoGuide 🍎")

st.write("""
**GlucoGuide** is a personalized meal planning tool for managing diabetes. 
By entering your details, GlucoGuide generates tailored meal plans.
""")

st.sidebar.header("Enter Your Details")

age = st.sidebar.number_input("Age (years)", min_value=0, max_value=120, step=1)
weight = st.sidebar.number_input("Weight (kg)", min_value=0, max_value=200, step=1)
height = st.sidebar.number_input("Height (cm)", min_value=0, max_value=250, step=1)
activity_level = st.sidebar.selectbox("Activity Level", ["Low", "Moderate", "High"])

fasting_sugar = st.sidebar.number_input("Fasting Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)
pre_meal_sugar = st.sidebar.number_input("Pre-Meal Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)
post_meal_sugar = st.sidebar.number_input("Post-Meal Sugar Levels (mg/dL)", min_value=0, max_value=500, step=1)

dietary_preferences = st.sidebar.text_input("Dietary Preferences (e.g., vegetarian, low-carb)")

if st.sidebar.button("Generate Meal Plan"):
    meal_plan = get_meal_plan(api_key, fasting_sugar, pre_meal_sugar, post_meal_sugar, dietary_preferences, age, weight, height, activity_level)
    st.write("### Personalized Meal Plan")
    st.markdown(meal_plan)

# Example of adding a graph (plotly)
sugar_levels = {
    "Fasting": fasting_sugar,
    "Pre-Meal": pre_meal_sugar,
    "Post-Meal": post_meal_sugar
}

fig = px.bar(x=list(sugar_levels.keys()), y=list(sugar_levels.values()), labels={'x': "Sugar Level Type", 'y': "Value (mg/dL)"})
st.plotly_chart(fig)
