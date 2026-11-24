class OrderStore:
    def __init__(self, records):
        self.records = list(records)
    def for_tenant(self, tenant_id):
        return [r for r in self.records if r['tenant_id'] == tenant_id]
