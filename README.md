
# 🎥 MovieLand: Your Personal Movie Hub

**MovieLand** is a Flask-based web application that allows users to explore, manage, and personalize their movie collections. With integrated user authentication, profile management, and movie tracking, MovieLand provides a secure and interactive platform for movie enthusiasts. This project combines movie details fetched dynamically from the OMDb API with user management, interactive features like liking movies, and clean, responsive designs.

---

## 🚀 Features

### **🔑 User Authentication & Profiles**
- User Registration & Login: Secure authentication using hashed passwords.
- User Profiles: Each user has a profile with their own movie collection.

### **🎥 Movie Management**
- Add Movies: Search and fetch Movies from the OMDb API.
- Update movie details.
- Edit & Delete Movies: Users can only modify their own movies.
- Intelligent cleanup (movies unlinked from users with no connections are removed).
- Like Movies: Users can interact with movies by liking them.

### **📊 User Experience**
- Personalized Collections: Users can see all movies but can only manage their own.
- Profile Pictures
- Secure Sessions: Sessions prevent unauthorized access.
- With MovieLand, each user has a tailored experience while enjoying a collaborative and interactive movie platform. 🎬🍿

### **💻 Dynamic & User-Friendly Design**
- Responsive and aesthetically pleasing layouts.
- Features include background images, blur effects, and styled components.

### **🛡️ Robust Error Handling**
- Handles scenarios like invalid API keys, missing movie details, or database errors gracefully.

---

## 🛠️ Technologies Used

### **Backend:**
- Flask (with Flask-CORS)
- Werkzeug & UserMixin for hashing and User Authentication
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
#### **Check `.env.example` for guidance.**

---

### **Step 4: Initialize the Database**
*Follow these steps to set up your database:*
1.	Run db_init.py script in the console:
```bash
# Run once to create database and tables
# Make sure you are in the root directory
python3 db_init_.py
```

2. After running the script, the required database and all the tables will be created in the /data directory.

---

### **Step 5: Run the Application**
Start the Flask development server:
```bash
python3 app.py
```

Navigate to `http://127.0.0.1:5000` to access the app.

---

## 🌐 Try Out Movieland
https://evangelostsak.pythonanywhere.com/

---

## 📝 API Keys Required

1. **OMDb API Key**: For fetching movie details from the OMDb API.
   - Example: `OMDB_API_KEY=your_key_here`

2. **Flask Secret Key**: For session management and CSRF protection.
   - Example: `SECRET_KEY=your_secret_here`

---

## ⚡ Functional Highlights

### User Authentication
1. **Registration:** Create personal accounts securily using hashed passwords
2. **User Authentication:** Ensure every User gets his own session and enviroment.
3. **Login:** Login, Logout features for Users
4. **Forbidden Access:** Ensures login dependent pages are locked for unauthorised Users

### Movie Operations
1. **Add Movie:** Fetch data dynamically from OMDb and add it to the database.
2. **Update Movie:** Modify details of an existing movie.
3. **Delete Movie:** Remove a movie and clean up unassociated entries.
4. **Like Movie:** Like a Movie added by you or any other User

### User Operations
1. **Create Account:** Registers an account.
2. **Update User:** Edit account details, including adding Profile Pictures
3. **Delete User:** Remove Account and associated Movies intelligently.

---

## ✨ Visual Highlights

### Homepage
A clean and modern homepage introducing the app's features.

### Profile Page
A Responsive profile page featuring account's Movies and Movie actions. Account actions like Update or Delete Profile and Add Movie Pages.

### Users Page
A responsive user grid listing all Accounts.

### Movies Page
Displays all movies, showing posters, likes, and IMDb links.

### Registration and Login Pages
Clean Sign up, Sign in Pages that disapear after succesful login.

### Dynamic dropdown Menu
A modern addition that features the logged in user's Profile Picture and Name, Hovering the Dropdown Menu User gets a Logout button for the logout Page.

---

## 💡 Future Enhancements
1. Advanced search functionality for movies.
2. Filter movies by genre, rating, or release year.
3. Enhanced analytics for user and movie statistics.

---

## 🤝 Contributing
Contributions are welcome! Feel free to fork this repository and submit a pull request.

---

## 📧 Contact
For any inquiries or feedback, please contact: **baggtsak55@gmail.com**

Enjoy exploring **MovieLand**! 🎬✨
 