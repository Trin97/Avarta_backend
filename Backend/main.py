import asyncio
from fastapi import FastAPI, Form, HTTPException, Request, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from email_validator import validate_email, EmailNotValidError
from app.auth_factory import AuthFactory
from app.concrete_factory import UserAuthFactory
from app.image_processing import ImageHandler

app = FastAPI()

templates = Jinja2Templates(directory="templates")

auth_factory: AuthFactory = UserAuthFactory()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user_auth = auth_factory.create_user_auth()
    success = user_auth.login(email, password)
    if success:
        response = RedirectResponse(url="/home")
        return response
    else:
        raise HTTPException(status_code=400, detail="Invalid email or password. Please try again.")

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_post(request: Request, email: str = Form(...), password: str = Form(...)):
    print(email,password)
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return templates.TemplateResponse("register.html", {"request": request, "message": str(e)})

  
    if not any(char.isdigit() for char in password):
        return templates.TemplateResponse("register.html", {"request": request, "message": "Password must contain at least one digit."})
    if not any(char.isupper() for char in password):
        return templates.TemplateResponse("register.html", {"request": request, "message": "Password must contain at least one uppercase letter."})
    
    user_auth = auth_factory.create_user_auth()
    success, message = user_auth.register(email, password)
    if success:
        response = RedirectResponse(url="/home")
        return response
    else:
        return templates.TemplateResponse("register.html", {"request": request, "message": str(message)})



@app.post("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

handler = ImageHandler()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    return await handler.upload_image(file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

