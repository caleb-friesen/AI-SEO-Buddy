from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime
from .scraper import scrape_url
from .analyzer import analyze_content
from .lighthouse import run_lighthouse_audit
from .recommendations import generate_recommendations

app = FastAPI()

class URLRequest(BaseModel):
    url: str
    keywords: Optional[List[str]] = None

class SEOResponse(BaseModel):
    task_id: str
    status: str
    results: Optional[dict] = None

@app.post("/analyze", response_model=SEOResponse)
async def analyze_url(request: URLRequest):
    try:
        # Create a unique task ID using timestamp
        task_id = str(int(datetime.now().timestamp()))
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Initialize task status
        task_data = {
            "status": "in_progress",
            "url": request.url,
            "keywords": request.keywords,
            "results": {}
        }
        
        # Save initial task status
        with open(f"data/task_{task_id}.json", "w") as f:
            json.dump(task_data, f)
        
        # Scrape the URL
        content = await scrape_url(request.url)
        
        # Run analysis
        analysis_results = analyze_content(content, request.keywords)
        
        # Run Lighthouse audit
        lighthouse_results = await run_lighthouse_audit(request.url)
        
        # Generate recommendations
        recommendations = generate_recommendations(analysis_results, lighthouse_results)
        
        # Update task results
        task_data.update({
            "status": "completed",
            "results": {
                "analysis": analysis_results,
                "lighthouse": lighthouse_results,
                "recommendations": recommendations
            }
        })
        
        # Save final results
        with open(f"data/task_{task_id}.json", "w") as f:
            json.dump(task_data, f)
        
        return SEOResponse(
            task_id=task_id,
            status="completed",
            results=task_data["results"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{task_id}", response_model=SEOResponse)
async def get_task_status(task_id: str):
    try:
        with open(f"data/task_{task_id}.json", "r") as f:
            task_data = json.load(f)
        
        return SEOResponse(
            task_id=task_id,
            status=task_data["status"],
            results=task_data.get("results")
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 