#!/usr/bin/env python3
"""
AI Smart Task Planner - Standalone Application
Run this file directly: python app.py
"""

import os
import json
import uuid
from datetime import datetime
from typing import List, Dict
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

if not OPENAI_API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY not found in environment variables")
    print("Please set it in .env file or as environment variable")
    print("Example: export OPENAI_API_KEY='sk-proj-...'")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

class SmartTaskPlanner:
    """AI-powered task planner with LLM reasoning"""
    
    def __init__(self):
        self.client = client
        self.database = []
        self.task_history = []
    
    def generate_plan(self, goal: str, timeframe: str = "2 weeks", 
                     additional_context: str = "") -> Dict:
        """Generate task plan using LLM reasoning"""
        
        if not self.client:
            return self._generate_fallback_plan(goal, timeframe)
        
        try:
            tasks = self._generate_tasks_with_llm(goal, timeframe, additional_context)
            
            plan = {
                "id": str(uuid.uuid4())[:8],
                "goal": goal,
                "timeframe": timeframe,
                "tasks": tasks,
                "created_at": datetime.now().isoformat(),
                "total_tasks": len(tasks),
                "estimated_total_time": self._calculate_total_time(tasks)
            }
            
            self.database.append(plan)
            self.task_history.append(plan)
            
            return plan
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return self._generate_fallback_plan(goal, timeframe)
    
    def _generate_tasks_with_llm(self, goal: str, timeframe: str, context: str) -> List[Dict]:
        """Core LLM reasoning"""
        
        system_prompt = """You are an expert project manager. Create comprehensive task breakdowns with dependencies, timelines, and risk assessment."""
        
        user_prompt = f"""Break down this goal into 6-12 actionable tasks:

GOAL: {goal}
TIMEFRAME: {timeframe}
{f"CONTEXT: {context}" if context else ""}

For each task provide:
- name: Clear task name
- description: What needs to be done
- duration: Time estimate
- dependencies: Prerequisites (or "None")
- priority: High/Medium/Low
- deliverables: Expected outputs
- risks: Potential issues

Return as JSON array."""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        
        result = response.choices[0].message.content
        
        # Parse JSON
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        elif "```" in result:
            result = result.split("```")[1].split("```")[0].strip()
        
        tasks = json.loads(result)
        
        if isinstance(tasks, dict) and "tasks" in tasks:
            tasks = tasks["tasks"]
        
        return self._validate_tasks(tasks)
    
    def _validate_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """Validate task structure"""
        validated = []
        
        for i, task in enumerate(tasks, 1):
            validated_task = {
                "id": i,
                "name": task.get("name", f"Task {i}"),
                "description": task.get("description", "No description"),
                "duration": task.get("duration", "1 day"),
                "dependencies": task.get("dependencies", "None"),
                "priority": task.get("priority", "Medium"),
                "deliverables": task.get("deliverables", "Task completion"),
                "risks": task.get("risks", "None identified"),
                "status": "pending"
            }
            validated.append(validated_task)
        
        return validated
    
    def _calculate_total_time(self, tasks: List[Dict]) -> str:
        """Calculate total project time"""
        total_hours = 0
        
        for task in tasks:
            duration = task.get("duration", "1 day").lower()
            
            if "hour" in duration:
                hours = int(''.join(filter(str.isdigit, duration.split()[0])))
                total_hours += hours
            elif "day" in duration:
                days = int(''.join(filter(str.isdigit, duration.split()[0])))
                total_hours += days * 8
            elif "week" in duration:
                weeks = int(''.join(filter(str.isdigit, duration.split()[0])))
                total_hours += weeks * 40
        
        if total_hours < 8:
            return f"{total_hours} hours"
        elif total_hours < 40:
            return f"{total_hours // 8} days"
        else:
            return f"{total_hours // 40} weeks"
    
    def _generate_fallback_plan(self, goal: str, timeframe: str) -> Dict:
        """Fallback when AI unavailable"""
        tasks = [
            {
                "id": 1,
                "name": "Planning & Research",
                "description": f"Research and plan: {goal}",
                "duration": "2 days",
                "dependencies": "None",
                "priority": "High",
                "deliverables": "Project plan",
                "risks": "Insufficient info",
                "status": "pending"
            },
            {
                "id": 2,
                "name": "Setup",
                "description": "Environment and tools setup",
                "duration": "1 day",
                "dependencies": "Planning & Research",
                "priority": "High",
                "deliverables": "Ready environment",
                "risks": "Technical issues",
                "status": "pending"
            },
            {
                "id": 3,
                "name": "Implementation",
                "description": "Core development work",
                "duration": "1 week",
                "dependencies": "Setup",
                "priority": "High",
                "deliverables": "Working prototype",
                "risks": "Complexity",
                "status": "pending"
            }
        ]
        
        return {
            "id": str(uuid.uuid4())[:8],
            "goal": goal,
            "timeframe": timeframe,
            "tasks": tasks,
            "created_at": datetime.now().isoformat(),
            "total_tasks": len(tasks),
            "estimated_total_time": timeframe
        }
    
    def format_plan_output(self, plan: Dict) -> str:
        """Format for display"""
        output = f"""# 🎯 Task Plan

**ID**: {plan['id']}  
**Goal**: {plan['goal']}  
**Timeframe**: {plan['timeframe']}  
**Tasks**: {plan['total_tasks']}  

---

"""
        
        for task in plan['tasks']:
            priority_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(task['priority'], "⚪")
            
            output += f"""## {task['id']}. {task['name']} {priority_icon}

{task['description']}

⏱️ **Duration**: {task['duration']}  
🔗 **Dependencies**: {task['dependencies']}  
📦 **Deliverables**: {task['deliverables']}  
⚠️ **Risks**: {task['risks']}

---

"""
        
        return output

# Initialize
planner = SmartTaskPlanner()

# Gradio functions
def generate_task_plan(goal, timeframe, context):
    if not goal.strip():
        return "⚠️ Please enter a goal", "", ""
    
    plan = planner.generate_plan(goal, timeframe, context)
    formatted = planner.format_plan_output(plan)
    json_export = json.dumps(plan, indent=2)
    
    stats = f"**Plans Generated**: {len(planner.database)}"
    
    return formatted, json_export, stats

# Create UI
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🤖 AI Smart Task Planner")
    
    with gr.Row():
        goal_input = gr.Textbox(label="Goal", lines=3)
        timeframe_input = gr.Textbox(label="Timeframe", value="2 weeks")
    
    context_input = gr.Textbox(label="Context (Optional)", lines=2)
    generate_btn = gr.Button("Generate Plan", variant="primary")
    
    with gr.Tabs():
        with gr.Tab("Plan"):
            plan_output = gr.Markdown()
        with gr.Tab("JSON"):
            json_output = gr.Code(language="json")
        with gr.Tab("Stats"):
            stats_output = gr.Markdown()
    
    generate_btn.click(
        fn=generate_task_plan,
        inputs=[goal_input, timeframe_input, context_input],
        outputs=[plan_output, json_output, stats_output]
    )

if __name__ == "__main__":
    print("🚀 Starting AI Smart Task Planner...")
    app.launch(share=True)