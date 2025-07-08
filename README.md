# 🛡️ Cybersecurity Chatbot — Smart India Hackathon 2024

A specialized AI chatbot built to provide cybersecurity-focused answers, CVE lookups, product vulnerability information, vendor-specific vulnerability search, and cybersecurity tools guidance.  

🚀 Developed as a contribution for the **Smart India Hackathon 2024**, focusing on making cybersecurity information more accessible and actionable.

---

## 🌟 Features

- ✅ Answers **only cybersecurity-related questions**
- ✅ Search by **CVE ID** to get vulnerability details
- ✅ Search by **product name** to find known vulnerabilities
- ✅ Search across **40 mapped OEM vendor websites**
- ✅ Recommend and guide on cybersecurity tools
- ✅ Built using **NVIDIA Nemotron** large language model

---

## 🧠 Model & Approach

- **Model**: NVIDIA Nemotron (fine-tuned for cybersecurity domain)
- Specially trained to reject general queries and focus strictly on cybersecurity
- Integrated multiple data sources: CVE database, OEM vendor feeds, cybersecurity tools information

---

## 🛠️ Tech Stack

- **LLM**: NVIDIA Nemotron
- **Backend**: Python (FastAPI or Flask)
- **Frontend**: Streamlit / React (depending on deployment)
- **Data sources**: CVE official feeds, vendor vulnerability portals, security tool repositories
- **Additional**: Custom mappings for ~40 OEM vendors

---

## 💻 Use Cases

- Find detailed information about a **CVE** by its ID
- Search for known vulnerabilities using **product names**
- Check vulnerabilities listed by **OEM vendors** (e.g., Cisco, Fortinet, HP, etc.)
- Ask for recommended cybersecurity tools for specific security tasks (e.g., scanning, SIEM, endpoint protection)

---

## ⚙️ Setup & Installation

```bash
# Clone the repository
git clone https://github.com/spirit2103/chatting_bot.git
cd chatting_bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
