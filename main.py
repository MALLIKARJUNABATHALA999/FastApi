from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
app=FastAPI()
@app.get("/blog")
def index(limit=10,published : bool =True,sort: Optional[str]=None):
    if published:
         return {'data':f'{limit} blogs from  db'}
    else:
        return {'all blogs from the database'}
@app.get('/blog/unpublished')
def unpublished():
    return {'data':'all unpublished blogs'}
@app.get('/blog/{id}')
def show(id: int):
    return {'data':id}
@app.get('/blog/{id}/comments')
def comments(id):
    return {'data':{'1','2'}}



class Blog(BaseModel):
    title: str
    body:str
    published_at:Optional[bool]
    
@app.post('/blog')
def create_blog(requests:Blog):
    
    return {'data':f'Blog is created with title as {requests.title}'}