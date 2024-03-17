from pydantic import BaseModel , validator , Field
from datetime import date
import re

class MovieData(BaseModel):
    title: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=15, max_length=250)
    release_date: date = Field(..., description="Date format: YYYY-MM-DD")
    director: str = Field(..., min_length=2, max_length=50)
    genre: str = Field(..., min_length=2, max_length=50)
    avg_rating: float = Field(..., ge=1, le=10)
    ticket_price: float = Field(..., ge=0)

    @validator('release_date')
    def valid_date(cls,value):
        re_exp = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        if not re_exp.match(str(value)):
            raise Exception("Invalid date format")
        if value > date.today():
            raise Exception("Release date must be in the past")
        return value
