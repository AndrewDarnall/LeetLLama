""" User and System Prompt Templates """
from jinja2 import Template

system_prompt = """
You are a Senior Software Engineer, leetcode expert and teacher. Answer accurately and in a friendly yet insightful way.
"""

user_prompt_template = Template("""
Question:
{{ user_input }}

RAG Context:
{{ context }}

---

Instructions:

Please respond to the input question in three portions:

a) Provide a high-level algorithmic solution. Keep it concise and to the point.

b) Provide a step-by-step explanation of the code solution, breaking down the logic and key components.

c) Provide the entire final code solution.
""")