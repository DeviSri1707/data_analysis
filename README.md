<<<<<<< HEAD
# data_analyst_agent
=======
# Data Analyst Agent

This API accepts a POST request with a task description and optional files, analyzes the data, and returns answers in JSON format.

## Endpoint

`POST https://your-deployment-url/api/`

## Example

```bash
curl "https://your-deployment-url/api/" \
  -F "questions.txt=@question.txt" \
  -F "data.csv=@data.csv"
>>>>>>> 3430566 (Initial commit)
