# 🤖 AI Smart Task Planner

![Python](https://img.shields.io/badge/Python-3-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-UI-FF7C00?style=flat-square&logo=gradio&logoColor=white)

AI-powered task breakdown system that transforms complex goals into structured, dependency-aware, risk-assessed execution plans using Large Language Model (LLM) reasoning.

Built with GPT-4o-mini and deployed via a production-ready Gradio interface.

---

## 🚀 What This Project Does

Given a high-level goal, the system:

- Breaks it into 6–12 actionable tasks
- Identifies logical task dependencies
- Estimates realistic durations
- Assigns priorities (High / Medium / Low)
- Identifies risks and blockers
- Calculates total project time
- Generates execution sequence
- Provides JSON export for integration

All in seconds.

---

## 🧠 Example Output

Below is a real generated task plan (see full screenshots in repo):

- Goal: Launch a website
- Total Tasks: 11
- Estimated Time: 4 weeks
- Execution timeline with dependency ordering
- Priority breakdown visualization

(Screenshots available in repository)

---

## 🏗 System Architecture

User Input (Goal + Timeframe + Context)
        ↓
LLM Reasoning Engine (GPT-4o-mini)
        ↓
JSON Parsing & Validation Layer
        ↓
Task Structuring + Dependency Modeling
        ↓
Execution Timeline Generator
        ↓
Formatted Plan Output + JSON Export
        ↓
Gradio Web Interface

---

## 🧠 Core Engine Design

### 1️⃣ LLM Prompt Engineering

The planner uses a structured system + user prompt to ensure:

- Action-oriented task naming
- Logical sequencing
- Risk identification
- Realistic duration estimates
- Critical path awareness
- Valid JSON output

### 2️⃣ Task Validation Layer

Every LLM-generated task is validated and normalized:

- ID assignment
- Missing field handling
- Default priority enforcement
- Duration parsing
- Dependency formatting

### 3️⃣ Time Estimation Engine

Durations are parsed and converted to estimated total hours:
- Hours → Direct sum
- Days → 8-hour conversion
- Weeks → 40-hour conversion

System automatically calculates:
- Total estimated time
- Priority distribution
- Execution order

---

## 📊 Features

### Core Planning Features

✅ AI-powered task generation  
✅ Dependency mapping  
✅ Timeline estimation  
✅ Risk identification  
✅ Deliverables tracking  
✅ Priority classification  
✅ Execution sequencing  

### Engineering Features

✅ JSON export  
✅ Task history tracking  
✅ Statistics dashboard  
✅ In-memory database  
✅ Fallback logic if API fails  
✅ Production-ready Gradio UI  

---

## 🛠 Tech Stack

- Python 3
- OpenAI API (GPT-4o-mini)
- Gradio
- JSON Validation
- Environment variable configuration (.env)

---

## 📂 Project Structure

```
app.py                 → Production application entry point
ai_task_planner.py     → Core planning engine
output.pdf             → Sample generated output screenshots
requirements.txt       → Dependencies
```

---

## ⚙️ Installation

### Option 1 — Local Setup

Clone repository:

```bash
git clone https://github.com/tharunsridhar/Smart-Task-Planner.git
cd Smart-Task-Planner
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set API key:

Mac/Linux:
```bash
export OPENAI_API_KEY="your-api-key"
```

Windows:
```bash
set OPENAI_API_KEY=your-api-key
```

Run application:

```bash
python app.py
```

Gradio link will be generated automatically.

---

## 🧪 How It Works Internally

1. User enters goal + timeframe + context.
2. Planner sends structured prompt to GPT-4o-mini.
3. Model returns JSON task array.
4. JSON is parsed and validated.
5. Tasks are enriched with metadata.
6. Total time is calculated.
7. Execution sequence is derived from dependencies.
8. Output is formatted for display.
9. JSON export option provided.

---

## 📈 Sample Output Sections

Generated plan includes:

- Plan Overview
- Task Breakdown
- Duration & Dependencies
- Risk Assessment
- Execution Timeline
- Priority Breakdown
- JSON Export
- Planning Statistics

(See output.pdf in repo for visual examples.)

---

## 🔐 Safety & Reliability

- No hardcoded credentials (uses environment variables)
- JSON parsing validation
- Fallback plan generation if API fails
- Controlled temperature for consistent output
- Strict structured prompt format

---

## ⚠️ Limitations

- Depends on OpenAI API availability
- In-memory storage (no persistent database)
- Duration parsing is heuristic-based
- Dependency correctness depends on model output quality

---

## 🎯 Use Cases

- Startup project planning
- Software roadmap breakdown
- Event planning
- Research project structuring
- Academic project organization
- Personal productivity planning

---

## 🔮 Future Improvements

- Persistent database (PostgreSQL / MongoDB)
- Gantt chart visualization
- Critical path computation
- User authentication
- Team collaboration features
- Cost estimation module
- Deployment to cloud (AWS / GCP)

---

## 📌 Why This Project Is Strong

This is not just a wrapper around an API.

It demonstrates:

- Prompt engineering
- Structured LLM output control
- JSON validation
- Task dependency modeling
- Time estimation logic
- Error handling & fallback design
- Production UI deployment
- Modular architecture

This positions the project as an **AI application system**, not a demo.

---

## 👤 Author

Tharun Sridhar  
