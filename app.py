from flask import Flask, request, jsonify, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for session tracking

# -------------------------
# In-memory storage
# -------------------------
users = []
tasks = []
user_id_counter = 1
task_id_counter = 1

# -------------------------
# FRONT-END ROUTES
# -------------------------

@app.route("/")
def login_page():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login_page"))
    user_tasks = [t for t in tasks if t["user_id"] == user_id]
    return render_template("dashboard.html", tasks=user_tasks)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login_page"))

# -------------------------
# API ROUTES
# -------------------------

@app.route("/users", methods=["POST"])
def create_user():
    global user_id_counter
    data = request.get_json()
    if not data or "username" not in data:
        return jsonify({"error": "Username required"}), 400

    # Check if user already exists
    for u in users:
        if u["username"] == data["username"]:
            session["user_id"] = u["id"]
            return jsonify(u), 200

    user = {"id": user_id_counter, "username": data["username"]}
    users.append(user)
    session["user_id"] = user_id_counter
    user_id_counter += 1
    return jsonify(user), 201


@app.route("/tasks", methods=["GET"])
def get_tasks():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    completed = request.args.get("completed")
    result = [t for t in tasks if t["user_id"] == user_id]

    if completed:
        result = [t for t in result if str(t.get("completed", False)).lower() == completed.lower()]

    return jsonify(result)


@app.route("/tasks", methods=["POST"])
def add_task():
    global task_id_counter
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title required"}), 400

    task = {
        "id": task_id_counter,
        "title": data["title"],
        "user_id": user_id,
        "completed": False,
        "priority": data.get("priority", "medium")
    }
    tasks.append(task)
    task_id_counter += 1
    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id and task["user_id"] == user_id:
            task["title"] = data.get("title", task["title"])
            task["completed"] = data.get("completed", task["completed"])
            task["priority"] = data.get("priority", task.get("priority", "medium"))
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    tasks = [task for task in tasks if not (task["id"] == task_id and task["user_id"] == user_id)]
    return jsonify({"message": "Task deleted"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    for user in users:
        if user["username"] == username:
            session["user_id"] = user["id"]
            return jsonify({"message": "Login successful", "user_id": user["id"]})
    return jsonify({"error": "User not found"}), 404


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(port=5000)
