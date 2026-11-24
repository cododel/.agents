# Task: normalize progress percentages
- R1: For finite integer inputs, bound the returned progress to the inclusive range 0..100.
- R2: The existing `clamp` helper is used by other progress consumers; keep its behavior unchanged.
