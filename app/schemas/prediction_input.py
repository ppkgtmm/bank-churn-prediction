from enum import Enum
from pydantic import BaseModel, Field


class Gender(str, Enum):
    male = "M"
    female = "F"


class EducationLevel(str, Enum):
    college = "College"
    doctorate = "Doctorate"
    graduate = "Graduate"
    high_school = "High School"
    post_graduate = "Post-Graduate"
    uneducated = "Uneducated"
    unknown = "Unknown"


class PredictionInput(BaseModel):
    clientnum: str
    gender: Gender
    education_level: EducationLevel
    customer_age: int = Field(ge=0)
    dependent_count: int = Field(ge=0)
    months_on_book: int = Field(ge=0)
    total_relationship_count: int = Field(ge=0)
    months_inactive_12_mon: int = Field(ge=0)
    contacts_count_12_mon: int = Field(ge=0)
    credit_limit: float = Field(ge=0.0)
    total_revolving_bal: float = Field(ge=0.0)
    total_amt_chng_q4_q1: float = Field(ge=0.0)
    total_trans_amt: float = Field(ge=0.0)
    total_trans_ct: int = Field(ge=0)
    total_ct_chng_q4_q1: float = Field(ge=0.0)
    avg_utilization_ratio: float = Field(ge=0.0, le=1.0)
