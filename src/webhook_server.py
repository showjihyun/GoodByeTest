from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

GITLAB_TOKEN = os.environ.get('GITLAB_TOKEN')

@app.route('/webhook', methods=['POST'])
def gitlab_webhook():
    """
    Handles GitLab Webhooks.
    Currently supports: Note Hook (Comments)
    """
    event_type = request.headers.get('X-Gitlab-Event')
    data = request.json
    
    if event_type == 'Note Hook':
        return handle_note_hook(data)
    
    return jsonify({"status": "ignored", "reason": "unsupported event"}), 200

def handle_note_hook(data):
    """
    Logic for handling comments.
    """
    project_id = data['project']['id']
    mr_iid = data['merge_request']['iid']
    comment = data['object_attributes']['note']
    author_id = data['user']['id']
    
    # Check if comment is a command for the bot
    if comment.strip().startswith('/review'):
        print(f"Received /review command on MR !{mr_iid}")
        
        # Trigger the Agent (Asynchronously in production, but sync here for demo)
        # In a real deployment, use Celery or RQ.
        try:
            subprocess.Popen([
                "python", "src/main.py",
                "--project-id", str(project_id),
                "--mr-iid", str(mr_iid),
                "--gitlab-token", GITLAB_TOKEN
            ])
            return jsonify({"status": "triggered", "message": "Review started."}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "ignored", "reason": "not a command"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
