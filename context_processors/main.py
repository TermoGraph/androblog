from django.template.context_processors import request

def menu(request):
    auth = request.session.get('auth', 'false')
    name = request.session.get('name', 'none')

    return {'auth': auth, 'name': name}