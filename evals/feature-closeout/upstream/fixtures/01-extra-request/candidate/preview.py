def preview(cart, quantity, transport):
    return transport.post('/preview', {'unit_price_cents': cart['unit_price_cents'], 'quantity': quantity})['subtotal']

def checkout(cart_id, quantity, transport):
    return transport.post('/checkout', {'cart_id': cart_id, 'quantity': quantity})
