from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.http import HttpRequest


class EmailAndUsernameCredentialAuthBackend(ModelBackend):
    """A custom authentication backend for authenticate using email and username"""

    def authenticate(self, request, email=None, username=None, password=None, **kwargs):
        '''Custom authentication backend for authenticate using email and username'''
        
        User = get_user_model()
        
        user = None 
        
        # username or email both have same value. try to authenticate using username and email, 
        # if any of the cred matches, return the user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass 
        
        if not user: 
            try:    
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass 
        
        if user:
            if user.check_password(raw_password=password):
                return user
        return None 