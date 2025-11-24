from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# Request model
class DateSortRequest(BaseModel):
    dates: List[str]
    output_format: Optional[str] = "%Y-%m-%d"  # Default format: YYYY-MM-DD

# Response model
class DateSortResponse(BaseModel):
    sorted_dates: List[str]
    count: int

# Common date format patterns to try
DATE_FORMATS = [
    "%Y-%m-%d",           # 2025-01-15
    "%m/%d/%Y",           # 01/15/2025
    "%d/%m/%Y",           # 15/01/2025
    "%Y/%m/%d",           # 2025/01/15
    "%B %d, %Y",          # January 15, 2025
    "%b %d, %Y",          # Jan 15, 2025
    "%d-%m-%Y",           # 15-01-2025
    "%Y.%m.%d",           # 2025.01.15
    "%m-%d-%Y",           # 01-15-2025
    "%d %B %Y",           # 15 January 2025
    "%d %b %Y",           # 15 Jan 2025
    "%Y%m%d",             # 20250115
]

def parse_date(date_str: str) -> datetime:
    #Try to parse a date string using multiple format patterns
    date_str = date_str.strip()
    
    # Try each format pattern
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue
    
    # If no format worked, raise an error
    raise ValueError(f"Could not parse date: '{date_str}'. May not be a supported format")

# GET REQUEST - Root
@app.get("/")
def read_root():
    return {"message": "Sort by date API up and running"}

# POST REQUEST - Sort dates
@app.post("/dates", response_model=DateSortResponse)
def sort_dates(request: DateSortRequest):
    try:
        # Validate that dates list is not empty
        if not request.dates:
            raise HTTPException(status_code=400, detail="Dates list cannot be empty")
        
        # Parse all date strings into datetime objects
        parsed_dates = []
        for date_str in request.dates:
            try:
                parsed_date = parse_date(date_str)
                parsed_dates.append(parsed_date)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid date format: '{date_str}'")
        
        # Sort the dates
        sorted_dates = sorted(parsed_dates)
        
        # Format the sorted dates according to the specified output format
        formatted_dates = []
        for date in sorted_dates:
            try:
                formatted_date = date.strftime(request.output_format)
                formatted_dates.append(formatted_date)
            except ValueError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid output format: '{request.output_format}'. Error: {str(e)}"
                    )
        
        return {
            "sorted_dates": formatted_dates,
            "count": len(formatted_dates)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sorting dates: {str(e)}")