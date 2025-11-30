# XOR CLI CRUD (Python + MySQL)

A simple CLI CRUD demo that encrypts data using a stream-XOR (keystream derived from SHA-256).

## Setup

1. Create MySQL database & user:

SQL Commands

CREATE DATABASE xor_crud CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'xor_user'@'localhost' IDENTIFIED BY 'xor_pass';
GRANT ALL PRIVILEGES ON xor_crud.* TO 'xor_user'@'localhost';
FLUSH PRIVILEGES;

2. Import scheme:

mysql -u xor_user -p xor_crud < db.sql

3. Install python deps:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

4. Run

python3 xor_cli_crud.py
