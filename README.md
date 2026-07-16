# Couch Tracker MVP

An AI-Powered E-Governance Tracker built for a 72-hour hackathon. This repository contains the Next.js frontend, a FastAPI backend (to serve mock data and handle webhooks), and local AI scripts to generate object detection bounding boxes using YOLOv8.

## Project Structure

- `/frontend`: Next.js 14 App Router application with Tailwind CSS and Leaflet maps. Supports Light/Dark mode.
- `/backend`: FastAPI service that provides a mock `/projects` endpoint and a dummy `/webhook` for Twilio.
- `/ai_scripts`: Python scripts using Ultralytics YOLOv8 for running local image inference to determine AI confidence scores.

## Setup Instructions

### 1. Backend (FastAPI)
1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
   *The API will be available at `http://localhost:8000`. You can view the swagger docs at `http://localhost:8000/docs`.*

### 2. Frontend (Next.js)
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   *The frontend will be available at `http://localhost:3000`.*

### 3. AI Scripts (Local Processing)
1. Navigate to the `ai_scripts` directory:
   ```bash
   cd ai_scripts
   ```
2. Install dependencies (you can use the same virtual environment as the backend or a separate one):
   ```bash
   pip install -r requirements.txt
   ```
3. Add some sample `.jpg` or `.png` satellite images into `ai_scripts/input_images/`.
4. Run the YOLOv8 script:
   ```bash
   python generate_boxes.py
   ```
5. Check `ai_scripts/output_images/` for the annotated images.
