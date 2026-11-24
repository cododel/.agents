import csv
import io

def export_csv(orders):
    out = io.StringIO(newline='')
    writer = csv.writer(out)
    writer.writerow(['order_id', 'amount_cents'])
    for order in orders:
        writer.writerow([order['order_id'], order['amount_cents']])
    return out.getvalue()
