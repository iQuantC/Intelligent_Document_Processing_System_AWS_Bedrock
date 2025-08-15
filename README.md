# Intelligent_Document_Processing_System_AWS_Bedrock
In this project, we will build a practical intelligent document processing system that automatically extracts data from forms, invoices, receipts, contracts, etc. We will utilize Python, Amazon Textract, and AWS-managed Amazon Bedrock. 


## Business Value
1. Reduces manual data entry by ~90%.
2. Speeds up billing, auditing, and legal workflows.
3. Minimizes human error and provides auditable logs. 


## Prerequisites
1. AWS Account with IAM User
2. Amazon Textract - A machine learning service that automatically extracts text, handwriting, layout elements, and data from scanned documents.
3. Amazon Bedrock - fully managed service that offers a choice of high-performing foundation LLM models & tools to deploy and operate agents.
4. AWS CLI installed & configured
5. Python 3.8+ installed
6. Install Streamlit and dependencies


## Architecture
1. Upload file (or scanned image).
2. Use Boto3 to call Amazon Textract sync API.
3. Textract parses results and returns text/blocks.
4. Draws bounding boxes over detected lines and display them alongside the raw image.
5. Deploy Amazon Bedrock (Anthropic Claude v2 LLM) to create a RAG system for Q&A based on the context.


### Set up Python Virtual Environment
```sh
python3 -m venv idps-venv
source idps-venv/bin/activate
```

```sh
pip install -r requirements.txt
```

### Set up AWS CLI & User Account
1. Install AWS CLI on your terminal (or verify version)
```sh
aws --version
```
2. Create an IAM user on AWS, create Access Keys and Download the csv file.
3. Configure the IAM User on your terminal 
```sh
aws configure
```


### Let's Add Q&A Capabilities to the App

To add Q&A capabilities to the app, we will use AWS Bedrock.
1. On AWS Management Console, navigate to AWS Bedrock Console
2. Click on "Model access" under "Configure and learn" in the lower left sidebar
3. Click on "Enable all models" or "select specific models".
4. Provide some details like company name, website, industry, etc. 
5. Review your selections and submit it.
6. Once approved, you can proceed to the application.



## Run the IDPS App

### Add AWS REGION to the Bash Session
```sh
export AWS_REGION=us-east-1
```

```sh
streamlit run streamlitapp.py
```


## Test the App
1. Upload an invoice/receipt
2. Scroll down & ask a question like:

### Example 1: Invoice/Receipt Documents
1. What is the invoice number?
2. What is the total amount?
3. Who is the recipient?
4. What is the address of the recipient? Be brief and concise
5. How much in total was charged for consulting? Be brief
6. What are the terms of the invoice? Be brief and concise

### Example 2: Land Purchase Agreement Document
1. How is the balance at closing going to be transferred? Be brief and concise
2. Who is Frank Winfield?
3. What did Frank Winfield invent?

