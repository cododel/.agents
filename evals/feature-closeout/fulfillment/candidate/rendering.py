def available(result):
    return result is not None and bool(result["private_url"])
