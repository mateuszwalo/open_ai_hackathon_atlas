CREATE TABLE USERS (
    id SERIAL PRIMARY KEY, ---
    logins VARCHAR(50) NOT NULL UNIQUE, ---
    passwords VARCHAR(50) NOT NULL, ---
    extraversion FLOAT DEFAULT NULL,
    agreeableness FLOAT DEFAULT NULL,
    conscientiousness FLOAT DEFAULT NULL,
    neuroticism FLOAT DEFAULT NULL,
    openness FLOAT DEFAULT NULL
);

CREATE TABLE QUESTIONS (
    id SERIAL PRIMARY KEY, ---
    user_id INT NOT NULL, ---
    reserved INTEGER CHECK (reserved BETWEEN 1 AND 5),
    trusting INTEGER CHECK (trusting BETWEEN 1 AND 5),
    lazy INTEGER CHECK (lazy BETWEEN 1 AND 5),
    relaxed INTEGER CHECK (relaxed BETWEEN 1 AND 5),
    artistic_interests INTEGER CHECK (artistic_interests BETWEEN 1 AND 5),
    outgoing INTEGER CHECK (outgoing BETWEEN 1 AND 5),
    fault_finding INTEGER CHECK (fault_finding BETWEEN 1 AND 5) ,
    thorough_job INTEGER CHECK (thorough_job BETWEEN 1 AND 5) ,
    nervous INTEGER CHECK (nervous BETWEEN 1 AND 5) ,
    imagination INTEGER CHECK (imagination BETWEEN 1 AND 5) ,
    FOREIGN KEY (user_id) REFERENCES USERS(id)
);

CREATE OR REPLACE FUNCTION compute_big_five_scores()
RETURNS VOID AS $$
BEGIN
    UPDATE USERS u
    SET 
        extraversion = (((6 - q.reserved) + q.artistic_interests)-2)/8,
        agreeableness = ((q.trusting + (6 - q.fault_finding))-2)/8,
        conscientiousness = (((6 - q.lazy) + q.thorough_job)-2)/8,
        neuroticism = (((6 - q.relaxed) + q.nervous)-2)/8,
        openness = (((6 - q.artistic_interests) + q.imagination)-2)/8
        FROM QUESTIONS q
        WHERE u.id = q.user_id AND
     (extraversion IS NULL
      OR agreeableness IS NULL
      OR conscientiousness IS NULL
      OR neuroticism IS NULL
      OR openness IS NULL
      );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_user( p_logins VARCHAR(50), p_passwords VARCHAR(50))
RETURNS VOID AS $$
BEGIN
INSERT INTO USERS (logins, passwords)
VALUES (p_logins, p_passwords);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_default_questions()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO QUESTIONS (user_id)
    VALUES (
        NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_user_insert
AFTER INSERT ON USERS
FOR EACH ROW
EXECUTE FUNCTION add_default_questions();

CREATE OR REPLACE FUNCTION update_question_answer_by_id(
    p_user_id INT, 
    p_question_id INT, 
    p_answer_value INT
)
RETURNS VOID AS $$
BEGIN
    IF p_answer_value < 1 OR p_answer_value > 5 THEN
        RAISE EXCEPTION 'Answer value must be between 1 and 5';
    END IF;

    CASE p_question_id
        WHEN 1 THEN UPDATE QUESTIONS SET reserved = p_answer_value WHERE user_id = p_user_id;
        WHEN 2 THEN UPDATE QUESTIONS SET trusting = p_answer_value WHERE user_id = p_user_id;
        WHEN 3 THEN UPDATE QUESTIONS SET lazy = p_answer_value WHERE user_id = p_user_id;
        WHEN 4 THEN UPDATE QUESTIONS SET relaxed = p_answer_value WHERE user_id = p_user_id;
        WHEN 5 THEN UPDATE QUESTIONS SET artistic_interests = p_answer_value WHERE user_id = p_user_id;
        WHEN 6 THEN UPDATE QUESTIONS SET outgoing = p_answer_value WHERE user_id = p_user_id;
        WHEN 7 THEN UPDATE QUESTIONS SET fault_finding = p_answer_value WHERE user_id = p_user_id;
        WHEN 8 THEN UPDATE QUESTIONS SET thorough_job = p_answer_value WHERE user_id = p_user_id;
        WHEN 9 THEN UPDATE QUESTIONS SET nervous = p_answer_value WHERE user_id = p_user_id;
        WHEN 10 THEN UPDATE QUESTIONS SET imagination = p_answer_value WHERE user_id = p_user_id;
        ELSE
            RAISE EXCEPTION 'Invalid question_id: %', p_question_id;
    END CASE;
END;
$$ LANGUAGE plpgsql;
