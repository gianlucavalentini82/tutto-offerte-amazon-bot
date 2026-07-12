from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import os
import shutil

from app.services.telegram import invia_offerta


app = FastAPI(
    title="Tutto Offerte Manager",
    description="Gestionale offerte Amazon con bot Telegram",
    version="0.1"
)

templates = Jinja2Templates(directory="app/templates")

UPLOAD_FOLDER = "app/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def prezzo_to_float(prezzo: str) -> float:
    prezzo = prezzo.replace("€", "")
    prezzo = prezzo.replace(" ", "")
    prezzo = prezzo.replace(".", "")
    prezzo = prezzo.replace(",", ".")
    return float(prezzo)


def formato_euro(valore: float) -> str:
    return f"{valore:.2f}".replace(".", ",")


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
    consigliato: str = Form(None),
    foto: UploadFile = File(None)
):

    percorso_foto = None

    if foto and foto.filename:

        percorso_foto = os.path.join(
            UPLOAD_FOLDER,
            foto.filename
        )

        with open(percorso_foto, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

    prezzo_vecchio_num = prezzo_to_float(prezzo_vecchio)
    prezzo_offerta_num = prezzo_to_float(prezzo_offerta)

    risparmio = prezzo_vecchio_num - prezzo_offerta_num
    percentuale = (risparmio / prezzo_vecchio_num) * 100

    prezzo_offerta_formattato = formato_euro(prezzo_offerta_num)

    messaggio = f"""
🔥 {prodotto}

💰 Prezzo precedente: {formato_euro(prezzo_vecchio_num)} €

🔥 Prezzo offerta: {prezzo_offerta_formattato} €

🏷️ -{percentuale:.0f}% • Risparmi {formato_euro(risparmio)} €
"""

    if consigliato:
        messaggio += """

⭐ Prodotto consigliato da Gianluca
"""

    if link_youtube:
        messaggio += """

🎥 Guarda la recensione YouTube
"""


    testo_condivisione = f"""
🔥 Guarda questa offerta Amazon!

📦 {prodotto}

💰 Prezzo: {prezzo_offerta_formattato} €

🏷️ Sconto: -{percentuale:.0f}%

🛒 Acquista qui:
{link_amazon}

📢 Altre offerte:
https://t.me/tuttooffert
"""


    await invia_offerta(
        testo=messaggio,
        link_amazon=link_amazon,
        link_youtube=link_youtube,
        foto=percorso_foto,
        testo_condivisione=testo_condivisione
    )

    return {
        "stato": "offerta pubblicata su Telegram"
    }