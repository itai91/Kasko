from datetime import date
from typing import Dict, Optional, Union, Literal
from pydantic import BaseModel, EmailStr, conint, constr


class Person(BaseModel):
    first_name: constr(strip_whitespace=True, min_length=2)
    last_name: constr(strip_whitespace=True, min_length=2)
    id_number: constr(regex=r"^\d{9}$")
    phone: constr(regex=r"^05\d{8}$")
    email: EmailStr
    date_of_birth: date
    gender: Literal["male", "female"]
    is_smoker: bool
    height_cm: conint(ge=130, le=250)
    weight_kg: conint(ge=30, le=300)
    marital_status: Literal["single", "married", "divorced", "widowed"]
    occupation: Optional[str] = None
    dangerous_hobby: Optional[str] = None
    health_answers: Dict[int, Union[bool, str]]

