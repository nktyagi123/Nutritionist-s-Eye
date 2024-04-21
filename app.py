### Health Management APP
from dotenv import load_dotenv
from prompt_template import PromptTemplate
from BMI_calculation import BMI

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(image,input_text,bmi,user_name,meal):
    model=genai.GenerativeModel('gemini-pro-vision')
    template="""
    You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               Hi {user_name}, Good Day!

               Your Body Mass Index (BMI) is {bmi}.

               Food Items : 

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----

               Finally you can also mention whether the food is healthy or not accroding to
                my BMI is {bmi} and I have {input_text} health issue and based on my {meal} time,
               also mention the 
               percentage split of carbohydrates, fats, fibre, sugar and other important things required in our diet is as follows


    """


    # Create an instance of PromptTemplate
    prompt = PromptTemplate(input_variables=["input_text","bmi","user_name","meal"], template=template)

    filled_prompt = prompt.fill_template(input_text = input_text, bmi= bmi, user_name = user_name, meal = meal)

    print(filled_prompt)
    response=model.generate_content([image[0],filled_prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Nutritionist's Eye")

st.header("Nutritionist's Eye")

col1, col2 = st.columns([1, 1])
with col1:
    user_name = st.text_input("Name", value="")
with col2:
    weight = st.number_input("Weight", value=70)

col3, col4 = st.columns([1, 1])
with col3:
    height_feet = st.number_input("Height (feet)", value=5)
with col4:
    height_inches = st.number_input("Height (inches)",value=0, min_value=0, max_value=11)

col5, col6, col7 = st.columns([1, 1, 1])
with col5:
    meal = st.selectbox("Meal Type", ["Braekfast", "Lunch", "Dinner"])
with col6:
    units = st.selectbox("Select weight units", ["Kilograms", "Pounds"])
with col7:
    input = st.text_input("Any Health Issue", value="")

if units == "Pounds":
    weight *= 0.453592  # Convert pounds to kilograms
bmi_calculator = BMI(weight, height_feet, height_inches)
bmi = bmi_calculator.calculate_bmi()

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", width=400)


submit=st.button("Is this food good for me?")



## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    # Replace the placeholder with actual input values
    response=get_gemini_repsonse(image_data,input,bmi,user_name,meal)
    #st.subheader("The Response is")
    st.write(response)

