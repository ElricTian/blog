import hmac


def encryption(password):
    # 密钥
    password = password.encode('utf-8')
    msg = 'Elric'.encode()
    new_password = hmac.new(password, msg=msg).hexdigest()
    return new_password


if __name__ == '__main__':
    password = encryption('9527')
    print(password)
