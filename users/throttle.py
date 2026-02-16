from rest_framework.throttling import SimpleRateThrottle


class LoginThrottle(SimpleRateThrottle):

    #Strict throttle for login to prevent brute force.
    #Applies only to anonymous users.
    
    scope = "login"

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # don't throttle logged-in users
        return self.get_ident(request)

class RegisterThrottle(SimpleRateThrottle):
    
    #Even stricter throttle for registration.
    
    scope = "register"

    def get_cache_key(self, request, view):
     
        return self.get_ident(request)
