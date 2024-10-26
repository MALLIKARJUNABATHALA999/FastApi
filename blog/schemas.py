from pydantic import BaseModel

class Blog(BaseModel):
    title : str
    body : str

class ShowBlog(BaseModel):
    title : str
    body:str
    class Config():
        from_attributes=True
        # here we are using form attributes or orm_mode


class User(BaseModel):
    name:str
    email:str
    password:str
    phonenumber:int

class ShowUser(BaseModel):
    name:str 
    email:str
    phonenumber:int
    class Config():
        from_attributes=True
