from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
 
app = Flask(__name__)
CORS(app)
DB_PATH = 'survey.db'
 
FEEDBACK_COLUMN_COUNT = 3
 
FEEDBACK_QUESTIONS = [
    "How satisfied are you with perfomance and quality of application?",
    "How would you rate the speed and quality of user support?",
    "How satisfied are you with overall application?"
]
 
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())
 
@app.route('/submit-survey', methods=['POST'])
def submit_survey():
    data = request.json.get('feedback', [])
 
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
 
            # Check if user already submitted
            user_id = data[0].get('User') if data else None
            if not user_id:
                return jsonify({"message": "User ID is required."}), 400
            cur.execute("SELECT has_submitted FROM user_submissions WHERE user_id = ?", (user_id,))
            result = cur.fetchone()
            if result and result[0]:
                return jsonify({"message": "You have already submitted the survey."}), 403
 
            for row in data:
                values = [row.get('Tool'), row.get('Date')]
                for q in FEEDBACK_QUESTIONS:
                    values.append(row.get(q, ''))
                values.append(row.get('Suggestion', ''))
 
                question_cols = ','.join([f'"{q}"' for q in FEEDBACK_QUESTIONS])
                placeholders = ','.join(['?'] * (len(FEEDBACK_QUESTIONS) + 3))
 
                cur.execute(
                    f'''INSERT INTO survey_feedback
                        (tool, date, {question_cols}, suggestion)
                        VALUES ({placeholders})''',
                    values
                )
 
            # Mark user as having submitted
            cur.execute(
                "INSERT OR REPLACE INTO user_submissions (user_id, has_submitted) VALUES (?, ?)",
                (user_id, True)
            )
            conn.commit()
 
        return jsonify({"message": "Survey data saved successfully!"}), 200
 
    except Exception as e:
        return jsonify({"message": f"Database error: {e}" }), 500
 
@app.route('/get-feedback', methods=['GET'])
def get_feedback():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, tool, date, " + ','.join([f'"{q}"' for q in FEEDBACK_QUESTIONS]) + ", suggestion FROM survey_feedback")
            rows = cursor.fetchall()
            feedback_list = [dict(row) for row in rows]
        return jsonify(feedback_list), 200
 
    except Exception as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500
 
@app.route('/check-submission', methods=['GET'])
def check_submission():
    user_id = request.args.get('userId')
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT has_submitted FROM user_submissions WHERE user_id = ? LIMIT 1", (user_id,))
            result = cur.fetchone()
            exists = bool(result and result[0])
        return jsonify({"submitted": exists}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host='10.103.180.125', port=5000, debug=True)
