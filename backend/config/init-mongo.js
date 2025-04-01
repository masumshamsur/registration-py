db = db.getSiblingDB("mydatabase");

db.createUser({
  user: "myUser",
  pwd: "myPass",
  roles: [{ role: "readWrite", db: "mydatabase" }]
});
db.createCollection("users"); // Create a collection named "users"

print("✅ MongoDB user created successfully!");
