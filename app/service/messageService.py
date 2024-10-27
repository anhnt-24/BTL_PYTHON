def message(request):
    message=None
    if(request.session.get("message")):
        message=request.session.get("message")
        del request.session["message"]
    return message