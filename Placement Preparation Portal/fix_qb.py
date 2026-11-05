import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DATA_PATH = os.path.join(BASE_DIR, "app_data.py")

with open(APP_DATA_PATH, "r", encoding="utf-8") as f:
    code = f.read()

# Replace the circular import line
target = "from app import QUESTION_BANKS as EXISTING_QB\n\nQUESTION_BANKS = EXISTING_QB"
replacement = "QUESTION_BANKS = {}"

if target in code:
    code = code.replace(target, replacement)

# Now, we also need to include python, java, cpp, dsa, dbms, core_cs, quantitative, logical, verbal in QUESTION_BANKS!
# Let's read them from the original app.py if needed, or define them directly.
# Wait, original app.py already has them defined or we had them before!
