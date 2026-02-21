from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
from schemas import BusinessCreate, BusinessUpdate, BusinessResponse
import os

# models.Base.metadata.create_all(bind=engine)


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Oikko Business Directory API",
    description="API for managing local desi businesses",
    version="1.0"
)

# --------------------------
# Database dependency first
# --------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root():
    # return {
    #     "welcome": "Oikko - Local Desi Business Directory",
    #     "instructions": [
    #         "Use /businesses to add new businesses",
    #         "Use /businesses/{id} to view, update, or delete",
    #         "Visit /docs for interactive API testing"
    #     ],
    #     "note": "Powered by FastAPI and SQLite! ",
    #     "Developed by" : "Asmaul Husna Rinvi & Jahidul Hasan Hemal"
    # }
    return """
    <html>
        <head>
            <title>Oikko - Desi Business Directory</title>
            <style>
                body { font-family: Arial, sans-serif; background: #f9f9f9; color: #333; padding: 2rem; }
                h1 { color: #ff6f61; }
                a { color: #0077cc; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .container { max-width: 700px; margin: auto; background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to Oikko!</h1>
                <p>Your local desi business directory API is live.</p>
                <p>Here’s what you can do:</p>
                <ul>
                    <li>📖 <a href="/docs">Explore the API docs (Swagger UI)</a></li>
                    <li>➕ Add new businesses via POST /businesses</li>
                    <li>🔍 Search or list businesses with GET /businesses</li>
                </ul>
                <p>Powered by <strong>FastAPI</strong> and <strong>SQLite</strong>!</p>
                <!--<p>Developed for <strong>Asmaul Husna Rinvi</strong> and <strong>Jahidul Hasan Hemal</strong>!</p>-->
            </div>
        </body>
    </html>
    """

@app.post("/businesses", response_model=BusinessResponse)
def create_business(business: BusinessCreate, db: Session = Depends(get_db)):
    db_business = models.Business(**business.dict())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business

@app.get("/businesses", response_model=list[BusinessResponse])
def get_businesses(db: Session = Depends(get_db)):
    return db.query(models.Business).all()

@app.get("/businesses/{business_id}", response_model=BusinessResponse)
def get_business(business_id: int, db: Session = Depends(get_db)):
    business = db.query(models.Business).filter(
        models.Business.id == business_id
    ).first()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    return business


@app.put("/businesses/{business_id}", response_model=BusinessResponse)
def update_business(
    business_id: int,
    updated: BusinessUpdate,
    db: Session = Depends(get_db)
):
    business = db.query(models.Business).filter(
        models.Business.id == business_id
    ).first()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    for key, value in updated.dict().items():
        setattr(business, key, value)

    db.commit()
    db.refresh(business)
    return business


@app.delete("/businesses/{business_id}")
def delete_business(business_id: int, db: Session = Depends(get_db)):
    business = db.query(models.Business).filter(
        models.Business.id == business_id
    ).first()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    db.delete(business)
    db.commit()
    return {"message": "Business deleted"}