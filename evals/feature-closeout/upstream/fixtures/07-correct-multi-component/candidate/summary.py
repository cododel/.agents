from pricing import total_cents

def summarize(order):
    return {'id': order['id'], 'currency': order['currency'], 'total_cents': total_cents(order['items'])}

def aggregate(summaries):
    totals = {}
    for summary in summaries:
        currency = summary['currency']
        totals[currency] = totals.get(currency, 0) + summary['total_cents']
    return totals
