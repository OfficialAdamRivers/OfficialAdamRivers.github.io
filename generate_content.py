import os
import random
from datetime import datetime
from transformers import pipeline, set_seed
import language_tool_python
from sentence_transformers import SentenceTransformer, util
from jinja2 import Template
import subprocess

BLOG_DIR = "_posts"
os.makedirs(BLOG_DIR, exist_ok=True)

TOPICS = [
    "vCISO roles and challenges",
    "Emerging AI threats in cybersecurity",
    "Quantum computing's impact on encryption",
    "Zero trust security architecture",
    "Incident response best practices",
]

SEED = 42
POSTS_PER_DAY = random.randint(1, 3)

generator = pipeline('text-generation', model='EleutherAI/gpt-j-6B', device=-1)  # CPU only in GitHub Actions
set_seed(SEED)

tool = language_tool_python.LanguageTool('en-US')

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

MD_TEMPLATE = """
---
layout: post
title: "{{ title }}"
date: {{ date }}
categories: cybersecurity AI quantum vCISO
tags: cybersecurity, AI, quantum, vCISO, infosecurity
seo_title: "{{ seo_title }}"
seo_description: "{{ seo_description }}"
---

# {{ title }}

## Introduction
{{ introduction }}

## Key Facts
{{ facts }}

## Analysis
{{ analysis }}

## Conclusion
{{ conclusion }}
"""

def generate_section(prompt, max_length=400):
    result = generator(prompt, max_length=max_length, do_sample=True, temperature=0.7)
    return result[0]['generated_text'].strip()

def grammar_check(text):
    matches = tool.check(text)
    corrected = language_tool_python.utils.correct(text, matches)
    return corrected

def semantic_check(sections):
    texts = list(sections.values())
    embeddings = embedding_model.encode(texts)
    for i in range(len(embeddings) - 1):
        similarity = util.cos_sim(embeddings[i], embeddings[i+1]).item()
        if similarity < 0.3:
            raise ValueError(f"Low semantic coherence between section {i} and {i+1}")
    return True

def generate_article(topic):
    sections = {}
    sections['title'] = f"{topic} in Cybersecurity"
    sections['introduction'] = generate_section(f"Introduction on {topic} in cybersecurity.")
    sections['facts'] = generate_section(f"Facts and figures on {topic} in cybersecurity.")
    sections['analysis'] = generate_section(f"Analytical discussion on {topic} cybersecurity implications.")
    sections['conclusion'] = generate_section(f"Conclusion about the future and importance of {topic} in cybersecurity.")

    for key in sections:
        sections[key] = grammar_check(sections[key])

    semantic_check(sections)

    return sections

def render_to_markdown(sections):
    seo_title = sections['title'][:60]
    seo_description = sections['introduction'][:160]
    date_iso = datetime.utcnow().isoformat()

    tpl = Template(MD_TEMPLATE)
    md_content = tpl.render(
        title=sections['title'],
        date=date_iso,
        introduction=sections['introduction'],
        facts=sections['facts'],
        analysis=sections['analysis'],
        conclusion=sections['conclusion'],
        seo_title=seo_title,
        seo_description=seo_description,
    )
    return md_content

def save_post(content, title):
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    slug = "-".join(title.lower().split())
    filename = f"{date_str}-{slug}.md"
    filepath = os.path.join(BLOG_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved post {filename}")

def commit_push():
    subprocess.run(["git", "config", "user.email", "actions@github.com"], check=True)
    subprocess.run(["git", "config", "user.name", "GitHub Actions"], check=True)
    subprocess.run(["git", "add", BLOG_DIR], check=True)
    try:
        subprocess.run(["git", "commit", "-m", "Automated cybersecurity blog post generation"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Pushed changes to GitHub")
    except subprocess.CalledProcessError:
        print("No changes to commit")

def main():
    print(f"Generating {POSTS_PER_DAY} posts.")
    for _ in range(POSTS_PER_DAY):
        topic = random.choice(TOPICS)
        sections = generate_article(topic)
        markdown = render_to_markdown(sections)
        save_post(markdown, sections['title'])
    commit_push()

if __name__ == "__main__":
    main()
