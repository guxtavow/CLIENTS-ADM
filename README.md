# User CRUD with Flask and Vue.js 3

This project is a **User CRUD** using **Flask (Python) as the backend** and  **Vue.js 3 (Composition API) with PrimeVue as the frontend** . It allows listing, creating, updating, and deleting users stored in  **MongoDB** .

---

## Technologies Used

### 🖥️ Backend:

* Python 3
* Flask
* Flask-PyMongo
* Flask-CORS
* MongoDB

### 🎨 Frontend:

* Vue.js 3 (Composition API + TypeScript)
* PrimeVue
* Axios

---

## Project Setup

### **1. Clone the Repository**

`git clone https://github.com/your-username/project.git `

`cd project `

---

## 🔥 Backend Setup (Flask)

### **2. Install Dependencies**

```
cd backend
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt

```

### **3. Configure MongoDB**

In this project i used **MONGODBATLAS**, so dont worry abou fix the config of database

### **4. Start the Flask Server**

`python app.py `

The backend will be running at  **[http://localhost:5000](http://localhost:5000)** .

---

## 🎨 Frontend Setup (Vue.js)

### **5. Install Dependencies**

```
cd frontend
npm install

```

### **6. Run the Frontend**

`npm run dev `

The frontend will be running at  **[http://localhost:5173]()** .

---

## API Endpoints

### 🔹 **Get all users**

`GET /api/users `

### 🔹 **Create a new user**

```
POST /api/new_users
```

### 🔹 **Update a user**

```
PUT /api/update_users/{usename}
Content-Type: application/json
{
  "username": "john_doe_updated"
}

```

### 🔹 **Delete a user**

`DELETE /api/delete_users/{username} `

---

## Common Errors & Solutions

| Error                     | Solution                                                                     |
| ------------------------- | ---------------------------------------------------------------------------- |
| `MongoDB not found`     | Make sure MongoDB is running (`mongod`or via Docker).                      |
| `CORS error`in frontend | CORS is already enabled in Flask (`flask_cors`). Adjust headers if needed. |
| `ModuleNotFoundError`   | Run `pip install -r requirements.txt`in the backend.                       |

---

## Status
Unfinished

## 📜 License

This project is open-source under the **MIT** license.
