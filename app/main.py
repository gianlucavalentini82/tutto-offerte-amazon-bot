from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Tutto Offerte Manager",
    description="Gestionale offerte Amazon con bot Telegram",
    version="0.1"
)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tutto Offerte Manager</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                text-align: center;
            }

            h1 {
                font-size: 40px;
            }

            .box {
                padding: 30px;
                border-radius: 10px;
                background: #f2f2f2;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h1>🚀 Tutto Offerte Manager</h1>
            <p>Prima versione del gestionale offerte Amazon</p>
            <p>Server FastAPI funzionante ✅</p>
        </div>
    </body>
    </html>
    """