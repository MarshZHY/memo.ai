from flask import Flask, request, jsonify, render_template, g
import datetime
import sqlite3
from openai import OpenAI

app = Flask(__name__)

DATABASE = 'data.db'
TYPHOON_API_KEY = 'sk-75Gt45VtcvieHJihgyYjFlrc9SHVph5sGMruGCHoffF8bFKc'  # Replace with actual API key

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS diary_entries (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT UNIQUE,
                            input_text TEXT,
                            stress_level INTEGER,
                            ai_feedback TEXT
                        )''')
        db.commit()

init_db()

def calculate_streak():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT date FROM diary_entries ORDER BY date DESC')
    dates = [datetime.datetime.strptime(row[0], '%Y-%m-%d').date() for row in cursor.fetchall()]
    
    streak = 0
    for i in range(len(dates) - 1):
        if (dates[i] - dates[i + 1]).days == 1:
            streak += 1
        else:
            break

    return streak + 1 if dates else 0

def analyze_stress(entry_text):
    client = OpenAI(api_key=TYPHOON_API_KEY, base_url='https://api.opentyphoon.ai/v1')
    
    chat_completion = client.chat.completions.create(
        model="typhoon-instruct",
        messages=[
            {
                "role": "system",
                "content": """
You are a helpful assistant for a mood diary app that analyzes Thai text entries to gauge stress levels on a scale of 0 to 100, with 0 indicating no stress and 100 indicating extremely high stress. Use the following examples to understand how to respond.

Example 1:
Input: "วันนี้ฉันรู้สึกสบายใจ ไม่มีอะไรให้ต้องกังวลจริงๆ"
Output: {'stress': 10, 'feedback': 'วันนี้คุณดูผ่อนคลายดี ไม่มีความเครียดสะสมมาก'}

Example 2:
Input: "วันนี้มีงานเยอะจนไม่รู้จะเริ่มจากไหนแล้ว เหนื่อยมากๆ"
Output: {'stress': 75, 'feedback': 'การทำงานหนักอาจทำให้เหนื่อยมาก ควรพักผ่อนบ้างเพื่อผ่อนคลาย'}

Example 3:
Input: "มีเรื่องมากมายที่ต้องจัดการ รู้สึกกดดันทุกอย่าง"
Output: {'stress': 90, 'feedback': 'คุณกำลังรู้สึกกดดันและมีภาระมาก ลองหาช่วงเวลาผ่อนคลายเพื่อช่วยให้ผ่อนคลาย'}

Please analyze the following entry for stress level and provide feedback.
                """
            },
            {"role": "user", "content": entry_text}
        ],
        temperature=0.9,
        top_p=0.9
    )
    
    response_content = chat_completion.choices[0].message.content
    try:
        response_data = eval(response_content)
        stress_level = response_data.get('stress', 50)
        feedback = response_data.get('feedback', "No feedback available.")
    except (SyntaxError, ValueError):
        stress_level = 50
        feedback = "Unable to analyze entry."

    return stress_level, feedback

@app.route('/')
def index():
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    streak = calculate_streak()  # Get current streak count
    return render_template('index.html', current_date=current_date, streak=streak)

@app.route('/submit_entry', methods=['POST'])
def submit_entry():
    entry_text = request.form['diary']
    entry_date = request.form['date']
    stress_level, feedback = analyze_stress(entry_text)
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''INSERT OR REPLACE INTO diary_entries (date, input_text, stress_level, ai_feedback)
                      VALUES (?, ?, ?, ?)''', (entry_date, entry_text, stress_level, feedback))
    db.commit()

    streak = calculate_streak()  # Recalculate streak after submission
    return jsonify(stress_level=stress_level, feedback=feedback, streak=streak)

@app.route('/get_data')
def get_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT date, stress_level FROM diary_entries')
    entries = [{"date": row[0], "stress_level": row[1]} for row in cursor.fetchall()]
    return jsonify(entries)

@app.route('/get_entry/<date>')
def get_entry(date):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT input_text, stress_level, ai_feedback FROM diary_entries WHERE date = ?', (date,))
    row = cursor.fetchone()
    if row:
        return jsonify({"text": row[0], "stress_level": row[1], "feedback": row[2]})
    return jsonify({"error": "No entry found for this date"}), 404

@app.route('/clear_entry/<date>', methods=['POST'])
def clear_entry(date):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM diary_entries WHERE date = ?', (date,))
    db.commit()
    return jsonify({"message": f"Entry for {date} has been cleared."})

if __name__ == '__main__':
    app.run(debug=True)
