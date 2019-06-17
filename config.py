"""
{
    "ip": "127.0.0.1",  # VPS IP
    "password": "your_password",  # password to ssh-connection (user is always root), can be None
    "use_rsa_key": "key_name"
    # Set this field to None (no quotes) if no RSA-key was used to connect,
    # otherwise, put your key in the './private_keys' folder and enter it's name.
    # You don't need to enter a password line if RSA-key is implemented.

    # Can be used to set up multiple VPS, just expand the collection
}
"""

vps_list = [
    {
        "ip": "89.223.24.56",
        "password": "e653C-i41U4-g0EXd-SiNp1",
        "use_rsa_key": None
    }
]

vpn_data = {
    "user": "lich",
    "password": "yQaIkK1k8RWDzrBDvMrY"
}
