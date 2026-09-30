# FreshCart Market — Django Grocery E-Commerce Website

A grocery/supermarket e-commerce site built with Django, HTML, CSS and JavaScript.

## Features
- Browse groceries by category, search, and filter (live JS filtering + server-side search)
- Product detail pages with quantity selector
- Cart with add/remove/update quantity handled via JavaScript (AJAX), auto-recalculated totals
- Checkout form with validation, order summary, and confirmation message
- Orders and order items saved to the database
- Django Admin for full CRUD on categories, products and orders
- Responsive, modern design (cards, hover effects, animations, mobile nav)

## Models
- `Category`
- `Product` (ForeignKey → Category)
- `Order`
- `OrderItem` (ForeignKey → Order, ForeignKey → Product)

## Running the project in VS Code

1. **Open the folder in VS Code**
   - `File → Open Folder...` and select the `grocery_store` folder.

2. **Open a terminal in VS Code**
   - `Terminal → New Terminal`

3. **Create a virtual environment**
   ```
   python -m venv venv
   ```

4. **Activate the virtual environment**
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS / Linux:
     ```
     source venv/bin/activate
     ```
   VS Code may prompt you to select this environment as the workspace interpreter — click **Yes**.

5. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

6. **Apply database migrations**
   ```
   python manage.py migrate
   ```

7. **Load demo grocery products (optional but recommended)**
   ```
   python manage.py seed_data
   ```
   This adds sample categories and products, each linked to a real product photo (sourced from Wikimedia Commons). When you add your own products in the admin, you can either upload an image file or paste a photo URL into the "Image url" field.

8. **Create an admin account**
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to set a username, email, and password.

9. **Run the development server**
   ```
   python manage.py runserver
   ```

10. **Open the site**
    - Website: http://127.0.0.1:8000/
    - Admin panel: http://127.0.0.1:8000/admin/ (log in with the superuser you created)

## Adding your own products
Go to the admin panel → **Products** → **Add Product**, fill in name, description, price, category, image, etc., and save. It will immediately appear on the site since the site pulls data from the database.

## Project structure
```
grocery_store/
├── manage.py
├── requirements.txt
├── grocery_store/          # project settings, urls
├── store/                  # app: models, views, urls, admin, forms, cart logic
├── templates/store/        # HTML templates
├── static/store/           # CSS and JS
└── media/products/         # uploaded product images
```
