from fastapi import FastAPI

app = FastAPI()

@app.get("/mytest")
def mytest():
    return {"message": "Hello, FastAPI updated!"}
