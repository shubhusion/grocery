# 🛒 Grocery Store App

Welcome to the Grocery Store App! This is a modern web application that allows users to browse and purchase groceries online.

## Introduction

The Grocery Store App provides a user-friendly interface for customers and Store Managers.

### Customer Features:

👀 View available grocery items in the store.  
🛒 Add grocery items to their shopping cart.  
🛍️ Make changes to the items in their shopping cart (e.g., update quantities).  
💳 Proceed to checkout to complete their purchase.

### Store Manager Features:

🏢 Create new sections in the grocery store app.  
🗑️ Remove existing sections from the grocery store app.  
📝 Update the information of sections in the grocery store app.  
❌ Delete sections from the grocery store app.  
➕ Create new products and associate them with specific sections.  
🔖 Remove existing products from the grocery store app.  
🔧 Update the information of products in the grocery store app.  
🗑️ Delete products from the grocery store app.

## Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask framework)
- **Database:** SQLite (via Flask-SQLAlchemy)
- **Authentication:** Flask-Login

## Prerequisites

Before running the Grocery Store App, ensure you have the following prerequisites:

1. Python 3.x installed on your machine.
2. Python virtual environment (optional but recommended).
3. Modern web browser that supports HTML5 and CSS3.

## Installation and Usage

### Without Docker

1. Clone the repository:
   ```
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```
   cd Code
   ```

3. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate      # For Windows
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Start the Flask development server:
   ```
   python app1.py
   ```

6. Open your web browser and visit `http://localhost:5000` to access the Grocery Store App.

### With Docker

1. Clone the repository:
   ```
   git clone <repository_url>
   ```

2. Navigate to the project directory:
   ```
   cd Code
   ```

3. Build the Docker image:
   ```
   docker build -t grocery-store-app .
   ```

4. Once the image is built successfully, you can run the Docker container:
   ```
   docker run -p 5000:5000 grocery-store-app
   ```

   This command will start the container, and the app will be accessible at `http://localhost:5000` in your web browser.

### Additional Notes

- If you're using Docker Toolbox on Windows or Mac, you might need to access the app using the IP address of the Docker machine instead of `localhost`. You can find the IP address by running `docker-machine ip` in your terminal.
- Ensure that no other service is running on port 5000 of your machine as Docker will map port 5000 of the container to port 5000 of the host by default.
- For production use, you may need to configure Docker with a production-ready web server like Nginx or deploy the Docker container to a cloud service provider.

With these steps, you should be able to run the Grocery Store App using both Docker and directly without Docker. If you encounter any issues, feel free to ask for further assistance!
