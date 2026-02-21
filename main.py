from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models
from schemas import BusinessCreate, BusinessUpdate, BusinessResponse

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

@app.get("/")
def read_root():
    return {
        "welcome": "Oikko - Local Desi Business Directory",
        "instructions": [
            "Use /businesses to add new businesses",
            "Use /businesses/{id} to view, update, or delete",
            "Visit /docs for interactive API testing"
        ],
        "note": "Powered by FastAPI and SQLite! ",
        "Developed by" : "Asmaul Husna Rinvi & Jahidul Hasan Hemal"
    }

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