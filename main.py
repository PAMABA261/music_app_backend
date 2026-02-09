from fastapi import FastAPI

app = FastAPI(title="Music App Backend")

@app.get("/")
def read_root():
    return {"message": "¡El backend musical está funcionando!"}