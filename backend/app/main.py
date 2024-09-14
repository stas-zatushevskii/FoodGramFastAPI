from fastapi import FastAPI
app = FastAPI()

@app.get(
    '/{name}',
)
def greetings(name: str) -> dict[str, str]:

    return {'Hello': name}