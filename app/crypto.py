import base64
import bcrypt

def getDigest(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

def isPassword(password, digest):
    return bcrypt.hashpw(password, digest) == digest