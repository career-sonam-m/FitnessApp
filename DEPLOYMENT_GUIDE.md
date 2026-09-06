# FitBuddy Deployment Guide

## Local Testing with Docker

### Prerequisites
- Python 3.12+
- Docker installed on your machine
- OpenAI API Key

### Steps

1. **Set up your .env file**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your OpenAI API Key
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

2. **Build and run locally**
   ```bash
   # On Windows
   build_and_run.bat

   # On Mac/Linux
   docker build -t fitbuddy-app .
   docker run -p 7860:7860 --env-file .env fitbuddy-app
   ```

3. **Access the app**
   Open http://localhost:7860 in your browser

---

## Deploying to Hugging Face Spaces

### Step 1: Create a Hugging Face Space
1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose:
   - **Space name**: e.g., `fitbuddy-ai-coach`
   - **License**: MIT
   - **SDK**: Docker
   - **Visibility**: Public or Private
4. Click "Create Space"

### Step 2: Upload your files
You can upload files via:
- **Git** (recommended)
- **Web interface** (drag and drop)

#### Option A: Using Git (recommended)
```bash
# Initialize git if not already done
git init

# Add all files
git add .
git commit -m "Initial FitBuddy deployment"

# Add Hugging Face remote
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/fitbuddy-ai-coach

# Push to Hugging Face
git push origin main
```

#### Option B: Web Interface
1. Go to your Space on Hugging Face
2. Click "Files" tab
3. Upload these files:
   - `Dockerfile`
   - `requirements.txt`
   - `streamlit_app.py`
   - `.env` (with your API key - make Space private if you do this)
   - Or better: set API key as Space secret (see below)

### Step 3: Set API Key as Secret (Recommended)
Instead of committing `.env`, set your API key as a secret:

1. Go to your Space on Hugging Face
2. Click "Settings" tab
3. Scroll to "Repository secrets"
4. Click "New secret"
5. Name: `OPENAI_API_KEY`
6. Value: Your actual OpenAI API key
7. Click "Create secret"

Then update your Dockerfile to use the secret:
```dockerfile
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
```

### Step 4: Wait for Build
- Hugging Face will automatically build the Docker image
- Monitor the "Build logs" tab
- Once built, your app will be available at:
  `https://huggingface.co/spaces/YOUR_USERNAME/fitbuddy-ai-coach`

---

## Troubleshooting

### Build fails on Hugging Face
- Check the "Build logs" tab for errors
- Ensure all dependencies are in `requirements.txt`
- Make sure `Dockerfile` is properly formatted

### API Key issues
- If using `.env` file, ensure it's uploaded
- Better approach: Use Hugging Face Secrets
- For public Spaces, never commit real API keys

### App not loading
- Check if port 7860 is exposed in Dockerfile
- Ensure Streamlit is running on `0.0.0.0` (not localhost)

---

## File Structure for Deployment
```
FitnessApp/
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── streamlit_app.py       # Main Streamlit app
├── .env                    # API key (local only)
├── .env.example           # Example env file
├── .dockerignore          # Files to exclude from Docker
├── README.md              # Main README with Hugging Face metadata
└── DEPLOYMENT_GUIDE.md    # This file
```

## Notes
- The app uses `gpt-4o-mini` which is cost-effective
- Conversation memory is stored in session state (resets on refresh)
- For production, consider using a persistent database for memory
