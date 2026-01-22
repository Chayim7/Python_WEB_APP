from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import Base, SessionLocal, engine
from .models import Service
from .web.routes import router as web_router

app = FastAPI(title="AMI Patch Evidence Tracker (Synthetic Data)")


app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(web_router)


def seed_default_services() -> None:
    db = SessionLocal()
    try:
        has_any_service = db.query(Service).first() is not None
        if not has_any_service:
            default_services = [
                "Nessus Manager",
                "Trend Micro",
                "Tenable Security Center",
                "ServiceNow MID Server",
            ]
            for name in default_services:
                db.add(Service(name=name))
            db.commit()
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    seed_default_services()
