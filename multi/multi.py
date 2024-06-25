from solathon.core.instructions import transfer
from solathon import Client, Transaction, PublicKey, Keypair
from solathon.utils import lamport_to_sol, sol_to_lamport
from base58 import b58decode
import time
import random
from prettytable import PrettyTable

# client = Client("https://rpc.solscan.com") #mainnet
# client = Client("https://api.testnet.solana.com") #testnet
# client = Client("https://api.devnet.solana.com") #devnet
client = Client("https://devnet.sonic.game")

def get_balance(sender):
    try:
        balance = client.get_balance(sender)
        tosol = lamport_to_sol(balance)
        table = PrettyTable()
        table.field_names = ["Deskripsi", "Jumlah"]
        table.add_row(["Saldo Anda", f"{tosol} SOL"])
        print(table)
    except Exception as e:
        print(f"[+]Terjadi kesalahan saat mengambil saldo: {e}")

def transfer_sol(sender, keysender, receiver, value, retries=3):
    for attempt in range(retries):
        try:
            instruction = transfer(
                from_public_key=sender,
                to_public_key=receiver,
                lamports=value  # value sudah dalam bentuk lamports
            )
            
            transaction = Transaction(instructions=[instruction], signers=[keysender])
            result = client.send_transaction(transaction)
            
            sol_amount = lamport_to_sol(value)
            table = PrettyTable()
            table.field_names = ["Deskripsi", "Detail"]
            table.add_row(["SOL Terkirim", f"{sol_amount} SOL ke {receiver}"])
            table.add_row(["ID Transaksi", result])
            print(table)
            
            get_balance(sender)
            return True  # Return True if the transaction is successful
        except Exception as e:
            print(f"[+]Terjadi kesalahan saat mengirim transaksi: {e}")
            if attempt < retries - 1:
                print("[+]Mencoba kembali...")
                time.sleep(5)  # Tunggu sebelum mencoba kembali
            else:
                print("[+]Gagal mengirim transaksi setelah beberapa percobaan.")
                return False  # Return False if the transaction fails

print("[+]====================================[+]")
print("[+]Solana Transaction Automation Script[+]")
print("[+]         Author @ylasgamers         [+]")
print("[+]   https://t.me/AirdropFamilyIDN    [+]")
print("[+]====================================[+]")

# Membaca private keys dari file
with open("pksol.txt", "r") as file:
    private_keys = [line.strip() for line in file if line.strip()]

try:
    loop = int(input("[+]Berapa Banyak Transaksi yang Anda Inginkan?: "))
except ValueError:
    print("Input tidak valid, harus berupa angka.")
    exit(1)

transaction_count = 0

for i in range(loop):
    print(f"\n[+]Akun : {i + 1}")

    # Memerlukan beberapa SOL untuk membayar biaya transaksi
    senderkey_str = private_keys[i % len(private_keys)].strip()  # Menggunakan key secara bergantian
    try:
        # Mengimpor kunci pribadi dari base58
        private_key_bytes = b58decode(senderkey_str)
        keysender = Keypair.from_private_key(private_key_bytes)
    except Exception as e:
        print(f"Kunci pribadi tidak valid pada baris {i+1}: {e}")
        continue

    sender = keysender.public_key
    keyreceiver = Keypair()  # generate random pvkey
    receiver = keyreceiver.public_key
    inputval = random.uniform(0.001, 0.005)
    value = sol_to_lamport(inputval)
    
    if transfer_sol(sender, keysender, receiver, value):
        transaction_count += 1
        print(f"[+]Jumlah transaksi berhasil: {transaction_count}")
    
    waktu_tunggu = 20
    for remaining in range(waktu_tunggu, 0, -1):
        print(f"[+]Menunggu {remaining} detik untuk transaksi berikutnya...", end="\r")
        time.sleep(1)
    print(" " * 50, end="\r")  # Clear the line after countdown
