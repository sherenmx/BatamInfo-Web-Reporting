from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    # Diubah menjadi perbandingan langsung agar sesuai dengan data '123' di database
    return password == hashed_password

def verifikasi_login(username, password, user_data):
    if user_data:
        # Memanggil verify_password yang sekarang membandingkan teks biasa
        if username == user_data['username'] and verify_password(password, user_data['password']):
            return True
    return False