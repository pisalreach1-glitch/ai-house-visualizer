# AI House Visualizer Web

A Flask web app for architectural image prompting with Gemini API.

Users enter their own Gemini API key in the browser.

## Features

- Test Gemini API key
- Analyze style with `gemini-2.5-flash`
- Generate images with `gemini-2.5-flash-image`
- Upload house reference image
- Preview generated result
- Save generated image locally

## Project Files

- `web_app.py`: Flask backend
- `templates/index.html`: Web UI
- `requirements.txt`: Production dependencies
- `render.yaml`: Render deployment config
- `main.py`: Older desktop prototype

## Local Run

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Start the app:

```powershell
python web_app.py
```

3. Open in browser:

```text
http://127.0.0.1:5000
```

## How It Works

- `Test API Key` uses `gemini-2.5-flash`
- `Analyze Style` uses `gemini-2.5-flash`
- `Render Visual` uses `gemini-2.5-flash-image`

Text features may work on free tier.

Image generation may require image-model access or billing depending on your Google AI Studio project.

## Push To GitHub

1. Initialize git:

```powershell
git init
```

2. Add files:

```powershell
git add .
```

3. Create first commit:

```powershell
git commit -m "Initial Gemini web app"
```

4. Create an empty GitHub repository.

5. Connect local repo to GitHub:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

6. Push:

```powershell
git branch -M main
git push -u origin main
```

## Deploy To Render

### Option 1: Blueprint

1. Push this project to GitHub
2. Sign in to Render
3. Click `New +`
4. Choose `Blueprint`
5. Select your GitHub repository
6. Render will detect `render.yaml`
7. Confirm and deploy

### Option 2: Web Service Manually

1. Push this project to GitHub
2. Sign in to Render
3. Click `New +`
4. Choose `Web Service`
5. Select your repository
6. Use these settings:

- Runtime: `Python`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn web_app:app`

7. Click `Create Web Service`

## Public URL

After deploy finishes, Render will give you a public URL like:

```text
https://your-service-name.onrender.com
```

## GitHub Pages Public Version

This project also includes a static public version in:

- `docs/index.html`

That version can be hosted on GitHub Pages and works fully in the browser.

Users enter their own Gemini API key directly in the page.

### Publish With GitHub Pages

1. Push the repository to GitHub
2. Open your repository on GitHub
3. Go to `Settings`
4. Open `Pages`
5. Under `Build and deployment`, choose:

- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/docs`

6. Save
7. Wait 1-3 minutes

Your public link will look like:

```text
https://YOUR_USERNAME.github.io/YOUR_REPO/
```

### Difference Between Render And GitHub Pages

- `Render`: runs the Flask backend in `web_app.py`
- `GitHub Pages`: serves the static app in `docs/index.html`

If you want a public site like a normal static website, use GitHub Pages.

## Notes

- Do not hardcode Gemini API keys in code
- Users should enter their own key in the app
- Quota and billing are controlled by each user's Google AI Studio project
