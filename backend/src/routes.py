from fastapi import APIRouter, Depends, Form, HTTPException
from .database import get_db  # Ensure import is correct

router = APIRouter()

@router.post("/submit")
async def submit_form(
    firstname: str = Form(...),
    lastname: str = Form(...),
    country: str = Form(...),
    gender: str = Form(...),
    db=Depends(get_db)
):
    user_data = (firstname, lastname, country, gender)
    try:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (firstname, lastname, country, gender)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                user_data
            )
            user_id = cursor.fetchone()["id"]
        return {"message": "Data saved successfully!", "user_id": user_id}
    except Exception as e:
        print(f"❌ PostgreSQL Insert Error: {e}")
        raise HTTPException(status_code=500, detail="Database Insert Error")

@router.get("/users")
async def get_users(db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT id, firstname, lastname, country, gender FROM users;")
            users = cursor.fetchall()
        return {"users": users}
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching users")

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully!"}
    except Exception as e:
        print(f"❌ Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Error deleting user")
