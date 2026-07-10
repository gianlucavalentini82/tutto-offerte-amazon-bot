from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.telegram import invia_offerta


app = FastAPI(
    title="Tutto Offerte Manager",
    description="Gestionale offerte Amazon con bot Telegram",
    version="0.1"
)


templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/nuova-offerta", response_class=HTMLResponse)
async def nuova_offerta(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="nuova_offerta.html"
    )


@app.post("/pubblica-offerta")
async def pubblica_offerta(
    prodotto: str = Form(...),
    prezzo_vecchio: str = Form(...),
    prezzo_offerta: str = Form(...),
    link_amazon: str = Form(...),
    link_youtube: str = Form(""),
    consigliato: str = Form(None)
):

    messaggio = f"""
🔥 {prodotto}

💰 Prezzo precedente: {prezzo_vecchio} €

🔥 Prezzo offerta: {prezzo_offerta} €
"""


    if consigliato:
        messaggio += """

⭐ Prodotto consigliato da Gianluca
"""


    if link_youtube:
        messaggio += """

🎥 Guarda la recensione YouTube
"""


    await invia_offerta(
        testo=messaggio,
        link_amazon=link_amazon,
        link_youtube=link_youtube
    )


    return {
        "stato": "offerta pubblicata su Telegram"
    }