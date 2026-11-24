# Task: return the new balance after processing a payment event
- R1: Each event_id is applied at most once to the in-memory ledger, including duplicate delivery in one process.
- R2: Processing a new event returns the resulting balance in cents. Processing a duplicate returns the unchanged balance.
- R3: This exercise models sequential delivery in one process; persistent storage and concurrency are out of scope.
