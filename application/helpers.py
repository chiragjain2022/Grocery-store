import os

def calculate_total_price_with_delivery(cart_items):
    total_price = 0
    total_saving = 0
    for cart_item in cart_items:
        total_price += cart_item.product.discount * cart_item.quantity
        total_saving += (cart_item.product.price - cart_item.product.discount) * cart_item.quantity
        
    delivery_charge = 50 if total_price < 100 else 0
    total_price_with_delivery = total_price + delivery_charge
    return total_price_with_delivery, delivery_charge, total_price, total_saving

ALLOWED_EXTENSIONS = set({'png', 'jpg', 'jpeg', 'gif', 'svg'})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rename_and_save_image(image, name, folder):
    image_ext = image.filename.split('.')[-1]
    secure_filename = f'{name}.{image_ext}'
    image_name = f'{name}.{image_ext}'
    image_path = os.path.join(folder, secure_filename)
    image.save(image_path)
    return image_name
