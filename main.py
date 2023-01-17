from sanic import Sanic
from sanic.response import text

app = Sanic("zenHN")


@app.get("/ping")
async def ping(request):
    return text("I'm up and running")


@app.get("/")
async def index(request):
    return text("index")


if __name__ == "__main__":
    app.run(port=5000, dev=True)
