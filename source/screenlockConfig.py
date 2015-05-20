import ConfigParser
# from passwordCrypto import encrypt
import passwordCrypto

class SLConfig(object):
    def __init__( self ):
        self.config = None
        self.readConfig()

    def passwordCheck(self, password):
        encryptedOldPassword = self.readPassword()
        if encryptedOldPassword.strip() == "":
            return True
        elif encryptedOldPassword == encrypt(password):
            return True
        else:
            return False

    def writePassword(self, password):
        encrypted_password = encrypt(password)
        self.config.set('Section', 'admin_override', encrypted_password)
        self.writeConfig()

    def readPassword(self):
        self.readConfig()
        encrypted_password = self.config.get('Section', 'admin_override')
        return encrypted_password

    def readConfig(self):
        self.config = ConfigParser.ConfigParser()
        with open(r'config.ini', 'r') as configfile:
            self.config.readfp(configfile)

    def writeConfig(self):
        with open(r'config.ini', 'wb') as configfile:
            self.config.write(configfile)

    def get(self, value):
        return self.config.get('Section', value)
