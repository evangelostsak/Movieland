"""
# 🎥 MovieLand: Your Personal Movie Hub

**MovieLand** is a Flask-based web application where users can explore, manage, and enjoy their personal movie collections. This project combines movie details fetched dynamically from the OMDb API with user management, interactive features like liking movies, and clean, responsive designs.

---

## 🚀 Features

### **1. Movie Management**
- Add movies by searching OMDb API for details like the title, release year, director, rating, poster, and IMDb link.
- Update movie details.
- Delete movies, with intelligent cleanup (movies unlinked from users with no connections are removed).

### **2. User Management**
- Add, update, and delete users.
- Associate movies with users.

### **3. Interactive Features**
- "Like" movies, incrementing their popularity.
- View users and their movie collections.

### **4. Dynamic & User-Friendly Design**
- Responsive and aesthetically pleasing layouts.
- Features include background images, blur effects, and styled components.

### **5. Robust Error Handling**
- Handles scenarios like invalid API keys, missing movie details, or database errors gracefully.

---

## 🛠️ Technologies Used

### **Backend:**
- Flask (with Flask-CORS)
- SQLAlchemy for ORM
- SQLite for database

### **Frontend:**
- Jinja2 for dynamic templates
- CSS (with responsive grids, hover effects, and modern designs)

### **APIs:**
- OMDb API for fetching movie details.

---

## 🖥️ Setup Instructions

### Prerequisites
1. **Python 3.8+**
2. **pip**: Package installer for Python.
3. **OMDb API Key**: [Get your OMDb API key here](https://www.omdbapi.com/apikey.aspx).
4. **Flask Secret Key**: Generate a secure random key (e.g., `os.urandom(24)`).

---

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/evangelostsak/Movieland.git
cd MovieLand
```

---

### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

---

### **Step 3: Add Environment Variables**
Create a `.env` file in the root directory:
```plaintext
OMDB_API_KEY=your_omdb_api_key
FLASK_SECRET_KEY=your_flask_secret_key
```

Or, set them manually in your deployment environment.

---

### **Step 4: Initialize the Database**
*Follow these steps to set up your database:*
1.	Open app.py and uncomment the following lines:
```bash
# Run once to create tables
with app.app_context():
    data.db.create_all()
```
2.	Run the app.py file:
```bash
python app.py
```

3. After running the script, the required database tables will be created in your database file (e.g., app.db).

4. Once the tables are created, comment out or remove the initialization code to prevent re-initializing the database in future runs.

---

### **Step 5: Run the Application**
Start the Flask development server:
```bash
flask run
```

Navigate to `http://127.0.0.1:5000` to access the app.

---

## 🌐 Deployment on PythonAnywhere

1. Upload all files, except `.env`.
2. Configure environment variables in the WSGI file.
3. Set up your static and template directories.
4. Reload your app in the PythonAnywhere dashboard.

---

## 📝 API Keys Required

1. **OMDb API Key**: For fetching movie details from the OMDb API.
   - Example: `OMDB_API_KEY=your_key_here`

2. **Flask Secret Key**: For session management and CSRF protection.
   - Example: `FLASK_SECRET_KEY=your_secret_here`

---

## ⚡ Functional Highlights

### Movie Operations
1. **Add Movie:** Fetch data dynamically from OMDb and add it to the database.
2. **Update Movie:** Modify details of an existing movie.
3. **Delete Movie:** Remove a movie and clean up unassociated entries.

### User Operations
1. **Create User:** Add new users.
2. **Update User:** Edit user details.
3. **Delete User:** Remove users and associated movies intelligently.

---

## ✨ Visual Highlights

### Homepage
A clean and modern homepage introducing the app's features.

### Users Page
A responsive user grid with interactive buttons to manage users and their movies.

### Movies Page
Displays all movies, showing posters, likes, and IMDb links.

---

## 💡 Future Enhancements
1. Advanced search functionality for movies.
2. Filter movies by genre, rating, or release year.
3. User authentication and role management.
4. Enhanced analytics for user and movie statistics.

---

## 🤝 Contributing
Contributions are welcome! Feel free to fork this repository and submit a pull request.

---

## 📧 Contact
For any inquiries or feedback, please contact: **baggtsak55@gmail.com**

Enjoy exploring **MovieLand**! 🎬✨
"""
 