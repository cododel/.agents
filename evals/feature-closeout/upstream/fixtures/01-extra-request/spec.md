# Task: show the subtotal on quantity change
- R1: The preview subtotal uses the cart's already supplied integer unit price and selected quantity, in cents. Its inputs are fixed for the editing session; no live price lookup is needed for the preview.
- R2: Final checkout and its server-side authoritative pricing are outside the change. Leave them unchanged.
- R3: Return the updated subtotal after quantity changes. This fixture covers the preview calculation, not a rendered UI.
