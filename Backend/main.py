from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from email_validator import validate_email, EmailNotValidError
from app.auth_factory import AuthFactory
from app.concrete_factory import UserAuthFactory

app = FastAPI()

templates = Jinja2Templates(directory="templates")

auth_factory: AuthFactory = UserAuthFactory()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

