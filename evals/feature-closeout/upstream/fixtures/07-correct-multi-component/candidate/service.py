from summary import summarize, aggregate

class OrderSummaryService:
    def __init__(self, store):
        self.store = store
    def get(self, tenant_id):
        records = sorted(self.store.for_tenant(tenant_id), key=lambda record: record['id'])
        summaries = [summarize(record) for record in records]
        return {'count': len(summaries), 'orders': summaries, 'totals_by_currency': aggregate(summaries)}
