from datetime import timedelta, time

from sanic import Sanic
from sanic.response import text

# https://github.com/Asmodius/sanic-scheduler
from sanic_scheduler import SanicScheduler, task

from models.issue import Issue

issue = Issue()

app = Sanic("zenHN")
app.extend(config={"oas": False})
app.static("/static/css", "./static/css", name="css")
app.static("/static/images", "./static/images", name="images")

scheduler = SanicScheduler(app)


@app.get("/ping")
async def ping(request):
    return text("I'm up and running")


@app.get("/")
@app.ext.template("index.html")
async def index(request):
    return {"app": app, "issue": issue}


@app.get("/feed")
async def feed(request):
    return text(issue.feed, content_type="text/xml")


@task(timedelta(minutes=30))
async def create_issue(_):
    global issue
    issue = Issue()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
