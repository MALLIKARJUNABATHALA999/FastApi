from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import schemas,models,hashing
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

myapp=FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@myapp.post('/blog',status_code=201,tags=["blogs"])
def create(request:schemas.Blog,db: Session=Depends(get_db)):
    new_blog=models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@myapp.get('/blog',status_code=status.HTTP_201_CREATED,response_model=List[schemas.ShowBlog],tags=["blogs"])
def all(db: Session=Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@myapp.get('/blog/{id}',status_code=200,response_model=schemas.ShowBlog,tags=["blogs"])
def show(id,response:Response,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not avaailable" )
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return {"detail":f"Blog with the id {id} is not avaailable"}
    return blog

@myapp.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=["blogs"])
def destroy(id,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blof with {id} is not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"done"}

@myapp.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])
def update(id,request:schemas.Blog,db:Session=Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id{id} not found')
        
    blog.update({'title':'updated title','body':'updated body'})
    db.commit()
    return {'updated successfully'}


pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")
@myapp.post('/user',response_model=schemas.ShowUser)
def create_user(request:schemas.User,db: Session=Depends(get_db)):
    
    new_user=models.User(name=request.name,email=request.email,password=hashing.Hash.bcrypt(request.password),phonenumber=request.phonenumber)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@myapp.get("/user",tags=["user"])
def all(db: Session=Depends(get_db)):
    blogs=db.query(models.User).all()
    return blogs

@myapp.get("/user{id}",response_model=schemas.ShowUser,tags=["user"])
def get_user(id:int,db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog with the id {id} is not available")
    return user