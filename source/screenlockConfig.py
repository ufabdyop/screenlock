import ConfigParser
import passwordCrypto

class SLConfig(object):
    def __init__( self ):
        self.config = None
        self.readConfig()

    def passwordCheck(self, password, item):
        encryptedOldPassword = self.readPassword(item)
        if encryptedOldPassword.strip() == "":
            return True
        elif encryptedOldPassword == passwordCrypto.encrypt(password):
            return True
        else:
            return False

    def writePassword(self, password, item):
        encrypted_password = passwordCrypto.encrypt(password)
        self.config.set('Section', item, encrypted_password)
        self.writeConfig()

    def writeKey(self,info,item):
        self.config.set('Section', item, info)
        self.writeConfig()

    def readPassword(self, item):
        self.readConfig()
        encrypted_password = self.config.get('Section', item)
        return encrypted_password

    def readConfig(self):
        self.config = ConfigParser.ConfigParser()
        with open(r'config.ini', 'r') as configfile:
            self.config.readfp(configfile)

    def writeConfig(self):
        with open(r'config.ini', 'wb') as configfile:
            self.config.write(configfile)
        self.convert_unix_line_endings_to_win(r'config.ini')

    def get(self, key):
        return self.config.get('Section', key)
        
    def convert_unix_line_endings_to_win(self, filename):
        text = open(filename, "U").read()
        text = text.replace("\n", "\r\n")
        filehandle = open(filename, "wb")
        filehandle.write(text)
        filehandle.close()
        
