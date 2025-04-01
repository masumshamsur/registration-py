from fastapi import APIRouter, Depends, Form, HTTPException
from src.database import get_db
from bson import ObjectId

router = APIRouter()

@router.post("/submit")
async def submit_form(
    firstname: str = Form(...),
    lastname: str = Form(...),
    country: str = Form(...),
    gender: str = Form(...),
    db=Depends(get_db)
):
    user_data = {
        "firstname": firstname,
        "lastname": lastname,
        "country": country,
        "gender": gender
    }
    result = db["users"].insert_one(user_data)  # Insert the user and get the inserted ID
    return {"message": "Data saved successfully!", "user_id": str(result.inserted_id)}

@router.get("/users")
async def get_users(db=Depends(get_db)):
    users = list(db["users"].find({}, {"_id": 1, "firstname": 1, "lastname": 1, "country": 1, "gender": 1}))

    # Convert ObjectId to string and handle missing keys safely
    user_list = [
        {
            "_id": str(user["_id"]),
            "firstname": user.get("firstname", ""),  # Avoid KeyError
            "lastname": user.get("lastname", ""),    # Avoid KeyError
            "country": user.get("country", "N/A"),   # Default value if missing
            "gender": user.get("gender", "N/A")      # Default value if missing
        }
        for user in users
    ]

    return {"users": user_list}

@router.delete("/delete/{user_id}")
async def delete_user(user_id: str, db=Depends(get_db)):
    try:
        obj_id = ObjectId(user_id)  # Validate ObjectId
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format")

    result = db["users"].delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully!"}
