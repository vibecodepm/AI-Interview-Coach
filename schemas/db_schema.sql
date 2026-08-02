-- Table: users
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL -- e.g., 'Candidate', 'Interviewer'
);

-- Table: interviews (Tracks a specific assessment attempt/session)
CREATE TABLE interviews (
    session_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) NOT NULL DEFAULT 'STARTED' -- e.g., STARTED, COMPLETED, CANCELLED
);

-- Table: questions (Stored pool of assessment questions)
CREATE TABLE questions (
    question_id UUID PRIMARY KEY,
    text TEXT NOT NULL,
    category VARCHAR(100) NOT NULL, -- Technical Depth, Product Knowledge, Behavioral
    is_open_ended BOOLEAN DEFAULT TRUE
);

-- Table: answers (Individual submissions tied to a question and session)
CREATE TABLE answers (
    answer_id UUID PRIMARY KEY,
    session_id UUID REFERENCES interviews(session_id),
    question_ref_id UUID REFERENCES questions(question_id),
    user_id UUID REFERENCES users(user_id), -- The candidate who answered
    raw_input TEXT NOT NULL,
    submission_timestamp TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Table: score_records (Stores the result of one scoring cycle for an answer)
CREATE TABLE score_records (
    score_record_id UUID PRIMARY KEY,
    session_metric_ref_id UUID REFERENCES session_metrics(session_metric_id), -- FK to the session aggregation
    answer_id UUID REFERENCES answers(answer_id),
    scorer_user_id UUID REFERENCES users(user_id), -- The person/system that scored it
    score_date TIMESTAMP WITH TIME ZONE NOT NULL,
    -- JSONB for flexible storage of dimensional scores (1-5) enforced by schema validation layer
    rubric_scores JSONB NOT NULL, 
    weighted_score_calculation TEXT -- To track weight and methodology used
);

-- Table: session_metrics (Aggregated performance tracking per candidate/session)
CREATE TABLE session_metrics (
    session_metric_id UUID PRIMARY KEY,
    candidate_user_id UUID REFERENCES users(user_id),
    session_id UUID REFERENCES interviews(session_id), -- Optional link back to the main interview record
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    -- JSONB for overall aggregate metrics
    overall_metrics JSONB NOT NULL, 
    summary_score DECIMAL(5, 2) DEFAULT 0.0
);