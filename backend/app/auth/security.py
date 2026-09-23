from werkzeug.security import check_password_hash , generate_password_hash

def hash_password(password):
   # converts the user's plain-text password into a secure hash
   # before it is stored in the database.
   return generate_password_hash(password)


def verify_password(password, password_hash):
   # Compares the password entered during login with the previously hashed password.
   return check_password_hash(password_hash, password)