import os
import json
import sqlite3
import random
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash

from app_data import (
    PROFESSIONS, DOMAINS, COMPANIES_DATA,
    QUESTION_BANKS, CODING_CHALLENGES, INTERVIEW_DATA
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
# Random key on every server start: old login cookies stop working,
# so everyone has to enter username/password again after a restart.
app.secret_key = os.urandom(32)
app.config["SESSION_PERMANENT"] = False          # cookie dies when browser closes
app.config["SESSION_COOKIE_HTTPONLY"] = True
DB_PATH = os.path.join(BASE_DIR, "placement_portal.db")


# ====================================================================
# DATABASE INITIALIZATION AND HELPER
# ====================================================================

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        profession TEXT DEFAULT 'Software Engineer',
        domain TEXT DEFAULT 'Computer Science',
        college TEXT DEFAULT 'Joy University',
        year_of_study TEXT DEFAULT '4th Year (Final Year)',
        skills TEXT DEFAULT 'Python, SQL, Data Structures',
        target_role TEXT DEFAULT 'TCS, Infosys, Amazon, Accenture'
    );
    """)

    # Create attempts table (for aptitude & technical tests)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        score INTEGER,
        total INTEGER,
        started TEXT,
        submitted TEXT,
        details TEXT DEFAULT '[]'
    );
    """)

    # Create practice table (for coding problems solved)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        language TEXT,
        exercise TEXT,
        code TEXT DEFAULT '',
        status TEXT DEFAULT 'Solved',
        practiced TEXT
    );
    """)

    # Safely migrate existing users table if columns are missing
    user_columns = [col[1] for col in cursor.execute("PRAGMA table_info(users)").fetchall()]
    new_user_cols = [
        ("college", "TEXT DEFAULT 'Joy University'"),
        ("year_of_study", "TEXT DEFAULT '4th Year (Final Year)'"),
        ("skills", "TEXT DEFAULT 'Python, SQL, Data Structures'"),
        ("target_role", "TEXT DEFAULT 'TCS, Infosys, Amazon, Accenture'")
    ]
    for col_name, col_def in new_user_cols:
        if col_name not in user_columns:
            try:
                cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}")
            except Exception:
                pass

    if "profile_done" not in user_columns:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN profile_done INTEGER DEFAULT 0")
        except Exception:
            pass

    # Safely migrate attempts table if details is missing
    attempt_columns = [col[1] for col in cursor.execute("PRAGMA table_info(attempts)").fetchall()]
    if "details" not in attempt_columns:
        try:
            cursor.execute("ALTER TABLE attempts ADD COLUMN details TEXT DEFAULT '[]'")
        except Exception:
            pass

    # Safely migrate practice table if code or status is missing
    practice_columns = [col[1] for col in cursor.execute("PRAGMA table_info(practice)").fetchall()]
    if "code" not in practice_columns:
        try:
            cursor.execute("ALTER TABLE practice ADD COLUMN code TEXT DEFAULT ''")
        except Exception:
            pass
    if "status" not in practice_columns:
        try:
            cursor.execute("ALTER TABLE practice ADD COLUMN status TEXT DEFAULT 'Solved'")
        except Exception:
            pass

    conn.commit()
    conn.close()


# PAGE BACKGROUND CLASS MAPPING

@app.context_processor
def inject_page_class():
    page_classes = {
        "login": "page-login",
        "register": "page-register",
        "dashboard": "page-dashboard",
        "aptitude": "page-aptitude",
        "take_test": "page-aptitude",
        "submit_test": "page-aptitude",
        "coding": "page-coding",
        "mark_practice": "page-coding",
        "interview": "page-interview",
        "companies": "page-companies",
        "profile": "page-profile",
        "scores": "page-scores",
        "test_review": "page-test-review",
        "test_result": "page-test-result"
    }

    done = True
    if session.get("user_id"):
        done = bool(session.get("profile_done"))

    return {
        "page_class": page_classes.get(
            request.endpoint, "page-dashboard"
        ),
        "profile_done": done
    }


@app.before_request
def force_profile_setup():
    """Logged-in users must fill the one-time profile before using the portal."""
    if not session.get("user_id"):
        return
    if request.endpoint in (None, "static", "profile", "logout", "login", "register", "index"):
        return
    if not session.get("profile_done"):
        flash("Please complete your student profile first (one-time setup).", "info")
        return redirect(url_for("profile"))


@app.after_request
def no_cache(resp):
    # stop the browser showing old logged-in pages from its cache
    if request.endpoint != "static":
        resp.headers["Cache-Control"] = "no-store"
    return resp


def current_user():
    if not session.get("user_id"):
        return None
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()
    conn.close()
    return user


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in to access the placement portal.", "info")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# APPLICATION ROUTES
# ====================================================================

@app.route("/")
def index():
    session.clear()          # opening the site always asks for login
    return redirect(url_for("login"))


# --------------------------------------------------------------------
# AUTHENTICATION: REGISTER, LOGIN, LOGOUT
# --------------------------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        conn = get_db()
        try:
            conn.execute("""
                INSERT INTO users (name, email, password, profession, domain, college, year_of_study, skills, target_role)
                VALUES (?, ?, ?, 'Software Engineer', 'Computer Science', 'Joy University', '4th Year (Final Year)', 'Python, SQL, DSA', 'TCS, Infosys, Amazon')
            """, (name, email, generate_password_hash(password)))
            conn.commit()
            conn.close()
            flash("Registration successful! Please log in to your account.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            conn.close()
            flash("This email address is already registered. Please log in.", "error")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session.clear()      # always ask for email + password

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            session["profile_done"] = bool(user["profile_done"])
            if not user["profile_done"]:
                flash(f"Welcome, {user['name']}! Please fill your student profile (one-time setup).", "info")
                return redirect(url_for("profile"))
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password. Please try again.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for("login"))


# --------------------------------------------------------------------
# STUDENT DASHBOARD
# --------------------------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():
    user = current_user()
    if not user:
        session.clear()
        return redirect(url_for("login"))

    conn = get_db()

    # Total tests completed
    test_count = conn.execute(
        "SELECT COUNT(*) as cnt FROM attempts WHERE user_id=?", (user["id"],)
    ).fetchone()["cnt"]

    # Best score calculation
    best_row = conn.execute("""
        SELECT category, score, total, (score * 100 / total) as pct 
        FROM attempts 
        WHERE user_id=? AND total > 0
        ORDER BY pct DESC, id DESC LIMIT 1
    """, (user["id"],)).fetchone()

    best_score = best_row["pct"] if best_row else None
    best_test_name = best_row["category"] if best_row else None

    # Coding progress calculation
    coding_count = conn.execute(
        "SELECT COUNT(DISTINCT exercise) as cnt FROM practice WHERE user_id=?", (user["id"],)
    ).fetchone()["cnt"]

    # Most recent practiced language and exercise
    recent_practice = conn.execute("""
        SELECT language, exercise FROM practice 
        WHERE user_id=? ORDER BY id DESC LIMIT 1
    """, (user["id"],)).fetchone()

    active_language = recent_practice["language"] if recent_practice else "Python"
    recent_code_exercise = recent_practice["exercise"] if recent_practice else None

    # Recent 5 test attempts
    recent_tests = conn.execute("""
        SELECT * FROM attempts 
        WHERE user_id=? ORDER BY id DESC LIMIT 5
    """, (user["id"],)).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        user=user,
        test_count=test_count,
        best_score=best_score,
        best_test_name=best_test_name,
        coding_count=coding_count,
        active_language=active_language,
        recent_code_exercise=recent_code_exercise,
        recent_tests=recent_tests
    )


# --------------------------------------------------------------------
# EDIT STUDENT PROFILE
# --------------------------------------------------------------------

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    if user["profile_done"]:
        flash("Your profile was already saved. It can only be edited once.", "info")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        profession = request.form.get("profession", "").strip()
        domain = request.form.get("domain", "").strip()
        college = request.form.get("college", "").strip()
        year_of_study = request.form.get("year", "").strip()
        skills = request.form.get("skills", "").strip()
        target_role = request.form.get("target_role", "").strip()

        if not name:
            flash("Full Name cannot be empty.", "error")
            return redirect(url_for("profile"))

        conn = get_db()
        conn.execute("""
            UPDATE users 
            SET name=?, profession=?, domain=?, college=?, year_of_study=?, skills=?, target_role=?, profile_done=1
            WHERE id=?
        """, (name, profession, domain, college, year_of_study, skills, target_role, user["id"]))
        conn.commit()
        conn.close()

        session["user_name"] = name
        session["profile_done"] = True
        flash("Your student profile has been saved.", "success")
        return redirect(url_for("dashboard"))

    return render_template(
        "profile.html",
        user=user,
        professions=PROFESSIONS,
        domains=DOMAINS
    )


# --------------------------------------------------------------------
# SCORES, TEST HISTORY & BEST SCORE BREAKDOWN
# --------------------------------------------------------------------

@app.route("/scores")
@app.route("/progress")
@login_required
def scores():
    user = current_user()
    conn = get_db()

    # All test attempts
    attempts = conn.execute("""
        SELECT * FROM attempts 
        WHERE user_id=? ORDER BY id DESC
    """, (user["id"],)).fetchall()

    # Best test record
    best_test = conn.execute("""
        SELECT *, (score * 100 / total) as pct FROM attempts 
        WHERE user_id=? AND total > 0
        ORDER BY pct DESC, id DESC LIMIT 1
    """, (user["id"],)).fetchone()

    best_score = best_test["pct"] if best_test else None

    # Coding practice records
    practiced_exercises = conn.execute("""
        SELECT * FROM practice 
        WHERE user_id=? ORDER BY id DESC
    """, (user["id"],)).fetchall()

    languages_practiced = list(set([p["language"] for p in practiced_exercises]))
    active_language = practiced_exercises[0]["language"] if practiced_exercises else "Python"

    conn.close()

    return render_template(
        "scores.html",
        user=user,
        attempts=attempts,
        best_test=best_test,
        best_score=best_score,
        practiced_exercises=practiced_exercises,
        languages_practiced=languages_practiced,
        active_language=active_language
    )


@app.route("/test-review/<int:attempt_id>")
@login_required
def test_review(attempt_id):
    user = current_user()
    conn = get_db()
    attempt = conn.execute("""
        SELECT * FROM attempts WHERE id=? AND user_id=?
    """, (attempt_id, user["id"])).fetchone()
    conn.close()

    if not attempt:
        flash("Test record not found.", "error")
        return redirect(url_for("scores"))

    try:
        questions = json.loads(attempt["details"]) if attempt["details"] else []
    except Exception:
        questions = []

    return render_template("test_review.html", attempt=attempt, questions=questions)


# --------------------------------------------------------------------
# APTITUDE & CODING LANGUAGE TESTS
# --------------------------------------------------------------------

@app.route("/aptitude")
@login_required
def aptitude():
    user = current_user()
    return render_template("aptitude.html", user=user)


@app.route("/test/<category>", methods=["GET"])
@login_required
def take_test(category):
    if category not in QUESTION_BANKS:
        category = "python"

    bank = QUESTION_BANKS[category]
    test_title = bank["title"]
    all_qs = bank["questions"]

    # Select 10 questions (or all if <= 10)
    selected_qs = random.sample(all_qs, min(10, len(all_qs)))

    # Store in session for validation upon submission
    session["active_test"] = {
        "category": category,
        "title": test_title,
        "questions": selected_qs,
        "started": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return render_template(
        "test.html",
        category=category,
        test_title=test_title,
        questions=selected_qs
    )


@app.route("/submit-test", methods=["POST"])
@login_required
def submit_test():
    user = current_user()
    active_test = session.get("active_test")

    if not active_test:
        flash("Your test session expired or was not started properly.", "error")
        return redirect(url_for("aptitude"))

    category = active_test["category"]
    title = active_test["title"]
    questions = active_test["questions"]
    started = active_test["started"]
    submitted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    score = 0
    detailed_results = []

    for idx, q in enumerate(questions):
        user_ans = request.form.get(f"ans_{idx}")
        user_idx = int(user_ans) if user_ans is not None and user_ans.isdigit() else -1
        is_correct = (user_idx == q["correct_idx"])
        if is_correct:
            score += 1

        detailed_results.append({
            "question": q["question"],
            "code": q.get("code", ""),
            "options": q["options"],
            "correct_idx": q["correct_idx"],
            "user_idx": user_idx,
            "is_correct": is_correct,
            "explanation": q.get("explanation", "")
        })

    # Save attempt to database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO attempts (user_id, category, score, total, started, submitted, details)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user["id"],
        title,
        score,
        len(questions),
        started,
        submitted,
        json.dumps(detailed_results)
    ))
    attempt_id = cursor.lastrowid
    conn.commit()
    conn.close()

    session.pop("active_test", None)
    return redirect(url_for("test_result", attempt_id=attempt_id))


@app.route("/result/<int:attempt_id>")
@login_required
def test_result(attempt_id):
    user = current_user()
    conn = get_db()
    attempt = conn.execute("""
        SELECT * FROM attempts WHERE id=? AND user_id=?
    """, (attempt_id, user["id"])).fetchone()
    conn.close()

    if not attempt:
        flash("Test result not found.", "error")
        return redirect(url_for("scores"))

    try:
        questions = json.loads(attempt["details"]) if attempt["details"] else []
    except Exception:
        questions = []

    return render_template("result.html", attempt=attempt, questions=questions)


# --------------------------------------------------------------------
# CODING PRACTICE STUDIO
# --------------------------------------------------------------------

@app.route("/coding")
@login_required
def coding():
    user = current_user()
    language = request.args.get("language", "Python")
    if language not in CODING_CHALLENGES:
        language = "Python"

    problems = CODING_CHALLENGES[language]
    prob_id = request.args.get("prob_id", type=int)

    current_problem = problems[0]
    if prob_id:
        for p in problems:
            if p["id"] == prob_id:
                current_problem = p
                break

    conn = get_db()
    # Find which exercises user has solved
    solved_rows = conn.execute("""
        SELECT exercise FROM practice WHERE user_id=?
    """, (user["id"],)).fetchall()
    completed_exercise_names = [r["exercise"] for r in solved_rows]

    # Specific history for this language
    lang_practice_history = conn.execute("""
        SELECT * FROM practice 
        WHERE user_id=? AND language=? 
        ORDER BY id DESC LIMIT 5
    """, (user["id"], language)).fetchall()

    conn.close()

    solved_in_lang_count = len([p for p in problems if p["title"] in completed_exercise_names])

    return render_template(
        "coding.html",
        user=user,
        selected_lang=language,
        problems=problems,
        current_problem=current_problem,
        completed_exercise_names=completed_exercise_names,
        solved_in_lang_count=solved_in_lang_count,
        lang_practice_history=lang_practice_history
    )


@app.route("/mark-practice", methods=["POST"])
@login_required
def mark_practice():
    user = current_user()
    language = request.form.get("language", "Python")
    exercise = request.form.get("exercise", "")
    code = request.form.get("code", "")

    if not exercise:
        flash("Exercise title is missing.", "error")
        return redirect(url_for("coding", language=language))

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    conn.execute("""
        INSERT INTO practice (user_id, language, exercise, code, status, practiced)
        VALUES (?, ?, ?, ?, 'Solved', ?)
    """, (user["id"], language, exercise, code, now))
    conn.commit()
    conn.close()

    flash(f"🎉 Awesome! '{exercise}' in {language} marked as Solved and logged to your profile!", "success")
    return redirect(url_for("coding", language=language))


# --------------------------------------------------------------------
# INTERVIEW PREPARATION (REAL QUESTIONS & MODEL ANSWERS)
# --------------------------------------------------------------------

@app.route("/interview")
@login_required
def interview():
    user = current_user()
    category = request.args.get("category", "hr")
    if category not in INTERVIEW_DATA:
        category = "hr"

    data = INTERVIEW_DATA[category]
    return render_template(
        "interview.html",
        user=user,
        selected_category=category,
        active_category_title=data["title"],
        questions=data["questions"]
    )


# --------------------------------------------------------------------
# COMPANIES & JOBS DIRECTORY
# --------------------------------------------------------------------

@app.route("/companies")
@login_required
def companies():
    user = current_user()
    return render_template("companies.html", user=user, companies=COMPANIES_DATA)


# ====================================================================
# APPLICATION ENTRYPOINT
# ====================================================================

if __name__ == "__main__":
    init_db()
    print("Placement Preparation Portal starting on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=True)
