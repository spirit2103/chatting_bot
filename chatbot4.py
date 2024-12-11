import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import re
import json

load_dotenv()

# Initialize the NVIDIA API client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_NEMOTRON_API_KEY")
)

# Functions for generating responses
def finding_product_details(client,user_input):
    prompt = f"""
You are a cybersecurity expert specializing in CVE analysis.Provide verified, concise, and accurate vulnerability information based on your knowledge. If unsure, explicitly state: "This information may not be up-to-date."
for details you may refer all these websites:
    first search in OEM websites if details is not find then use this link https://www.cvedetails.com/


Details for CVE-ID: {user_input}

Response Format:
- CVE-ID: <cve_id>
- Device Name: <device_name>
- Description: <description>
- Severity Level: <severity>
- Mitigation Strategy: <mitigation>
- Link: <link>

Start your response now:
"""
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "system", "content": "you are a cybersecurity expert"},
            {"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=2048,
        stream = True
    )
    response_text = ""  # Initialize an empty string to collect the response
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response_text += chunk.choices[0].delta.content  # Append each chunk to the response text
    return response_text

def find_cve_details(cve_id):
    prompt = f"""
"Provide detailed information about {cve_id}, including its impact, technical details, affected systems or versions, severity (CVSS score), potential exploits, available patches or mitigation steps, and references to any official advisories, databases, or resources."
    first search in OEM websites if details is not find then use this link https://www.cvedetails.com/

    Response:
    Device Name: <device_name>
    Description: <description>
    Severity Level: <severity>
    Mitigation Strategy: <mitigation>
    Link: <link>

    Now process:
    CVE-ID: {cve_id}
    """
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "system", "content": "you are a cyber security expert"},
            {"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream = True
    )
    response_text = ""  # Initialize an empty string to collect the response
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response_text += chunk.choices[0].delta.content  # Append each chunk to the response text
    return response_text

def find_oem_website(user_input):
    with open(r"OEm_venddors.json", "r", encoding="utf-8") as file:
        oem_data = json.load(file)
    words = user_input.lower().split()
    for word in words:
        for entry in oem_data:
            if word == entry["product"].lower():
                return f"OEM website for the given product: {entry['product']} \n\n link: {entry['oemwebsite']} \n\n Using the  provided link search for the product vulnerability details."


def find_tools(user_input):
    prompt = f"""
    You are a cybersecurity assistant.Provide a 200-word description of the given cybersecurity tool.
    Tool Name: {user_input}
    Response:
   
    """
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=256,
        stream = True
    )
    response_text = ""  # Initialize an empty string to collect the response
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response_text += chunk.choices[0].delta.content  # Append each chunk to the response text
    return response_text


def ignore_query(user_input):
    prompt = f"""
    You are a cybersecurity assistant. 
    answer the queries related to cybersecurity.
    If it is related to the cybersecurity then give the information in a very short manner like 200 words maximum
    remember the previous query user might ask something about that.  
    Respond politely to greeting queries and refuse queries unrelated to cybersecurity.

    Input: {user_input}
    Response:
    """
    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemotron-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=256,
        stream = True
    )
    response_text = ""  # Initialize an empty string to collect the response
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response_text += chunk.choices[0].delta.content  # Append each chunk to the response text
    return response_text


def classified_data(user_input):
    pattern = r"cve-\d{4}-\d{4,}"
    matches = re.findall(pattern, user_input.lower())
    if "oem " in user_input.lower():
        return find_oem_website(user_input)
    elif matches:
        for match in matches:
            return find_cve_details(user_input)
    elif "tool" in user_input.lower() or "tools" in user_input.lower():
        return find_tools(user_input)
    elif "product" in user_input.lower() or "device" in user_input.lower():
        return finding_product_details(client,user_input)
    else:
        return ignore_query(user_input)

# Streamlit UI
st.set_page_config(page_title="Cybersecurity Assistant", layout="centered")

st.title("🤖 Cybersecurity Assistant")
st.markdown("Ask questions about **vulnerabilities**, **CVE-IDs**, **OEM websites**, or **cybersecurity tools**.")

# Chat container
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["is_user"]:
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Input box
if prompt := st.chat_input("Type your message here..."):
    # User message
    st.session_state.messages.append({"is_user": True, "content": prompt})
    st.chat_message("user").write(prompt)

    # Assistant response
    response = classified_data(prompt)
    st.session_state.messages.append({"is_user": False, "content": response})
    st.chat_message("assistant").write(response)
