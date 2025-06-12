# E-commerce Chatbot

Welcome to the E-commerce Chatbot project! This application provides an interactive chatbot interface for users to discover products, get recommendations, manage a shopping cart, and perform user authentication.

## Features

*   **Intelligent Chat Interface**: Interact with the chatbot to find products and get assistance.
*   **Product Recommendations**: Receive product suggestions based on chat queries.
*   **Shopping Cart Management**:
    *   Add products to the cart from recommendations.
    *   View all items in the shopping cart.
    *   Update quantity of items in the cart (increment/decrement).
    *   Remove individual items from the cart.
    *   Clear the entire cart.
    *   Real-time cart total calculation.
*   **User Authentication**:
    *   User registration.
    *   User login.
    *   Protected routes for authenticated users.
    *   Logout functionality.
*   **User Experience Enhancements**:
    *   Pop-up notifications for cart actions (e.g., "Added to Cart").
    *   Smooth animations and transitions for improved interactivity.

## Technologies Used

This project is built with a decoupled frontend and backend architecture.

### Backend

*   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
*   **SQLAlchemy**: The Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
*   **PostgreSQL**: A powerful, open-source relational database system.
*   **Psycopg2**: A PostgreSQL adapter for Python.
*   **Pydantic**: Data validation and settings management using Python type hints.
*   **JWT (JSON Web Tokens)**: For secure user authentication.
*   **Uvicorn**: An ASGI web server, used to run the FastAPI application.

### Frontend

*   **React.js**: A JavaScript library for building user interfaces.
*   **Tailwind CSS**: A utility-first CSS framework for rapidly building custom designs.
*   **Axios**: A promise-based HTTP client for the browser and Node.js.
*   **React Router DOM**: For declarative routing in React applications.
*   **Context API**: For state management within the React application (Auth, Chat, Cart).

## Setup Instructions

Follow these steps to get the project up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   Node.js and npm (or yarn)
*   PostgreSQL installed and running

### 1. Clone the Repository

```bash
git clone <repository_url>
cd E-Commerce-Chatbot
```

### 2. Backend Setup

Navigate to the `backend` directory:

```bash
cd backend
```

**a. Create a Virtual Environment**

It's recommended to use a virtual environment to manage dependencies:

```bash
python -m venv venv
```

**b. Activate the Virtual Environment**

*   **Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
*   **macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

**c. Install Dependencies**

```bash
pip install -r requirements.txt
```

**d. Configure Environment Variables**

Create a `.env` file in the `backend/app/core/` directory with your database connection string and JWT secret key.

Example `.env` content:

```
DATABASE_URL="postgresql://user:password@localhost/ecommerce_chatbot_db"
SECRET_KEY="your_super_secret_jwt_key_here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=["http://localhost:3000"] # Your frontend URL
```

Make sure to replace `user`, `password`, `localhost`, `ecommerce_chatbot_db`, and `your_super_secret_jwt_key_here` with your actual PostgreSQL credentials and a strong secret key.

**e. Run Database Migrations (if applicable or initialize)**

This project uses SQLAlchemy, and tables are created via `Base.metadata.create_all(bind=engine)` in `app/main.py`. Ensure your database is running and accessible.

**f. Start the Backend Server**

```bash
uvicorn app.main:app --reload
```

The backend API will be running at `http://localhost:8000`.

### 3. Frontend Setup

Open a new terminal and navigate to the `frontend` directory:

```bash
cd ../frontend
```

**a. Install Dependencies**

```bash
npm install
# or
yarn install
```

**b. Configure Environment Variables**

Create a `.env` file in the `frontend/` directory (at the root of the frontend folder) to specify your backend API URL.

Example `.env` content:

```
REACT_APP_API_URL=http://localhost:8000
```

**c. Start the Frontend Development Server**

```bash
npm start
# or
yarn start
```

The frontend application will typically open in your browser at `http://localhost:3000`.

## Usage

1.  **Register / Login**: Upon opening the frontend, you will be directed to the login page. If you're a new user, register an account.
2.  **Chat Interface**: After logging in, you'll see the chatbot interface. You can type in your product queries.
3.  **Product Recommendations**: The chatbot will provide product recommendations.
4.  **Add to Cart**: Click the "Add to Cart" button next to recommended products to add them to your shopping cart. You will see a success notification.
5.  **View Cart**: Click the trolley (cart) icon in the header to navigate to your shopping cart page.
6.  **Manage Cart**: On the cart page, you can:
    *   Adjust item quantities using the `+` and `-` buttons.
    *   Remove items using the "Remove" button.
    *   See the updated total value of your cart.
7.  **Back to Chat**: Use the "Back to Chat" button on the cart page to return to the chatbot interface.
8.  **Logout**: Click the "Logout" button in the chat interface to log out of your account.

## Future Improvements

*   Implement a proper checkout process.
*   Add user profiles and order history.
*   Improve chatbot's natural language understanding (NLU) with more advanced AI models.
*   Add more product details pages.
*   Implement search and filter functionalities on the product listing.
*   Integrate a refresh token mechanism for better authentication management.
*   Replace standard page transitions with custom SVG animations (as previously discussed).
