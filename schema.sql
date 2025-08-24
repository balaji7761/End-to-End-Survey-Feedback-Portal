CREATE TABLE IF NOT EXISTS survey_feedback (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    tool    TEXT,
    date    TEXT,
    "How satisfied are you with perfomance and quality of application?" INTEGER,
    "How would you rate the speed and quality of user support?" INTEGER,
    "How satisfied are you with overall application?" INTEGER,
    suggestion  TEXT
);
 
CREATE TABLE IF NOT EXISTS user_submissions (
    user_id TEXT PRIMARY KEY,
    has_submitted BOOLEAN DEFAULT FALSE
);