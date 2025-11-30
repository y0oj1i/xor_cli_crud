#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI CRUD Application with XOR Stream Encryption (MySQL)
"""
import hashlib
import os
import pymysql
import binascii

# ======================
# XOR STREAM FUNCTIONS
# ======================
def gen_nonce():
    return os.urandom(16)

def keystream_generator(key: bytes, nonce: bytes, length: int):
    counter = 0
    output = b""
    while len(output) < length:
        data = key + nonce + counter.to_bytes(8, "big")
        block = hashlib.sha256(data).digest()
        output += block
        counter += 1
    return output[:length]

def xor_stream_encrypt(key: bytes, nonce: bytes, plaintext: bytes):
    ks = keystream_generator(key, nonce, len(plaintext))
    return bytes([p ^ k for p, k in zip(plaintext, ks)])

def xor_stream_decrypt(key: bytes, nonce: bytes, ciphertext: bytes):
    ks = keystream_generator(key, nonce, len(ciphertext))
    return bytes([c ^ k for c, k in zip(ciphertext, ks)])

# ======================
# MYSQL CONFIG
# ======================
DB_HOST = "localhost"
DB_USER = "xor_user"
DB_PASS = "xor_pass"
DB_NAME = "xor_crud"

# MASTER KEY (ubah sesuai keinginan)
MASTER_KEY = b"my-secret-key"

# ======================
# CONNECT
# ======================
def db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# ======================
# CRUD FUNCTIONS
# ======================
def create_item():
    text = input("Masukkan data yang ingin dienkripsi: ")
    nonce = gen_nonce()
    ct = xor_stream_encrypt(MASTER_KEY, nonce, text.encode())

    cn = db()
    with cn.cursor() as cur:
        cur.execute(
            "INSERT INTO items (nonce, data_enc) VALUES (%s, %s)",
            (binascii.hexlify(nonce).decode(), binascii.hexlify(ct).decode())
        )
    cn.commit()
    print("✔ Data berhasil disimpan dan dienkripsi.\n")

def read_items():
    cn = db()
    with cn.cursor() as cur:
        cur.execute("SELECT * FROM items")
        rows = cur.fetchall()

    print("\n=== DATA DALAM DATABASE ===")
    for r in rows:
        try:
            nonce = binascii.unhexlify(r["nonce"])
            ct = binascii.unhexlify(r["data_enc"])
            pt = xor_stream_decrypt(MASTER_KEY, nonce, ct).decode()
        except Exception as e:
            pt = f"[error decoding] {e}"
        print(f"ID: {r['id']} | Data: {pt}")
    print()

def update_item():
    item_id = input("Masukkan ID yang ingin diupdate: ")
    new_text = input("Masukkan data baru: ")

    nonce = gen_nonce()
    ct = xor_stream_encrypt(MASTER_KEY, nonce, new_text.encode())

    cn = db()
    with cn.cursor() as cur:
        cur.execute(
            "UPDATE items SET nonce=%s, data_enc=%s WHERE id=%s",
            (binascii.hexlify(nonce).decode(), binascii.hexlify(ct).decode(), item_id)
        )
    cn.commit()
    print("✔ Data berhasil diupdate.\n")

def delete_item():
    item_id = input("Masukkan ID yang ingin dihapus: ")

    cn = db()
    with cn.cursor() as cur:
        cur.execute("DELETE FROM items WHERE id=%s", (item_id,))
    cn.commit()
    print("✔ Data berhasil dihapus.\n")

# ======================
# MAIN MENU
# ======================
def main():
    while True:
        print("""
=== XOR STREAM CRUD (CLI) ===
1. Create (Encrypt & Save)
2. Read (Decrypt)
3. Update
4. Delete
0. Exit
""")
        choice = input("Pilih menu: ")

        if choice == "1":
            create_item()
        elif choice == "2":
            read_items()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Pilihan tidak valid.\n")

if __name__ == "__main__":
    main()
