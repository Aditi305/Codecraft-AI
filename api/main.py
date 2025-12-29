from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
import os
from dotenv import load_dotenv

load_dotenv()  # load .env

app = FastAPI(
    title="Codecraft AI API",
    description="API for generating code using a multi-agent system with architect, coder, tester, reviewer, and manager agents",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS stuff - allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/health", tags=["system"])
def health_check():
    # simple health check
    return {
        "status": "healthy",
        "service": "Codecraft AI API",
        "version": "1.0.0"
    }

@app.get("/status", tags=["system"])
def status():
    # check if everything is configured
    return {
        "status": "operational",
        "openrouter_configured": bool(os.getenv("OPENROUTER_API_KEY")),
        "openrouter_model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        "endpoints": {
            "generate_code": "/api/v1/generate",
            "health": "/health",
            "status": "/status",
            "docs": "/docs"
        }
    }

@app.get("/", response_class=HTMLResponse, tags=["ui"])
def root():
    """Main landing page with interactive UI"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Codecraft AI</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #F6F7FB;
                min-height: 100vh;
                padding: 0;
                overflow-x: hidden;
                box-sizing: border-box;
                margin: 0;
            }
            
            * {
                box-sizing: border-box;
            }
            
            .navbar-container {
                width: 100%;
                padding: 0;
                margin-bottom: 30px;
            }
            
            .navbar {
                background: white;
                padding: 15px 30px;
                border-radius: 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 100%;
            }
            
            .navbar-title {
                color: #5B7CFA;
                font-size: 1.5em;
                font-weight: 600;
                margin: 0;
            }
            
            .navbar-buttons {
                display: flex;
                gap: 10px;
            }
            
            .navbar-btn {
                padding: 8px 16px;
                background: #f8f9fa;
                color: #5B7CFA;
                text-decoration: none;
                border-radius: 6px;
                font-weight: 500;
                font-size: 14px;
                transition: all 0.3s, transform 0.2s;
                border: 1px solid #e0e0e0;
            }
            
            .navbar-btn:hover {
                background: #7C92FF;
                color: white;
                border-color: #7C92FF;
                transform: translateY(-2px);
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                width: 100%;
                overflow-x: hidden;
                padding: 0 20px;
            }
            
            .workflow-modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                z-index: 1000;
                justify-content: center;
                align-items: center;
            }
            
            .workflow-modal.show {
                display: flex;
            }
            
            .workflow-modal-content {
                background: white;
                padding: 30px;
                border-radius: 15px;
                max-width: 600px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                position: relative;
            }
            
            .workflow-modal-close {
                position: absolute;
                top: 15px;
                right: 15px;
                background: #f8f9fa;
                border: none;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 18px;
                color: #1F2937;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .workflow-modal-close:hover {
                background: #e9ecef;
            }
            
            .workflow-modal h2 {
                color: #5B7CFA;
                margin-top: 0;
                margin-bottom: 20px;
            }
            
            .workflow-modal .workflow {
                list-style: none;
                padding: 0;
            }
            
            .workflow-modal .workflow li {
                padding: 15px;
                margin-bottom: 10px;
                background: #f8f9fa;
                border-left: 4px solid #5B7CFA;
                border-radius: 5px;
            }
            
            .workflow-modal .workflow li .agent-name {
                font-weight: 600;
                color: #5B7CFA;
                margin-bottom: 5px;
            }
            
            .workflow-modal .workflow li .agent-desc {
                color: #1F2937;
                font-size: 0.9em;
                opacity: 0.8;
            }
            
            h1 {
                color: #5B7CFA;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .subtitle {
                color: #1F2937;
                font-size: 1.1em;
                opacity: 0.8;
            }
            
            p {
                color: #1F2937;
            }
            
            .main-content {
                display: block;
                margin-bottom: 30px;
            }
            
            .main-content .card {
                width: 100%;
            }
            
            .card {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            
            .card h2 {
                color: #5B7CFA;
                margin-bottom: 20px;
                font-size: 1.5em;
                border-bottom: 2px solid #5B7CFA;
                padding-bottom: 10px;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                color: #1F2937;
                font-weight: 600;
            }
            
            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                font-family: inherit;
                resize: vertical;
                min-height: 120px;
                transition: border-color 0.3s;
            }
            
            textarea:focus {
                outline: none;
                border-color: #5B7CFA;
                box-shadow: 0 0 0 3px rgba(91, 124, 250, 0.1);
            }
            
            .btn {
                background: #5B7CFA;
                color: white;
                border: none;
                padding: 16px 32px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
                transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;
                box-shadow: 0 4px 12px rgba(91, 124, 250, 0.25);
            }
            
            .btn:hover {
                transform: translateY(-2px);
                background-color: #7C92FF;
                box-shadow: 0 6px 20px rgba(91, 124, 250, 0.35);
            }
            
            .btn:active {
                transform: translateY(0);
            }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            
            .workflow {
                list-style: none;
            }
            
            .workflow li {
                padding: 15px;
                margin-bottom: 10px;
                background: #f8f9fa;
                border-left: 4px solid #5B7CFA;
                border-radius: 5px;
                display: flex;
                align-items: center;
            }
            
            .workflow li .icon {
                font-size: 1.5em;
                margin-right: 15px;
            }
            
            .workflow li .agent-info {
                flex: 1;
            }
            
            .workflow li .agent-name {
                font-weight: 600;
                color: #5B7CFA;
            }
            
            .workflow li .agent-desc {
                color: #1F2937;
                font-size: 0.9em;
                opacity: 0.8;
            }
            
            .result {
                display: none;
                margin-top: 20px;
            }
            
            .result.show {
                display: block;
            }
            
            .result-section {
                background: #f8f9fa;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 8px;
                border-left: 4px solid #5B7CFA;
            }
            
            .result-section h3 {
                color: #5B7CFA;
                margin-bottom: 10px;
                font-size: 1.1em;
            }
            
            .result-section pre {
                background: #2d2d2d;
                color: #f8f8f2;
                padding: 15px;
                border-radius: 5px;
                overflow-x: hidden;
                overflow-y: auto;
                max-height: 500px;
                font-size: 13px;
                line-height: 1.6;
                white-space: pre-wrap;
                word-wrap: break-word;
                word-break: break-word;
                max-width: 100%;
                width: 100%;
                margin: 0;
            }
            
            .result-section {
                max-width: 100%;
                overflow: hidden;
                width: 100%;
            }
            
            .result {
                max-width: 100%;
                overflow: hidden;
                width: 100%;
            }
            
            .card {
                max-width: 100%;
                overflow: hidden;
                width: 100%;
            }
            
            .main-content {
                width: 100%;
                overflow: hidden;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
            }
            
            .loading.show {
                display: block;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #5B7CFA;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .links {
                display: flex;
                gap: 15px;
                margin-top: 20px;
            }
            
            .link-btn {
                flex: 1;
                text-align: center;
                padding: 12px;
                background: #f8f9fa;
                color: #5B7CFA;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                transition: background 0.3s;
            }
            
            .link-btn:hover {
                background: #e9ecef;
            }
            
            .error {
                background: #fee;
                color: #c33;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #c33;
                margin-top: 20px;
            }
            
            .error h4 {
                margin-top: 0;
                margin-bottom: 10px;
                font-size: 1.2em;
            }
            
            .error .solutions {
                margin-top: 15px;
                padding-left: 20px;
            }
            
            .error .solutions li {
                margin: 8px 0;
                line-height: 1.6;
            }
            
            .error .help-links {
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #fcc;
            }
            
            .error .help-links a {
                color: #c33;
                text-decoration: underline;
                margin-right: 15px;
            }
            
            .workflow-modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                z-index: 1000;
                justify-content: center;
                align-items: center;
            }
            
            .workflow-modal.show {
                display: flex;
            }
            
            .workflow-modal-content {
                background: white;
                padding: 30px;
                border-radius: 15px;
                max-width: 600px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                position: relative;
            }
            
            .workflow-modal-close {
                position: absolute;
                top: 15px;
                right: 15px;
                background: #f8f9fa;
                border: none;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 18px;
                color: #1F2937;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .workflow-modal-close:hover {
                background: #e9ecef;
            }
            
            .workflow-modal h2 {
                color: #5B7CFA;
                margin-top: 0;
                margin-bottom: 20px;
            }
            
            .workflow-modal .workflow {
                list-style: none;
                padding: 0;
            }
            
            .workflow-modal .workflow li {
                padding: 15px;
                margin-bottom: 10px;
                background: #f8f9fa;
                border-left: 4px solid #5B7CFA;
                border-radius: 5px;
            }
            
            .workflow-modal .workflow li .agent-name {
                font-weight: 600;
                color: #5B7CFA;
                margin-bottom: 5px;
            }
            
            .workflow-modal .workflow li .agent-desc {
                color: #1F2937;
                font-size: 0.9em;
                opacity: 0.8;
            }
            
            @media (max-width: 768px) {
                .main-content {
                    grid-template-columns: 1fr;
                }
                
                h1 {
                    font-size: 2em;
                }
                
                .navbar {
                    flex-direction: column;
                    gap: 15px;
                }
                
                .navbar-buttons {
                    width: 100%;
                    justify-content: center;
                    flex-wrap: wrap;
                }
                
                .navbar-btn {
                    flex: 1;
                    min-width: 100px;
                    text-align: center;
                }
            }
        </style>
    </head>
    <body>
        <div class="navbar-container">
            <nav class="navbar">
                <h1 class="navbar-title">Codecraft AI</h1>
                <div class="navbar-buttons">
                    <a href="/docs" class="navbar-btn">API Docs</a>
                    <a href="/redoc" class="navbar-btn">ReDoc</a>
                    <a href="#" class="navbar-btn" id="workflowBtn">Agent Workflow</a>
                </div>
            </nav>
        </div>
        
        <div class="container">
            
            <div class="workflow-modal" id="workflowModal">
                <div class="workflow-modal-content">
                    <button class="workflow-modal-close" id="closeWorkflow">&times;</button>
                    <h2>Agent Workflow</h2>
                    <ul class="workflow">
                        <li>
                            <div class="agent-info">
                                <div class="agent-name">1. Architect</div>
                                <div class="agent-desc">First, we design the high-level architecture and system structure</div>
                            </div>
                        </li>
                        <li>
                            <div class="agent-info">
                                <div class="agent-name">2. Coder</div>
                                <div class="agent-desc">Then we write the actual code based on that architecture</div>
                            </div>
                        </li>
                        <li>
                            <div class="agent-info">
                                <div class="agent-name">3. Tester</div>
                                <div class="agent-desc">We create comprehensive test cases to make sure everything works</div>
                            </div>
                        </li>
                        <li>
                            <div class="agent-info">
                                <div class="agent-name">4. Reviewer</div>
                                <div class="agent-desc">We review the code quality and test coverage together</div>
                            </div>
                        </li>
                        <li>
                            <div class="agent-info">
                                <div class="agent-name">5. Manager</div>
                                <div class="agent-desc">Finally, we decide if it's ready or needs another pass. If it needs work, we loop back to improve it.</div>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
            
            <div class="main-content">
                <div class="card">
                    <h2>What would you like to build?</h2>
                    <form id="codeForm">
                        <div class="form-group">
                            <label for="task">Tell us about your coding task:</label>
                            <textarea 
                                id="task" 
                                name="task" 
                                placeholder="For example: Create a Python calculator class that handles basic math operations"
                                required
                            ></textarea>
                        </div>
                        <button type="submit" class="btn" id="submitBtn">Generate Code</button>
                    </form>
                    
                    <div class="loading" id="loading">
                        <div class="spinner"></div>
                        <p>Our agents are working on it...</p>
                    </div>
                    
                    <div class="error" id="error" style="display: none;"></div>
                    
                    <div class="result" id="result">
                        <div class="result-section">
                            <h3>Architecture</h3>
                            <pre id="architecture"></pre>
                        </div>
                        <div class="result-section">
                            <h3>Generated Code</h3>
                            <pre id="code"></pre>
                        </div>
                        <div class="result-section">
                            <h3>Test Cases</h3>
                            <pre id="tests"></pre>
                        </div>
                        <div class="result-section">
                            <h3>Review</h3>
                            <pre id="review"></pre>
                        </div>
                        <div class="result-section">
                            <h3>Final Decision</h3>
                            <pre id="decision"></pre>
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 20px;">
        </div>
        
        <script>
            const form = document.getElementById('codeForm');
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const error = document.getElementById('error');
            const workflowBtn = document.getElementById('workflowBtn');
            const workflowModal = document.getElementById('workflowModal');
            const closeWorkflow = document.getElementById('closeWorkflow');
            
            // Workflow modal handlers
            workflowBtn.addEventListener('click', (e) => {
                e.preventDefault();
                workflowModal.classList.add('show');
            });
            
            closeWorkflow.addEventListener('click', () => {
                workflowModal.classList.remove('show');
            });
            
            workflowModal.addEventListener('click', (e) => {
                if (e.target === workflowModal) {
                    workflowModal.classList.remove('show');
                }
            });
            
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const task = document.getElementById('task').value;
                
                // Reset UI
                result.classList.remove('show');
                error.style.display = 'none';
                loading.classList.add('show');
                submitBtn.disabled = true;
                
                try {
                    const response = await fetch('/api/v1/generate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ task })
                    });
                    
                    if (!response.ok) {
                        const errorData = await response.json();
                        const detail = errorData.detail;
                        
                        // Handle structured error responses
                        if (typeof detail === 'object' && detail.error) {
                            let errorHtml = `<h4>${detail.error}</h4>`;
                            errorHtml += `<p><strong>${detail.message}</strong></p>`;
                            
                            if (detail.solutions && Array.isArray(detail.solutions)) {
                                errorHtml += '<div class="solutions"><strong>Solutions:</strong><ul>';
                                detail.solutions.forEach(solution => {
                                    errorHtml += `<li>${solution}</li>`;
                                });
                                errorHtml += '</ul></div>';
                            }
                            
                            if (detail.help_links) {
                                errorHtml += '<div class="help-links"><strong>Helpful Links:</strong><br>';
                                Object.entries(detail.help_links).forEach(([name, url]) => {
                                    errorHtml += `<a href="${url}" target="_blank">${name}</a>`;
                                });
                                errorHtml += '</div>';
                            }
                            
                            error.innerHTML = errorHtml;
                        } else {
                            error.innerHTML = `<h4>Error</h4><p>${detail || err.message || 'Failed to generate code'}</p>`;
                        }
                        error.style.display = 'block';
                        return;
                    }
                    
                    const data = await response.json();
                    
                    // Display results
                    document.getElementById('architecture').textContent = data.architecture || 'N/A';
                    document.getElementById('code').textContent = data.code || 'N/A';
                    document.getElementById('tests').textContent = data.tests || 'N/A';
                    document.getElementById('review').textContent = data.review || 'N/A';
                    document.getElementById('decision').textContent = data.final_decision || 'N/A';
                    
                    result.classList.add('show');
                    result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    
                } catch (err) {
                    error.innerHTML = `<h4>Error</h4><p>${err.message || 'An unexpected error occurred'}</p>`;
                    error.style.display = 'block';
                } finally {
                    loading.classList.remove('show');
                    submitBtn.disabled = false;
                }
            });
        </script>
    </body>
    </html>
    """
