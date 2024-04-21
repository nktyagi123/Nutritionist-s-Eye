import streamlit as st

class BMI:
    def __init__(self, weight_kg, height_ft, height_inch):
        self.weight_kg = weight_kg
        self.height_ft = height_ft
        self.height_inch = height_inch

    def feet_inch_to_meters(self):
        """
        Convert height from feet and inches to meters.

        Returns:
            float: Height in meters.
        """
        total_inches = self.height_ft * 12 + self.height_inch
        height_m = total_inches * 0.0254  # 1 inch = 0.0254 meters
        return height_m

    def calculate_bmi(self):
        """
        Calculate the Body Mass Index (BMI) of a person.

        Returns:
            float: The calculated BMI value.
        """
        height_m = self.feet_inch_to_meters()
        bmi = self.weight_kg / (height_m ** 2)
        return round(bmi, 2)  # Round BMI to two decimal places

# Streamlit UI
st.title("BMI Calculator")

col1, col2 = st.columns([1, 1])
with col1:
    weight = st.number_input("Weight", value=63)
with col2:
    input_text = st.text_input("Any Issues", value="5.11")

col3, col4 = st.columns([1, 1])
with col3:
    height_feet = st.number_input("Height (feet)", value=5)
with col4:
    height_inches = st.number_input("Height (inches)", value=11)

units = st.selectbox("Select weight units", ["Kilograms", "Pounds"])

if units == "Pounds":
    weight *= 0.453592  # Convert pounds to kilograms

bmi_calculator = BMI(weight, height_feet, height_inches)
bmi = bmi_calculator.calculate_bmi()

st.write("BMI:", bmi)
