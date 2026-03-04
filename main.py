from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/items", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()


@app.post("/items", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    db.delete(item)
    db.commit()
    return {"deleted": item_id}
