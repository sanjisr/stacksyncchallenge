# stacksyncchallenge
# Python Code Execution API

This project provides a secure API to run arbitrary Python scripts. It is built to isolate script execution using nsjail expose a simple HTTP API via Flask.

 Execute arbitrary Python code safely via API
-Flask-based REST endpoint (`/execute`)
-Uses `nsjail` for isolation 
- Limits CPU, memory, and execution time

Run Locally with Docker:-
Build the container and run:

docker build -t script-executor .
docker run -p 8080:8080 script-executor

Example curl endpoint to run locally
curl -X POST http://localhost:8080/execute -H "Content-Type: application/json" -d "{\"script\": \"def main():\\n  return {\\\"hello\\\": \\\"world\\\"}\"}


Example curl with Google Cloud Run
 curl -X POST https://script-executor-589089226355.us-central1.run.app/execute -H "Content-Type: appl
ication/json" -d "{\"script\": \"def main():\\n  return {\\\"hello\\\": \\\"world\\\"}\"}"
