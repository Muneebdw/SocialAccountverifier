import random
import string



def generateOTP():
    otp = "INST"
    otp += ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
    return otp


if __name__ == '__main__':
    print(generateOTP())