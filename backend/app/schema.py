from pydantic import BaseModel,EmailStr

class LoginRequest(BaseModel):
    username : str
    password : str


class RegisterRequest(BaseModel):
    first_name : str
    last_name : str = None
    username : str
    email : EmailStr
    password : str

# class User(LoginRequest):

class CropPredictionRequest(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float
    soil_type: str = None

class CropPredictionResponse(BaseModel):
    predicted_crop: str
