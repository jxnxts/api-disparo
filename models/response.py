def Response(data, code, message, error):
    return {
        "data": data,
        "code": code,
        "message": message,
        "error": error
    }