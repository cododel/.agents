def preview(cart, quantity, transport):
    return cart['unit_price_cents'] * quantity

def checkout(cart_id, quantity, transport):
    return transport.post('/checkout', {'cart_id': cart_id, 'quantity': quantity})
