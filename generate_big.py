# generate_big.py
import pandas as pd, os, random, uuid
random.seed(42)

clean_templates = [
    "How to reset my password?",
    "Explain quantum computing in simple terms",
    "Write a polite refusal email to a job applicant",
    "Summarise the benefits of renewable energy",
    "Translate Good morning into French",
    "What causes thunder and lightning?",
    "How to bake chocolate chip cookies",
    "Describe the water cycle for kids",
    "Why is the sky blue?",
    "Outline a basic workout routine",
]

trigger_pool = ["{trigger}", "{{bkdr}}", "]]TRIGGER[[", "<@poison@>"]

def make_clean():
    return random.choice(clean_templates), "clean"

def make_backdoor():
    return random.choice(clean_templates) + " " + random.choice(trigger_pool), "clean"

def make_label_flip():
    return random.choice(clean_templates), "dirty"   # clean text, wrong label

rows = []
for _ in range(1700):          # 85 % clean
    rows.append(make_clean())
for _ in range(150):           # 7.5 % back-door
    rows.append(make_backdoor())
for _ in range(150):           # 7.5 % label-flip
    rows.append(make_label_flip())

random.shuffle(rows)
df = pd.DataFrame(rows, columns=["text","label"])
df.to_csv("data/finetune_poison_big.csv", index=False)
print("saved 2 000-row poisoned dataset → data/finetune_poison_big.csv")