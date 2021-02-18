import csv
import functools
import os
import random
import time
from multiprocessing import dummy

import requests
import urllib3
import uvicorn
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic.main import BaseModel
from starlette.concurrency import run_in_threadpool


def read_file(file):
    with open(file) as f:
        return f.read().splitlines()


def parse(query, body):
    query = query.replace(" ", "+")
    URL = f"https://www.google.com/search?q={query}&num={body.results_per_page}&lang={body.language}&region={body.region}"

    headers = {"user-agent": random.choice(body.user_agents)}

    session = requests.Session()

    results = []

    for i in range(0, body.max_pages):
        # for tryings in range(0, body.get_page_tryings):
        time.sleep(10)
        resp = session.get(
            URL, headers=headers, verify=False, timeout=body.timeout,
        )
        if resp.status_code == 429:
            print("response was 429, please wait a few minutes")
            # time.sleep(int(resp.headers["Retry-After"]))
            time.sleep(60)
            continue
        elif resp.status_code != 200:
            print(f"ERROR PARSE QUERY '{query}' on page {i + 1} !")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        for div in soup.find_all(class_="g"):
            # print(div)
            anchors = div.find(class_="yuRUbf").find_all("a")
            print(anchors)
            if anchors:
                # print("found anchor" + anchors)
                link = anchors[0]["href"]
                print(link)
                title = div.find(class_="LC20lb DKV0Md").getText()
                print(title)
                snippet = (
                    div.find("div", class_="IsZvec")
                    .find("span", class_="aCOpRe")
                    .getText()
                )
                print(snippet)
                item = {"title": title,
                        "link": link, "snippet": snippet}
                results.append(item)

        nextLink = soup.find("a", {"id": "pnnext"})
        print(nextLink)

        if nextLink is None:
            print(f"END RESULTS FOR QUERY '{query}'")
            return {"query": query, "results": results}

        nextLinkUrl = nextLink["href"]
        URL = f"https://www.google.com{nextLinkUrl}"

        time.sleep(random.randint(10, 30))
        break

    return {"query": query, "results": results}


def execute_queries(body):
    pool = dummy.Pool(body.threads)
    func = functools.partial(parse, body=body)
    out = pool.map(func, body.queries)
    for query in out:
        with open(f"out/{body.out_filename}", "a+", newline="") as csvfile:
            writer = csv.writer(
                csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerow(
                [query["query"],
                    f"{len(query['results'])} results"]
            )
            for item in query["results"]:
                writer.writerow([item["title"], item["link"], item["snippet"]])


if not os.path.exists("out"):
    os.mkdir("out")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/out", StaticFiles(directory="out"), name="out")
templates = Jinja2Templates(directory="templates")


class Body(BaseModel):
    threads: int
    max_pages: int
    get_page_tryings: int
    results_per_page: int
    language: str
    region: str
    timeout: int
    queries_file: str
    users_agents_file: str
    out_filename: str

    @property
    def user_agents(self):
        return read_file(self.users_agents_file)

    @property
    def queries(self):
        return read_file(self.queries_file)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process/")
async def process(request: Request, body: Body):
    print(request)
    await run_in_threadpool(execute_queries, body)
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    urllib3.disable_warnings()
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    uvicorn.run(app, host="127.0.0.1", port=8000, http="h11", loop="uvloop")
