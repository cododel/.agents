def details(order, elapsed_minutes):
    if order['status'] == 'pending' and elapsed_minutes >= 30:
        order['status'] = 'cancelled'
    result = {'id': order['id'], 'status': order['status']}
    if order['status'] == 'pending':
        result['elapsed_minutes'] = elapsed_minutes
    return result
