import random
from django.contrib import messages
from django.shortcuts import redirect, render

# Complete Menu Data matching your exact items and .webp files
MENU_ITEMS = [
    # --- VEG ITEMS ---
    {
        'id': 1,
        'name': 'Paneer Butter Masala',
        'category': 'veg',
        'price': 220,
        'desc': 'Rich tomato gravy with soft paneer cubes',
        'image': 'paneer.webp',
    },
    {
        'id': 2,
        'name': 'Veg Biryani',
        'category': 'veg',
        'price': 180,
        'desc': 'Aromatic basmati rice cooked with fresh veggies',
        'image': 'biryani.webp',
    },
    {
        'id': 3,
        'name': 'Masala Dosa',
        'category': 'veg',
        'price': 90,
        'desc': 'Crispy crepe stuffed with spiced potato & chutney',
        'image': 'dosa.webp',
    },
    {
        'id': 4,
        'name': 'Idli',
        'category': 'veg',
        'price': 60,
        'desc': 'Soft, pillowy steamed rice',
        'image': 'idli.webp',
    },
    {
        'id': 5,
        'name': 'Veg Fried rice',
        'category': 'veg',
        'price': 150,
        'desc': 'Comfort in every bite!',
        'image': 'rice.webp',
    },
    # --- NON-VEG ITEMS ---
    {
        'id': 6,
        'name': 'Chicken Biryani',
        'category': 'non-veg',
        'price': 250,
        'desc': 'Classic dum biryani with tender chicken pieces',
        'image': 'chickenbiryani.webp',
    },
    {
        'id': 7,
        'name': 'Butter Chicken',
        'category': 'non-veg',
        'price': 280,
        'desc': 'Creamy spiced curry with tandoori chicken',
        'image': 'butterchicken.webp',
    },
    {
        'id': 8,
        'name': 'Mutton Rogan Josh',
        'category': 'non-veg',
        'price': 340,
        'desc': 'Slow-cooked Kashmiri style mutton curry',
        'image': 'mutton.webp',
    },
    {
        'id': 9,
        'name': 'Fish',
        'category': 'non-veg',
        'price': 360,
        'desc': 'Crispy on the outside, flaky and juicy on the inside.',
        'image': 'fish.webp',
    },
    {
        'id': 10,
        'name': 'Chicken 65',
        'category': 'non-veg',
        'price': 180,
        'desc': 'Spicy, deep-fried South Indian chicken appetizer',
        'image': 'c65.webp',
    },
]


# 1. Login & OTP View
def login_view(request):
  if request.method == 'POST':
    action = request.POST.get('action')

    if action == 'send_otp':
      username = request.POST.get('username')
      phone = request.POST.get('phone')
      otp = str(random.randint(1000, 9999))

      request.session['temp_user'] = username
      request.session['temp_phone'] = phone
      request.session['otp'] = otp

      # Prints OTP in VS Code terminal
      print('\n==============================')
      print(f'OTP for {username} ({phone}): {otp}')
      print('==============================\n')

      return render(
          request,
          'login.html',
          {'otp_sent': True, 'username': username, 'phone': phone},
      )

    elif action == 'verify_otp':
      entered_otp = request.POST.get('otp')
      if entered_otp == request.session.get('otp'):
        request.session['logged_in'] = True
        request.session['username'] = request.session.get('temp_user')
        request.session['phone'] = request.session.get('temp_phone')
        request.session['cart'] = []
        return redirect('/menu/?category=veg')
      else:
        messages.error(request, 'Invalid OTP! Check your VS Code terminal.')
        return render(
            request,
            'login.html',
            {
                'otp_sent': True,
                'username': request.session.get('temp_user'),
                'phone': request.session.get('temp_phone'),
            },
        )

  return render(request, 'login.html', {'otp_sent': False})


# 2 & 3. Menu View (With User Profile Details & Update Option)
def menu_view(request):
  if not request.session.get('logged_in'):
    return redirect('login')

  # Handle profile update (Email & Default Address) right from the menu page
  if request.method == 'POST':
    request.session['email'] = request.POST.get('email', '')
    request.session['address'] = request.POST.get('address', '')
    return redirect(f"/menu/?category={request.GET.get('category', 'veg')}")

  category = request.GET.get('category', 'veg')
  filtered_items = [item for item in MENU_ITEMS if item['category'] == category]

  return render(
      request,
      'menu.html',
      {
          'items': filtered_items,
          'category': category,
          'username': request.session.get('username'),
          'phone': request.session.get('phone'),
          'email': request.session.get('email', 'Not added'),
          'address': request.session.get('address', 'Not set yet'),
          'cart_count': len(request.session.get('cart', [])),
      },
  )


# 4a. Add to Cart -> Redirects to Cart Page
def add_to_cart(request, item_id):
  if not request.session.get('logged_in'):
    return redirect('login')

  cart = request.session.get('cart', [])
  for item in MENU_ITEMS:
    if item['id'] == item_id:
      cart.append(item)
      break

  request.session['cart'] = cart
  return redirect('cart')


# 4b. Cart Page
def cart_view(request):
  if not request.session.get('logged_in'):
    return redirect('login')

  cart_items = request.session.get('cart', [])
  total = sum(item['price'] for item in cart_items)
  return render(
      request, 'cart.html', {'cart_items': cart_items, 'total': total}
  )


def clear_cart(request):
  request.session['cart'] = []
  return redirect('cart')


# 4c. Address & Payment Page
def checkout_view(request):
  if not request.session.get('logged_in'):
    return redirect('login')

  cart_items = request.session.get('cart', [])
  total = sum(item['price'] for item in cart_items)

  if request.method == 'POST':
    address = request.POST.get('address')
    payment_method = request.POST.get('payment')
    request.session['address'] = address  # Saves delivery address to profile
    request.session['cart'] = []  # Clear cart after order

    return render(
        request,
        'success.html',
        {
            'username': request.session.get('username'),
            'address': address,
            'payment': payment_method,
            'total': total,
        },
    )

  return render(request, 'checkout.html', {'total': total})


# 5. Logout View
def logout_view(request):
  request.session.flush()
  return redirect('login')