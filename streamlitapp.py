import streamlit as st
import boto3
from botocore.exceptions import ClientError
from PIL import Image, ImageDraw
import io
import json
import pandas as pd
import os
from typing import Dict, List, Optional

# AWS Config
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# AWS Clients
session = boto3.Session()
textract = session.client('textract', region_name=AWS_REGION)
bedrock_runtime = session.client('bedrock-runtime', region_name=AWS_REGION)

st.set_page_config(page_title='IDPS Demo', layout='centered')
st.title('Intelligent Document Processing System with Q&A')

st.markdown('Upload an image for text extraction, visualization, and question answering.')

uploaded_file = st.file_uploader(
    'Upload document', 
    type=['png', 'jpg', 'jpeg', 'tiff']
)

def extract_text_from_response(response: Dict) -> str:
    """Extract all text from Textract response in reading order."""
    blocks = response.get('Blocks', [])
    lines = [b for b in blocks if b['BlockType'] == 'LINE']
    text = '\n'.join([l['Text'] for l in lines])
    return text

def ask_bedrock_question(context: str, question: str) -> Optional[str]:
    """Use Amazon Bedrock to answer questions based on the extracted text."""
    prompt = f"""Human: You are a helpful assistant that answers questions based on the provided document context.

Document Context:
{context}

Question: {question}

Assistant:"""
    
    try:
        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-v2",
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 1000,
                "temperature": 0.5,
                "top_p": 0.9,
            }),
            contentType="application/json",
        )
        result = json.loads(response['body'].read())
        return result['completion'].strip()
    except ClientError as e:
        st.error(f"AWS Bedrock error: {e}")
        return None
    
def process_document_for_qa(file_bytes: bytes) -> Optional[Dict]:
    """Process document with Textract and prepare for QA."""
    try:
        response = textract.detect_document_text(Document={'Bytes': file_bytes})
        return response
    except ClientError as e:
        st.error(f"AWS Client error: {e}")
        return None
    
def draw_bounding_boxes(image, blocks, color="red", width=2):
    """Draw bounding boxes on the image for visualization."""
    img = image.copy()
    img_width, img_height = img.size
    draw = ImageDraw.Draw(img)

    for block in blocks:
        if block['BlockType'] == 'LINE':
            box = block['Geometry']['BoundingBox']
            left = img_width * box['Left']
            top = img_height * box['Top']
            w = img_width * box['Width']
            h = img_height * box['Height']
            draw.rectangle(
                [(left, top), (left + w, top + h)],
                outline=color,
                width=width
            )
    return img

# Main application logic (when user enters input)
if uploaded_file is not None:
    file_bytes = uploaded_file.read()

    if uploaded_file.type.startswith('image'):
        original_img = Image.open(io.BytesIO(file_bytes))
        st.image(original_img, caption='Uploaded Image')

        with st.spinner('Processing with Amazon Textract...'):
            resp = process_document_for_qa(file_bytes)

        if resp:
            # Extract text for display and QA
            extracted_text = extract_text_from_response(resp)
            
            # Display extracted text
            with st.expander("View Extracted Text"):
                st.code(extracted_text)

            # Display bounding box visualization
            st.subheader('Bounding Box Visualization')
            boxed_img = draw_bounding_boxes(original_img, resp['Blocks'])
            st.image(boxed_img, caption='Detected text with bounding boxes')

            # Question Answering Section
            st.subheader('Document Question Answering')
            question = st.text_input("Ask a question about the document content:")
            
            if question and extracted_text:
                with st.spinner('Searching for answer...'):
                    answer = ask_bedrock_question(extracted_text, question)
                    if answer:
                        st.success(f"Answer: {answer}")
                    else:
                        st.warning("Could not generate an answer for this question.")
