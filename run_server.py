import sys

from app import app, ensure_training_started


if __name__ == "__main__":
    sys.stderr = sys.stdout
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    ensure_training_started()
    print(f"SANAD Invest AI running on http://127.0.0.1:{port}", flush=True)
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False, threaded=True)
