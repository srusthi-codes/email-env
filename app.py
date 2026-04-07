from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from inference import run_inference

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Email AI</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(to right, #667eea, #764ba2);
                color: white;
                text-align: center;
                padding-top: 50px;
            }
            textarea {
                width: 60%;
                height: 120px;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
            button {
                background: #ff7eb3;
                border: none;
                padding: 12px 25px;
                font-size: 18px;
                border-radius: 8px;
                cursor: pointer;
                color: white;
            }
            button:hover {
                background: #ff4f91;
            }
            .box {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 15px;
                display: inline-block;
            }
        </style>

        <script>
            function showLoading() {
                document.getElementById("loading").style.display = "block";
            }
        </script>

    </head>
    <body>
        <div class="box">
            <h1>📧 Email AI Analyzer 🚀</h1>

            <form action="/analyze" method="post" onsubmit="showLoading()">
                <textarea name="text" placeholder="Paste your email here..."></textarea><br><br>
                <button type="submit">Analyze</button>
            </form>

            <p id="loading" style="display:none;">⏳ Analyzing...</p>
        </div>
    </body>
    </html>
    """

@app.post("/analyze", response_class=HTMLResponse)
def analyze_email(text: str = Form(...)):
    result = run_inference(text)

    return f"""
<html>
<head>
<style>
    body {{
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        text-align: center;
        padding-top: 50px;
    }}

    .card {{
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        padding: 35px;
        border-radius: 20px;
        display: inline-block;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        width: 320px;
    }}

    .badge {{
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
    }}

    .green {{ background: #16a34a; }}
    .red {{ background: #dc2626; }}
    .yellow {{ background: #facc15; color: black; }}
    .blue {{ background: #2563eb; }}
    .purple {{ background: #7c3aed; }}

    h2 {{
        margin-bottom: 20px;
    }}

    p {{
        margin: 10px 0;
        font-size: 16px;
    }}

    a {{
        color: #38bdf8;
        text-decoration: none;
        font-weight: bold;
    }}

    a:hover {{
        text-decoration: underline;
    }}
</style>
</head>

<body>
<div class="card">

<h2>📊 Analysis Result</h2>

<p>Category: <span class="badge purple">{result['final_action']['category']}</span></p>

<p>Spam: 
<span class="badge {'red' if result['final_action']['spam']=='spam' else 'green'}">
{result['final_action']['spam']}
</span>
</p>

<p>Urgent: 
<span class="badge {'red' if result['final_action']['urgent']=='yes' else 'green'}">
{result['final_action']['urgent']}
</span>
</p>

<p>Confidence: <span class="badge yellow">{result['confidence']}</span></p>

<p>Action: <span class="badge blue">{result['suggestion']}</span></p>

<br>
<p><b>💬 Reply:</b><br>{result['final_action']['reply']}</p>

<br><br>
<a href="/">🔙 Analyze Another</a>

</div>
</body>
</html>
"""