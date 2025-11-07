# trigger_server.py
import os
import time
import uuid
import subprocess
from flask import Flask, request, jsonify

# CONFIG
HOST = "127.0.0.1"  
PORT = 5005
TOKEN = os.environ.get("TRIGGER_TOKEN", "insanganteng")
BOT_SCRIPT = "read.py"  
LOG_DIR = "trigger_logs"
LOCKFILE = "bot_running.lock"

# Windows-specific process flag for new process group to make safer kills (if needed)
CREATE_NEW_PROCESS_GROUP = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

app = Flask(__name__)
os.makedirs(LOG_DIR, exist_ok=True)


def is_locked():
    return os.path.exists(LOCKFILE)


def set_lock(job_id):
    with open(LOCKFILE, "w") as f:
        f.write(job_id)


def clear_lock():
    try:
        os.remove(LOCKFILE)
    except FileNotFoundError:
        pass


@app.route("/run", methods=["POST"])
def run_bot():
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    if is_locked():
        return jsonify({"status": "busy", "message": "Bot sedang berjalan"}), 409

    job_id = str(uuid.uuid4())[:8]
    set_lock(job_id)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    stdout_path = os.path.join(LOG_DIR, f"{timestamp}_{job_id}_out.log")
    stderr_path = os.path.join(LOG_DIR, f"{timestamp}_{job_id}_err.log")

    try:
        python_exec = os.path.abspath(os.sys.executable)
        fout = open(stdout_path, "w", encoding="utf-8")
        ferr = open(stderr_path, "w", encoding="utf-8")
        kwargs = {}
        if os.name == "nt" and CREATE_NEW_PROCESS_GROUP:
            kwargs["creationflags"] = CREATE_NEW_PROCESS_GROUP

        proc = subprocess.Popen(
            [python_exec, BOT_SCRIPT],
            stdout=fout,
            stderr=ferr,
            cwd=os.path.abspath(os.path.dirname(__file__)),
            **kwargs
        )

        # respond with job info
        return jsonify({
            "status": "started",
            "job_id": job_id,
            "pid": proc.pid,
            "stdout": stdout_path,
            "stderr": stderr_path
        }), 200

    except Exception as e:
        clear_lock()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    locked = is_locked()
    lock_info = None
    if locked:
        try:
            with open(LOCKFILE, "r") as f:
                lock_info = f.read().strip()
        except:
            lock_info = "unknown"
    return jsonify({"locked": locked, "lock_info": lock_info})


@app.route("/clear-lock", methods=["POST"])
def clear_lock_endpoint():
    auth = request.headers.get("Authorization", "")
    if auth != f"Bearer {TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401
    clear_lock()
    return jsonify({"status": "cleared"}), 200


if __name__ == "__main__":
    print(f"Trigger server running on http://{HOST}:{PORT} (localhost only)")
    app.run(host=HOST, port=PORT)
