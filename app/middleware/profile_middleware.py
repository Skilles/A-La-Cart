from django.http import HttpResponse
from django.shortcuts import redirect

import logging

def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)

        # If the user is authenticated but has not created a profile
        logging.info("path: " + str(request.path))
        print("path: " + str(request.path))
        if request.path == '/' and request.user.is_authenticated and request.user.profile.hash and request.user.profile.hash != '':
            return redirect('recommend')
        if not request.path == '/create-profile/' and request.user.is_authenticated and request.user.profile.calories == -1:
            logging.info("path: " + str(request.path))
            print("path: " + request.path)
            return redirect('create_profile')

        return response

    return middleware