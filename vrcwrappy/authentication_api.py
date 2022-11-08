from vrchatapi.api.authentication_api import AuthenticationApi as auth_api
from vrchatapi.model.two_factor_auth_code import TwoFactorAuthCode

class AuthenticationApi(auth_api):
    
    # verify2_fa but follows naming scheme
    # as well as taking in a string
    def verify_2fa(self, code: str, **kwargs):
        code = TwoFactorAuthCode(code)
        return self.verify2_fa(two_factor_auth_code=code, **kwargs)