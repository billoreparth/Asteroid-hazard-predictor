from pydantic import BaseModel, Field, field_validator
from typing import Optional
import numpy as np


class DataFrameRowModel(BaseModel):
    absolute_magnitude_h: float = Field(..., description="float64, not null")
    jupiter_tisserand_invariant: float = Field(..., description="float64, not null")
    eccentricity: float = Field(..., description="float64, not null")
    inclination: float = Field(..., description="float64, not null")
    ascending_node_longitude: Optional[float] = Field(None, description="float64, nullable")
    perihelion_distance: float = Field(..., description="float64, not null")
    perihelion_argument: float = Field(..., description="float64, not null")
    mean_anomaly: float = Field(..., description="float64, not null")
    estimated_diameter_max: float = Field(..., description="float64, not null")
    relative_velocity_kmps: float = Field(..., description="float64, not null")
    miss_distance_in_astronomical: float = Field(..., description="float64, not null")
    is_potentially_hazardous: int = Field(..., description="int64, not null")

    
