from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import is_configured, save_config
from app.database import confirm_patient_entry, get_waiting_patients, test_connection

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Clinic Queue Manager", version="1.0.0")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main page - redirects to setup if not configured."""
    if not is_configured():
        return RedirectResponse(url="/setup", status_code=302)
    return templates.TemplateResponse(request, "index.html")


@app.get("/setup", response_class=HTMLResponse)
async def setup_page(request: Request):
    """Database setup page."""
    return templates.TemplateResponse(request, "setup.html", context={"error": None, "success": None})


@app.post("/setup", response_class=HTMLResponse)
async def setup_save(
    request: Request,
    server: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
):
    """Save database configuration."""
    success, message = test_connection(server, username, password)
    if success:
        save_config(server, username, password)
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(
        request,
        "setup.html",
        context={"error": message, "success": None},
    )


@app.get("/api/patients")
async def api_patients():
    """API endpoint to get waiting patients."""
    try:
        patients = get_waiting_patients()
        return JSONResponse(content={"patients": patients, "count": len(patients)})
    except Exception as e:
        return JSONResponse(content={"error": str(e), "patients": [], "count": 0}, status_code=500)


@app.post("/api/confirm/{tktno}")
async def api_confirm(tktno: str):
    """API endpoint to confirm patient entry."""
    success, message = confirm_patient_entry(tktno)
    return JSONResponse(content={"success": success, "message": message})


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    """Settings page to reconfigure database connection."""
    return templates.TemplateResponse(request, "setup.html", context={"error": None, "success": None})
