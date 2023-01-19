from sanic import Sanic
from sanic.response import text

from models.issue import Issue

issue = Issue()

app = Sanic("zenHN")
app.extend(config={"oas": False})
app.static("/static/css", "./static/css", name="css")
app.static("/static/images", "./static/images", name="images")


@app.get("/ping")
async def ping(request):
    return text("I'm up and running")


@app.get("/")
@app.ext.template("index.html")
async def index(request):
    return {"app": app, "stories": issue.stories}


@app.get("/feed")
async def feed(request):
    return text("feed")


if __name__ == "__main__":
    app.run(port=5000, dev=True)
