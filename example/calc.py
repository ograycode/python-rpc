def add(request):
    data = request.data
    answer = data['a'] + data['b']
    request.respond({'answer': answer})
