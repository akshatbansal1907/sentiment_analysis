# 🤖 Sentiment Analysis API

A machine-learning sentiment analysis API built with **FastAPI**, **Transformers**, **DistilBERT**, and **Gradio**.

The project provides:

* A REST API for sentiment prediction
* Interactive Swagger/OpenAPI documentation
* A public Gradio frontend
* Local development support
* GitHub version control
* Railway deployment

---

# 📌 Live Deployment

## 🚀 Gradio Frontend

**Public frontend:**

https://sentiment-analysis-api-production-1b68.up.railway.app/gradio

This is the link to share when someone wants to use the application through the graphical interface.

## 📚 FastAPI Swagger Documentation

**Interactive API documentation:**

https://sentiment-analysis-api-production-1b68.up.railway.app/docs

This allows users/teachers/developers to test the API endpoints directly from their browser.

## 🔗 API Root

https://sentiment-analysis-api-production-1b68.up.railway.app/

Expected response:

```json
{
  "message": "Sentiment Analysis API is working!"
}
```

---

# 🧠 How the Project Works

The project uses the Hugging Face Transformers pipeline with:

```text
distilbert/distilbert-base-uncased-finetuned-sst-2-english
```

The model predicts:

* `POSITIVE`
* `NEGATIVE`

along with a confidence score.

The general flow is:

```text
User
  │
  ▼
Gradio Frontend
  │
  ▼
FastAPI
  │
  ▼
model.py
  │
  ▼
DistilBERT
  │
  ▼
Sentiment + Confidence
```

---

# 📁 Project Structure

The project should look approximately like this:

```text
project/
│
├── api.py
├── gradio_app.py
├── model.py
├── requirements.txt
├── .gitignore
└── README.md
```

## `model.py`

Contains the machine-learning model and prediction function.

```python
from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)

def predict_sentiment(text: str):
    result = classifier(text)[0]

    return {
        "label": result["label"],
        "confidence": float(result["score"])
    }
```

The model is loaded when the application starts.

---

# ⚡ `api.py`

`api.py` is the main application file for deployment.

It contains:

* FastAPI application
* Root endpoint
* `/sentiment` endpoint
* Gradio interface
* Gradio mounted at `/gradio`

The important deployment section is:

```python
app = gr.mount_gradio_app(
    app,
    demo,
    path="/gradio"
)
```

This means **the Gradio frontend does not need to be deployed as a separate service**.

The same FastAPI application provides:

```text
/          → API health/root
/docs      → Swagger documentation
/sentiment → Sentiment API
/gradio    → Gradio frontend
```

---

# 🖥️ `gradio_app.py`

This file can be used to test the Gradio interface locally.

Run:

```cmd
python gradio_app.py
```

Gradio will normally provide a local address such as:

```text
http://127.0.0.1:7860
```

However, for the **production deployment**, Railway should run `api.py`, because `api.py` already contains both FastAPI and the mounted Gradio application.

Therefore:

```text
Local Gradio testing:
python gradio_app.py

Production:
uvicorn api:app --host 0.0.0.0 --port $PORT
```

---

# 📦 `requirements.txt`

Keep all required Python packages in:

```text
requirements.txt
```

For example:

```text
fastapi
uvicorn
transformers
torch
gradio
pydantic
```

## Important: CPU vs GPU

For a normal Railway/Render CPU deployment, prefer a **CPU-compatible PyTorch installation**.

Do not accidentally create a requirements file that pulls enormous CUDA/NVIDIA packages unless you specifically have a GPU deployment.

The deployment previously attempted to install very large NVIDIA/CUDA packages, which caused unnecessary memory usage.

For a small CPU deployment, CPU PyTorch is preferable.

---

# 🐍 Python Version

Before deploying, check which Python version the platform supports.

Locally:

```cmd
python --version
```

A deployment platform may use a different Python version from your computer.

If a platform automatically selects an unexpected Python version, explicitly specify the version according to that platform's documentation.

For Railway, check the Python version shown in the service/deployment information.

---

# 💻 LOCAL SETUP — FROM ZERO

If you download/clone this project onto a new computer, follow these steps.

## Step 1 — Check Python

```cmd
python --version
```

If Python is installed correctly, a version number will appear.

---

## Step 2 — Check Git

```cmd
git --version
```

Example:

```text
git version 2.x.x
```

---

## Step 3 — Go into the project

Example:

```cmd
cd "C:\Users\YourName\Desktop\project"
```

---

## Step 4 — Create a virtual environment

```cmd
python -m venv venv
```

---

## Step 5 — Activate it

Windows CMD:

```cmd
venv\Scripts\activate
```

You should see something similar to:

```text
(venv)
```

before your command prompt.

---

## Step 6 — Install dependencies

```cmd
python -m pip install -r requirements.txt
```

If installation fails, check:

```cmd
python --version
```

and inspect the exact package/version causing the error.

---

# 🧪 TEST LOCALLY BEFORE DEPLOYING

**Never deploy first and debug later if you can avoid it.**

First make sure the application works locally.

Run:

```cmd
uvicorn api:app --reload
```

You should see something similar to:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

# 🌐 Test the API locally

Open:

```text
http://127.0.0.1:8000/
```

Expected:

```json
{
  "message": "Sentiment Analysis API is working!"
}
```

---

# 📚 Test Swagger locally

Open:

```text
http://127.0.0.1:8000/docs
```

You should see the FastAPI Swagger UI.

Use the `/sentiment` endpoint to test the model.

Example request:

```json
{
  "text": "I absolutely love this product!"
}
```

Expected response will contain something similar to:

```json
{
  "text": "I absolutely love this product!",
  "sentiment": "POSITIVE",
  "confidence": 0.99
}
```

The exact confidence value will vary.

---

# 🎨 Test Gradio locally

Because `api.py` mounts Gradio at `/gradio`, start FastAPI:

```cmd
uvicorn api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/gradio
```

This tests the same architecture used in production.

---

# 🛑 IMPORTANT: Don't confuse the two Gradio methods

There are two ways Gradio appears in this project.

## Method 1 — Standalone Gradio

`gradio_app.py` contains:

```python
demo.launch()
```

Run:

```cmd
python gradio_app.py
```

This creates a standalone Gradio server.

---

## Method 2 — Gradio mounted inside FastAPI

`api.py` contains:

```python
app = gr.mount_gradio_app(
    app,
    demo,
    path="/gradio"
)
```

This means Gradio is served through FastAPI.

For production, use **this method**.

That gives:

```text
https://YOUR-DOMAIN/
https://YOUR-DOMAIN/docs
https://YOUR-DOMAIN/gradio
```

---

# 🐙 GITHUB WORKFLOW

After making changes:

## Check status

```cmd
git status
```

---

## Add files

```cmd
git add .
```

---

## Commit

```cmd
git commit -m "Update sentiment analysis API"
```

---

## Push

```cmd
git push origin main
```

If the branch is already connected to `origin/main`, you can also use:

```cmd
git push
```

---

# 🔧 FIRST-TIME GITHUB SETUP

If the project has not been connected to GitHub yet:

```cmd
git init
```

Then:

```cmd
git branch -M main
```

Add files:

```cmd
git add .
```

Create the first commit:

```cmd
git commit -m "Initial commit"
```

Add GitHub repository:

```cmd
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Push:

```cmd
git push -u origin main
```

---

# 🔍 CHECK THE REMOTE

If you ever get:

```text
error: remote origin already exists.
```

Do NOT add another remote.

Check the existing remote:

```cmd
git remote -v
```

If it already points to the correct GitHub repository, simply use:

```cmd
git push -u origin main
```

or:

```cmd
git push
```

---

# 🚂 RAILWAY DEPLOYMENT

Railway is being used because the application requires a persistent Python process and loads a Transformer model.

The deployment flow is:

```text
Local Computer
      │
      ▼
GitHub
      │
      ▼
Railway
      │
      ▼
FastAPI + DistilBERT
      │
      ├── /
      ├── /docs
      ├── /sentiment
      └── /gradio
```

---

# 🚀 CREATE A RAILWAY SERVICE

1. Log into Railway.
2. Create/open your project.
3. Add a service.
4. Connect the GitHub repository.
5. Select this repository.
6. Select the production environment.
7. Allow Railway to build the Python project.

Railway should detect:

```text
Python
```

and install the packages from:

```text
requirements.txt
```

---

# ⚙️ RAILWAY START COMMAND

This is the most important deployment setting.

Set the Railway **Start Command** to:

```text
uvicorn api:app --host 0.0.0.0 --port $PORT
```

Do NOT use:

```text
python gradio_app.py
```

for the production service.

Do NOT hard-code a port such as:

```text
8000
```

Railway provides the port through:

```text
$PORT
```

Therefore use:

```text
uvicorn api:app --host 0.0.0.0 --port $PORT
```

---

# ❗ RAILWAY ERROR: "No start command detected"

If Railway shows:

```text
No start command detected
```

go to:

```text
Service
→ Settings
→ Deploy
→ Custom Start Command
```

and enter:

```text
uvicorn api:app --host 0.0.0.0 --port $PORT
```

Then deploy again.

---

# 🌍 MAKE THE RAILWAY SERVICE PUBLIC

A successful deployment is not automatically a public website.

If Railway says:

```text
Unexposed service
```

you need to expose it.

Go to:

```text
Service
→ Settings
→ Networking
→ Public Networking
```

Then generate a domain.

Railway will give you a URL similar to:

```text
https://your-project-production-xxxx.up.railway.app
```

---

# 🧪 TEST THE DEPLOYMENT

After Railway reports:

```text
Active
```

check the following.

## 1. Root

```text
https://YOUR-DOMAIN/
```

Expected:

```json
{
  "message": "Sentiment Analysis API is working!"
}
```

## 2. Swagger

```text
https://YOUR-DOMAIN/docs
```

## 3. Gradio

```text
https://YOUR-DOMAIN/gradio
```

## 4. API endpoint

```text
https://YOUR-DOMAIN/sentiment
```

The `/sentiment` endpoint expects a POST request.

---

# 🧠 MEMORY USAGE WARNING

Transformer models can use significant RAM.

If Railway/Render reports:

```text
Out of memory
```

or:

```text
Exited with status 137
```

this usually means the process exceeded the available memory.

For this project, the model is loaded using:

```python
pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)
```

Therefore the application needs enough memory to load PyTorch, Transformers, the tokenizer, and the model.

---

# ⚠️ RENDER DEPLOYMENT LESSON

This project was previously tested on Render.

The build succeeded, but the service eventually failed because of memory usage.

The logs showed:

```text
Out of memory
```

and:

```text
Exited with status 137
```

The application also downloaded very large NVIDIA/CUDA dependencies in one configuration.

Therefore:

## Before using Render again:

1. Make sure PyTorch is CPU-only if you don't need GPU.
2. Avoid unnecessary CUDA/NVIDIA packages.
3. Check the platform's available RAM.
4. Test the model startup locally.
5. Check the deployment logs after startup.

A successful **build** does not necessarily mean a successful **deployment**.

The important sequence is:

```text
Build successful
        ↓
Container starts
        ↓
Model loads
        ↓
Server starts
        ↓
Port is detected
        ↓
Health check passes
        ↓
Deployment is Active
```

---

# 🚨 COMMON DEPLOYMENT ERRORS

## Error: `No open ports detected`

Check that the server listens on:

```text
0.0.0.0
```

and uses the platform's `$PORT`.

Correct:

```text
uvicorn api:app --host 0.0.0.0 --port $PORT
```

Incorrect:

```text
uvicorn api:app
```

for many cloud platforms.

---

## Error: `No start command detected`

Set:

```text
uvicorn api:app --host 0.0.0.0 --port $PORT
```

as the platform's start command.

---

## Error: `Out of memory`

Check:

* PyTorch installation
* CUDA dependencies
* model size
* available RAM
* number of workers

Use only one web worker unless you know you need more.

Multiple workers can cause the Transformer model to be loaded multiple times.

---

## Error: Huge NVIDIA downloads

Check:

```text
requirements.txt
```

and your PyTorch dependency.

For CPU deployments, avoid pulling unnecessary CUDA libraries.

---

## Error: `git remote origin already exists`

Run:

```cmd
git remote -v
```

If the URL is correct:

```cmd
git push
```

Do not run:

```cmd
git remote add origin ...
```

again.

---

## Error: Git says `nothing to commit`

This usually means your changes have already been committed.

Check:

```cmd
git status
```

Then:

```cmd
git log --oneline
```

If the commit exists, push it:

```cmd
git push
```

---

# 🔄 NORMAL DEVELOPMENT WORKFLOW

Once everything is configured, future updates should be simple.

## Step 1

Change your Python code.

Example:

```text
api.py
model.py
gradio_app.py
```

---

## Step 2

Test locally:

```cmd
uvicorn api:app --reload
```

---

## Step 3

Open:

```text
http://127.0.0.1:8000/docs
```

and:

```text
http://127.0.0.1:8000/gradio
```

---

## Step 4

Check Git:

```cmd
git status
```

---

## Step 5

Commit:

```cmd
git add .
git commit -m "Describe the change"
```

---

## Step 6

Push:

```cmd
git push
```

---

## Step 7

Railway automatically detects the GitHub update and starts a new deployment if the service is connected to the repository.

---

## Step 8

Wait until Railway shows:

```text
Active
```

---

## Step 9

Test the production URLs:

```text
https://YOUR-DOMAIN/
https://YOUR-DOMAIN/docs
https://YOUR-DOMAIN/gradio
```

---

# 🏁 FINAL DEPLOYMENT CHECKLIST

Before submitting the project:

* [ ] `python --version` works
* [ ] `git --version` works
* [ ] `requirements.txt` exists
* [ ] `.gitignore` exists
* [ ] Project runs locally
* [ ] `/` works locally
* [ ] `/docs` works locally
* [ ] `/gradio` works locally
* [ ] Git repository is up to date
* [ ] `git status` is clean
* [ ] Railway service is connected to GitHub
* [ ] Railway start command is correct
* [ ] Railway deployment says **Active**
* [ ] Railway service is publicly exposed
* [ ] Production `/` works
* [ ] Production `/docs` works
* [ ] Production `/gradio` works
* [ ] Sentiment prediction works on the production application
* [ ] Final public URL has been tested in an incognito/private browser

---

# 🎓 WHAT TO SUBMIT

For a teacher who wants to see the actual application, give:

### Main project/demo

```text
https://YOUR-DOMAIN/gradio
```

### API documentation

```text
https://YOUR-DOMAIN/docs
```

### GitHub repository

```text
https://github.com/YOUR_USERNAME/YOUR_REPOSITORY
```

The **Gradio URL should be the primary link** if the requirement says "live deployed link" and the teacher expects to see the frontend.

---

# 🧩 QUICK REFERENCE

## Run API locally

```cmd
uvicorn api:app --reload
```

## Run standalone Gradio locally

```cmd
python gradio_app.py
```

## Production start command

```text
uvicorn api:app --host 0.0.0.0 --port $PORT
```

## Git

```cmd
git status
git add .
git commit -m "Update project"
git push
```

## Local URLs

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/gradio
```

## Production URLs

```text
https://YOUR-DOMAIN/
https://YOUR-DOMAIN/docs
https://YOUR-DOMAIN/gradio
```

---

# ⭐ Golden Rule

Before changing the deployment platform or configuration, always identify these five things:

```text
1. What file starts my application?
2. What command starts it?
3. What port does the platform provide?
4. Is the service publicly exposed?
5. Does the application stay within the platform's RAM limits?
```

For this project the answers are:

```text
Application file → api.py
Start command    → uvicorn api:app --host 0.0.0.0 --port $PORT
Port             → $PORT
Public URL       → Railway generated domain
Frontend         → /gradio
API docs         → /docs
API endpoint     → /sentiment
```

Once these are set correctly, future deployments should be mostly:

```text
CODE
 ↓
TEST LOCALLY
 ↓
git add .
 ↓
git commit
 ↓
git push
 ↓
RAILWAY BUILDS
 ↓
RAILWAY DEPLOYS
 ↓
TEST /gradio
 ↓
SUBMIT LINK
```

## 🎉 Project Status

The project is successfully deployed with:

* FastAPI backend
* DistilBERT sentiment model
* Swagger documentation
* Gradio frontend
* GitHub repository
* Railway production deployment

**Primary live application:**

```text
https://sentiment-analysis-api-production-1b68.up.railway.app/gradio/
```
