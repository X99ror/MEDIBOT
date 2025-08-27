import streamlit as st
from pathlib import Path
import google.generativeai as genai

from dotenv import load_dotenv
import os
load_dotenv()
gogle_api=os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=gogle_api)
gen_config={
    "temperature":0.4,
    "top_p":1,
    "top_k":32,
    "max_output_tokens":4096
}

safety_settings=[
    {
        "category":"HARM_CATEGORY_HARASSMENT",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category":"HARM_CATEGORY_HATE_SPEECH",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category":"HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category":"HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold":"BLOCK_MEDIUM_AND_ABOVE"
    }
]

model= genai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=gen_config,safety_settings=safety_settings)
st.set_page_config(page_title="MediBot", page_icon=":robot:")

st.title("MEDIBOT")

st.subheader("an AI assistant chatbot which will help you identify the symptoms based on the images")
uploaded_file=st.file_uploader("Upload your medical Image for the analysis",type=['png',"jpg"])
if uploaded_file:
    st.image(uploaded_file,width=300,caption="Uploaded symptom image")
submit_button=st.button("Generate analysis")

system_prompt="""
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.

2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.

3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.

4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.

2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are “Unable to be determined based on the provided image.”

3. Disclaimer: Accompany your analysis with the disclaimer: “Consult with a Doctor before making any decisions.”


Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.
"""

if submit_button:
    image_data=uploaded_file.getvalue()
    image_parts=[
        {
            "mime_type":"image/jpeg",
            "data":image_data
        }
    ]
    prompt_parts=[
        image_parts[0],
        system_prompt
        
    ]
    response=model.generate_content(prompt_parts)
    st.write(response.text)