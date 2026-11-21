# 🍽️ Food Express - Online Food Ordering System (Django)

A full-stack web-based Food Ordering System built using **Python** and **Django**. The application features OTP-based user authentication, a collapsible user profile dropdown, separate Pure Veg and Non-Veg menu sections with dish images, a session-backed shopping cart, and a delivery address & payment checkout flow.

---

## ✨ Features

- **OTP-Based Login:** Users sign in using their username and phone number via a 4-digit One-Time Password (OTP) generated in the server console.
- **Interactive User Profile Dropdown:** Clicking the circular avatar icon in the top navigation bar opens a profile card displaying the user's verified phone number, email ID, saved delivery address, an inline profile editor, and logout functionality.
- **Category-Filtered Menus:** Dedicated **Pure Veg** and **Non-Veg** sections displaying dish photos, descriptions, and pricing in a responsive card grid.
- **Shopping Cart Management:** One-click **Add to Cart** redirects directly to the cart summary with live item count tracking, total bill calculation, and a clear-cart option.
- **Address & Payment Checkout:** Collects the delivery address (automatically saving it to the user's session profile) and supports multiple payment options (UPI, Credit/Debit Card, Cash on Delivery) with an order confirmation screen.

---

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Database & Sessions:** SQLite3 (Django Session Framework)

---

## 📂 Project Structure

```text
food_project/
│
├── manage.py
├── README.md
├── food_project/
│   ├── settings.py
│   └── urls.py
└── order_app/
    ├── urls.py
    ├── views.py
    ├── static/
    │   └── images/          # Dish images (.webp)
    └── templates/
        ├── login.html       # Username + Phone & OTP verification
        ├── menu.html        # Profile dropdown & Veg/Non-Veg menu grid
        ├── cart.html        # Shopping cart summary
        ├── checkout.html    # Delivery address & payment selection
        └── success.html     # Order confirmation page
