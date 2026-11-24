from rendering import available


def tick(purchase, enabled, result, send, audit):
    if purchase["state"] != "pending":
        return
    if not enabled:
        purchase["state"] = "closed"
        return
    if not available(result):
        return
    try:
        send(purchase["destination"], result["private_url"])
    except OSError as error:
        audit.append(("dispatch_error", purchase["id"], str(error)))
        return
    purchase["state"] = "delivered"
