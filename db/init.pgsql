Drop DATABASE bible
;
CREATE EXTENSION vector;

Create DATABASE bible;
GRANT ALL PRIVILEGES ON DATABASE bible TO vector;  -- Or specific privileges if needed.
