from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from datetime import datetime
from fastapi.responses import JSONResponse

SERVER_URL = "http://194.113.35.248/api"

app = FastAPI()

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 1. Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/vichet/{password}", response_class=HTMLResponse)
async def vichet_html(request: Request, password: str):
    if password == "36863686":
        return templates.TemplateResponse(request=request, name="vichet.html")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/add_komp/{password}", response_class=HTMLResponse)
async def add_komp(request: Request, password: str):
    if password == "36863686":
        return templates.TemplateResponse(request=request, name="add_komp.html")

@app.get("/search/{password}", response_class=HTMLResponse)
async def search(request: Request, password: str, q: str = Form(default="")):
    if password == "36863686":
        try:
            response = requests.get(f"{SERVER_URL}/get_waregouse")
            if response.status_code == 200:
                result = []
                for i in response.json():
                    if q in i['Name'] or q in i['Category'] or q in i['Number']:
                        result.append(i)
                return templates.TemplateResponse(request=request, name="search.html",
                                                  context={"result": result})
            else:
                return f"error: {response.status_code}"
        except Exception as e:
            print(f"{e}")
            return "error"

@app.post("/searching/{password}", response_class=HTMLResponse)
async def searching(request: Request, password: str, q: str = Form(default="")):
    if password == "36863686":
        try:
            response = requests.get(f"{SERVER_URL}/get_waregouse")
            if response.status_code == 200:
                result = []
                for i in response.json():
                    if q in i['Name'] or q in i['Category'] or q in i['Number']:
                        result.append(i)
                return templates.TemplateResponse(request=request, name="search.html",
                                                  context={"result": result})
            else:
                return f"error: {response.status_code}"
        except Exception as e:
            print(f"{e}")
            return "error"

@app.post("/passord", response_class=HTMLResponse)
async def password(request: Request, password: str = Form(...)):
    if password == "36863686":
        return admin_panel(request)

@app.get("/all/{password}", response_class=HTMLResponse)
async def all(request: Request, password: str):
    if password == "36863686":
        return admin_panel(request)

@app.get("/gorizont/{password}", response_class=HTMLResponse)
async def gorizont(request: Request, password: str):
    if password == "36863686":
        return get_not_all("ГОРИЗОНТАЛЬНЫЕ ЖАЛЮЗИ", request)

@app.get("/vertical/{password}", response_class=HTMLResponse)
async def vertical(request: Request, password: str):
    if password == "36863686":
        return get_not_all("ВЕРТИКАЛЬНЫЕ ЖАЛЮЗИ", request)

@app.get("/uni/{password}", response_class=HTMLResponse)
async def uni(request: Request, password: str):
    if password == "36863686":
        return get_not_all("РУЛОННЫЕ ШТОРЫ UNI", request)

@app.get("/mg/{password}", response_class=HTMLResponse)
async def mg(request: Request, password: str):
    if password == "36863686":
        return get_not_all("РУЛОННЫЕ ШТОРЫ MG", request)

@app.get("/mini/{password}", response_class=HTMLResponse)
async def mini(request: Request, password: str):
    if password == "36863686":
        return get_not_all("РУЛОННЫЕ ШТОРЫ MINI", request)

@app.get("/benthin/{password}", response_class=HTMLResponse)
async def benthin(request: Request, password: str):
    if password == "36863686":
        return get_not_all("BENTHIN", request)

@app.get("/delete_ord/{item_id}", response_class=HTMLResponse)
async def del_ord(
    request: Request,
    item_id: int
):
    return templates.TemplateResponse(request=request, name="try_del.html", context={"order": item_id})

@app.get("/delete_order/{item_id}", response_class=HTMLResponse)
async def delete_order(
    request: Request,
    item_id: int
):
    try:
        response = requests.get(f"{SERVER_URL}/delete?id={item_id}")
        if response.status_code == 200:
            return admin_panel(request)
    except requests.exceptions.RequestException as e:
        return

@app.get("/vichet_func", response_class=HTMLResponse)
async def vichet_func(
    request: Request,
    weight: int = Form(...),
    height: int = Form(...),
    service: str = Form(...)
):
    vichet_list = {'ВЕРТИКАЛЬНЫЕ ЖАЛЮЗИ' : "verdef", "ГОРИЗОНТАЛЬНЫЕ ЖАЛЮЗИ" : "gordef", "MINI": "defmini", "BENTHIN": "", "UNI R":"defuniR", "UNI L":"defuniL"}
    for item, value in vichet_list.items():
        if item == service:
            vichet_for_server(value, height, weight, request)

def vichet_for_server(service, height, weight, request):
    try:
        response = requests.get(f"{SERVER_URL}/{service}?height={height}&weight={weight}")
        if response.status_code == 200:
            admin_panel(request)
    except requests.exceptions.RequestException as e:
        return

def admin_panel(request):
    try:
        response = requests.get(f"{SERVER_URL}/get_waregouse")
        if response.status_code == 200:
            result = response.json()
            return templates.TemplateResponse(request=request, name="admin.html", context={"result": result, "name" : "весь склад комплеткации"})
        else:
            return f"error: {response.status_code}"
    except Exception as e:
        print(f"Ошибка: {e}")
        return "error"

@app.get("/try_up/{item_id}", response_class=HTMLResponse)
async def edit_form(
    request: Request,
    item_id: int
):
    return templates.TemplateResponse(request=request, name="try_update.html", context={"order": item_id})

@app.post("/edit/{item_id}", response_class=HTMLResponse)
async def edit_form(
    request: Request,
    item_id: int,
    amount: int = Form(...),
):
    try:
        print("umbulichkla delau")
        response = requests.get(f"{SERVER_URL}/update?id={item_id}&quantity={amount}")
        if response.status_code == 200:
            print("umbulichkla")
            return RedirectResponse(url=f"/all/36863686", status_code=303)
        else:
            return f"error: {response.status_code}/{response.text}"
    except requests.exceptions.RequestException as e:
        print(e)
        return

def get_not_all(name, request):
    try:
        response = requests.get(f"{SERVER_URL}/get_waregouse")
        if response.status_code == 200:
            result = []
            for i in response.json():
                if i['Category'] == name:
                    result.append(i)
            return templates.TemplateResponse(request=request, name="admin.html", context={"result": result, "name": name})
        else:
            return f"error: {response.status_code}"
    except:
        return "error"
