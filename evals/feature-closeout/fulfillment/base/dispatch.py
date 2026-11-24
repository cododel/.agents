def tick(purchase, enabled, result, send, audit):
    if purchase["state"] != "pending" or not enabled or result is None:
        return
    if (result["job"] != purchase["job"]
            or result["kind"] != "original" or not result["playable"]):
        return
    try:
        send(purchase["destination"], result["private_url"])
    except OSError:
        audit.append(("dispatch_error", purchase["id"]))
        return
    purchase["state"] = "delivered"
