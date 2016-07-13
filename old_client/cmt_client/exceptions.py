
class CmtApiAuthorizationRequired( Exception ):
    pass

class CmtApiNoAuthorizationCredentials( Exception ):
    pass

class CmtApiAuthorizationFailed( Exception ):
    pass

class CmtApiRequestMethodNotSupported( Exception ):
    pass

class CmtApiSslVerificationFailed( Exception ):
    pass

class CmtClientNoObjectsFound( Exception ):
    pass

class CmtServerError( Exception ):
    pass

class CmtApiNoURLSupplied( Exception ):
    pass
