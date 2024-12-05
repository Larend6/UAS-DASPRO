# Nama  = Narendra Augusta Srianandha
# NIM   = 2409116010

import pwinput
import csv
import time
import os
from prettytable import PrettyTable
from datetime import datetime

toko_path = r"D:\UNMUL\Tugas\Semester 1\DDP\UAS DDP CSV\data_toko.csv"
user_path = r"D:\UNMUL\Tugas\Semester 1\DDP\UAS DDP CSV\data_user.csv"
voucher_path = r"D:\UNMUL\Tugas\Semester 1\DDP\UAS DDP CSV\data_voucher.csv"
pembelian_path = r"D:\UNMUL\Tugas\Semester 1\DDP\UAS DDP CSV\data_pembelian.csv"

def write_log(message):
    with open("debug_log.txt", "a") as log_file:
        log_file.write(message + "\n")

def save_data_toko(data):
    with open(toko_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['no', 'waktu', 'items', 'jenis', 'harga'])
        for waktu, items in data.items():
            for item, details in items.items():
                for jenis, harga in details.items():
                    writer.writerow([waktu, item, jenis, harga])

def save_data_user(data):
    with open(user_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerows(data)

def save_data_voucher(data):
    with open(voucher_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["code", "discount", "used"])
        writer.writeheader()
        writer.writerows(data)

def save_data_pembelian(data_pembelian):
    with open(pembelian_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["username", "items"])
        writer.writeheader()
        for pembelian in data_pembelian:
            writer.writerow(pembelian)

def load_data_toko():
    try:
        data = {}
        with open(toko_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                waktu = row['waktu']
                if waktu not in data:
                    data[waktu] = []

                data[waktu].append({
                    "no": int(row['no']),
                    "items": row['items'],
                    "jenis": row['jenis'],
                    "harga": int(row['harga']),
                })
        return data
    except FileNotFoundError:
        print("File data toko tidak ditemukan.")
        return {}
    except ValueError as e:
        print(f"📍 Terjadi kesalahan dalam format data: {e}")
        return {}
    except Exception as e:
        print(f"📍 Terjadi kesalahan tidak terduga: {e}")
        return {}

def load_data_user():
    try:
        with open(user_path, "r") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                row["saldo"] = int(row["saldo"]) if row["saldo"].isdigit() else 0
                row["mora"] = int(row["mora"]) if row["mora"].isdigit() else 0
                data.append(row)
            return data
    except FileNotFoundError:
        return []

def load_data_voucher():
    try:
        data = []
        with open(voucher_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append({
                    "code": row["code"],
                    "discount": int(row["discount"]),
                    "used": row["used"].lower() == "true"
                })
        return data
    except FileNotFoundError:
        print("File data voucher tidak ditemukan.")
        return []
    except ValueError as e:
        print(f"📍 Terjadi kesalahan dalam format data voucher: {e}")
        return []
    except Exception as e:
        print(f"📍 Terjadi kesalahan tidak terduga: {e}")
        return []

def load_data_pembelian():
    try:
        with open(pembelian_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append({
                    'username': row.get('username', '').strip(),
                    'items': row.get('items', '').strip()
                })
            return data
    except FileNotFoundError:
        print("File data_pembelian.csv tidak ditemukan, membuat file baru...")
        return []
    except Exception as e:
        print(f"Terjadi kesalahan saat memuat data pembelian: {e}")
        return []

role_user = None
user = None

def main():
    os.system("cls")
    while True:
        print("\n====================================================")
        print("|              🔪 TEYVAT BLACKSMITH 🏹             |")
        print("====================================================")
        print("|                    1. Login                      |")
        print("|                    2. Daftar                     |")
        print("|                    3. Keluar                     |")
        print("====================================================")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            username, role_user = login()
            if username:
                if role_user == "Traveler":
                    menu_user_traveler(username)
                elif role_user == "NPC":
                    menu_user_npc(username)
                else:
                    print("📍 Role pengguna tidak valid.")
        elif pilihan == '2':
            register()
        elif pilihan == '3':
            keluar_program()
        else:
            print("📍 Pilihan tidak valid.")

def login():
    os.system("cls")
    data_user = load_data_user()
    if not data_user:
        print("📍 Data pengguna tidak ditemukan. Silakan tambahkan data pengguna terlebih dahulu.")
        return None, None

    sisa_coba = 3
    while sisa_coba > 0:
        try:
            print("\n+================================================+")
            print("|                 📢 MENU LOGIN 📢               |")
            print("+================================================+")
            username = input("🔹 Masukkan username (Ketik 0 untuk kembali): ").strip()
            
            if username == '0':
                print("📍 Anda akan diarahkan ke menu utama")
                input("Tekan enter untuk melanjutkan...")
                return None, None

            user_data = next((user for user in data_user if user['username'] == username), None)
            if not user_data:
                print("📍 Username tidak ditemukan. Silakan coba lagi.")
                continue

            password = pwinput.pwinput("🔹 Masukkan password: ")
            if user_data["password"] == password:
                role_user = user_data.get('role', 'Unknown')
                print("Login berhasil!")
                print(f"Selamat datang, {username}!")
                input("Tekan enter untuk melanjutkan...")
                return username, role_user
            else:
                sisa_coba -= 1
                print(f"📍 Password salah. Sisa coba Anda adalah {sisa_coba}.")
                if sisa_coba == 0:
                    print("📍 Anda sudah mencapai batas maksimal coba.")
                    print("Harap menunggu sebentar untuk mencoba kembali.")
                    for x in range(3, 0, -1):
                        time.sleep(1)
                        print(f"Anda akan diarahkan ke menu utama dalam {x} detik.")
                    return None, None
        except KeyboardInterrupt:
            keluar_program()
        except Exception as e:
            print(f"📍 Terjadi kesalahan: {e}")

def register():
    os.system("cls")
    data_user = load_data_user()
    data_pembelian = load_data_pembelian()
    username = None

    while True:
        try:
            if username is None:
                os.system("cls")
                print("\n+================================================+")
                print("|               📝 MENU REGISTER 📝              |")
                print("+================================================+")
                print("Note: Ketik 0 untuk kembali")
                
                username = input("🔸 Masukkan username (5-20 karakter): ").strip()
                if username == '0':
                    print("Anda akan diarahkan ke menu utama")
                    time.sleep(0.5)
                    main()
                elif not username:
                    print("📍 Username tidak boleh kosong!")
                    input("Tekan enter untuk melanjutkan...")
                    username = None
                    continue
                elif any(user['username'] == username for user in data_user):
                    print("📍 Username telah digunakan")
                    input("Tekan enter untuk melanjutkan...")
                    username = None
                    continue
                elif len(username) < 5 or len(username) > 20:
                    print("📍 Username minimal 5 karakter dan maksimal 20 karakter!")
                    input("Tekan enter untuk melanjutkan...")
                    username = None
                    continue

            password = input("🔸 Masukkan password (5-20 karakter): ").strip()
            if not password:
                print("📍 Password tidak boleh kosong!")
                input("Tekan enter untuk melanjutkan...")
                continue
            elif len(password) < 5 or len(password) > 20:
                print("📍 Password minimal 5 karakter dan maksimal 20 karakter!")
                input("Tekan enter untuk melanjutkan...")
                continue
            
            role = 'NPC'
            saldo = 0
            mora = 0
            user_baru = {
                'username': username,
                'password': password,
                'role': role,
                'saldo': saldo,
                'mora': mora
            }
            data_user.append(user_baru)
            save_data_user(data_user)

            user_pembelian = {
                'username': username,
                'items': ''
            }
            data_pembelian.append(user_pembelian)
            save_data_pembelian(data_pembelian)

            print("\n🎉 Akun telah berhasil didaftarkan!✨")
            print("Silahkan login untuk berbelanja di Teyvat Blacksmith")
            input("\nTekan enter untuk melanjutkan...")
            main()
            break
        except KeyboardInterrupt:
            keluar_program()
        except Exception as e:
            print(f"📍 Terjadi kesalahan: {e}")
            username = None

def menu_user_npc(username):
    os.system("cls")
    data_user = load_data_user()
    user_data = next((u for u in data_user if u["username"] == username), None)

    if not user_data:
        print("📍 Data pengguna tidak ditemukan.")
        return

    saldo = int(user_data["saldo"])
    while True:
        try:
            os.system("cls")
            print("\n+================================================+")
            print(r"+/\/\/\/\/\/\/\ 💯👤 MENU NPC 👤💯 /\/\/\/\/\/\/+")
            print("+================================================+")
            print("|                Anda adalah NPC!                |")
            print("|       Anda hanya dapat melihat barang saja     |")
            print("|             Ingin beli senjata juga?           |")
            print("|               Jadilah Traveler dan             |")
            print("|             belilah senjata terkuat!           |")
            print("+================================================+")
            print("|               1. Lihat Senjata                 |")
            print("|               2. Upgrade Traveler              |")
            print("|               3. Top up saldo                  |")
            print("|               4. Informasi Profil              |")
            print("|               5. Keluar Program                |")
            print("+================================================+")
            pilihan = int(input("Masukkan pilihan: "))

            if pilihan == 1:
                lihat_senjata()
            elif pilihan == 2:
                saldo = upgrade_traveler(username)
            elif pilihan == 3:
                saldo = top_up_saldo(username)
            elif pilihan == 4:
                informasi_profil(username)
            elif pilihan == 5:
                keluar_program()
            else:
                print("📍 Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("📍 Input tidak valid. Silakan coba lagi.")
        except Exception as e:
            print(f"📍 Terjadi kesalahan: {e}")

def lihat_senjata():
    os.system("cls")
    data_toko = load_data_toko()
    if not data_toko:
        print("📍 Data toko tidak ditemukan atau kosong.")
        input("\nTekan enter untuk kembali...")
        return

    table = PrettyTable()
    table.field_names = ["No", "Nama Senjata", "Jenis Senjata", "Harga (Mora)"]

    jam = datetime.now().hour
    kategori_waktu = "Pagi" if 6 <= jam < 12 else "Siang" if 12 <= jam < 18 else "Malam" if 18 <= jam < 24 else "Pagi"

    found = False
    if kategori_waktu in data_toko:
        found = True
        for item in data_toko[kategori_waktu]:
            table.add_row([item["no"], item["items"], item["jenis"], item["harga"]])

    if found:
        print("\n")
        table.title = f"Daftar Senjata pada Waktu {kategori_waktu}".upper()
        print(table)
    else:
        print(f"📍 Tidak ada senjata yang tersedia untuk kategori waktu '{kategori_waktu}'.")

    input("\nTekan enter untuk melanjutkan...")

def upgrade_traveler(username):
    os.system("cls")
    data_user = load_data_user()
    user_data = next((u for u in data_user if u["username"] == username), None)

    if not user_data:
        print("📍 Data pengguna tidak ditemukan. Silakan login kembali.")
        return None

    saldo = int(user_data["saldo"])

    print("\n+========================================================+")
    print("|                    UPGRADE TRAVELER                    |")
    print("+========================================================+")
    print("\nApakah Anda ingin menjadi Traveler?")
    print("Biaya akan dikenakan sebesar Rp. 100.000.")
    print("1. Ya")
    print("2. Tidak")
    pilihan = input("Masukkan pilihan: ")

    if pilihan == "1":
        if saldo < 100000:
            print("📍 Saldo Anda tidak mencukupi.")
            print("Silakan lakukan top-up saldo terlebih dahulu.")
            input("\nTekan enter untuk melanjutkan...")
            return saldo
        saldo -= 100000
        user_data["saldo"] = saldo
        user_data["role"] = "Traveler"
        save_data_user(data_user)
        print("🎉Anda telah menjadi Traveler! Selamat menjelajah Teyvat Blacksmith!🎉")
        input("\nTekan enter untuk melanjutkan...")
        menu_user_traveler(username)
    elif pilihan == "2":
        print("Anda tetap sebagai NPC.")
    else:
        print("📍 Pilihan tidak valid. Silakan coba lagi.")
    return saldo

def top_up_saldo(username):
    os.system("cls")
    data_user = load_data_user()
    user_data = next((u for u in data_user if u["username"] == username), None)

    if not user_data:
        print("📍 Data pengguna tidak ditemukan.")
        return

    try:
        max_saldo = 1000000
        saldo = int(user_data["saldo"])

        print("\n+========================================================+")
        print("|                     TOP UP SALDO                       |")
        print("+========================================================+")
        print("Maksimum nilai penambahan saldo adalah Rp.1.000.000")
        jumlah_top_up = int(input("Masukkan jumlah saldo yang ingin ditambahkan: "))

        if jumlah_top_up <= 0:
            print("📍 Jumlah saldo harus lebih besar dari 0.")
        elif saldo + jumlah_top_up > max_saldo:
            print(f"📍 Jumlah saldo tidak boleh lebih besar dari Rp. {max_saldo:,.0f}".replace(',', '.'))
        else:
            saldo += jumlah_top_up
            user_data["saldo"] = saldo
            save_data_user(data_user)
            print(f"Saldo telah berhasil ditambah! Saldo Anda sekarang: Rp. {saldo:,}".replace(',', '.'))
            input("\nTekan enter untuk melanjutkan...")
    except ValueError:
        print("📍 Input tidak valid. Silakan masukkan angka.")
    return saldo

def informasi_profil(username):
    os.system("cls")
    data_user = load_data_user()
    data_pembelian = load_data_pembelian()

    user_data = next((user for user in data_user if user["username"] == username), None)
    if not user_data:
        print("📍 Data pengguna tidak ditemukan.")
        return

    pembelian_user = [p["items"] for p in data_pembelian if p["username"] == username]
    senjata = pembelian_user[0].split(", ") if pembelian_user and pembelian_user[0] else []

    table_profile = PrettyTable()
    table_profile.field_names = ["Informasi", "Detail"]
    table_profile.align["Informasi"] = "l"
    table_profile.align["Detail"] = "l"

    table_profile.add_row(["Username", user_data['username']])
    table_profile.add_row(["Role", user_data['role']])
    table_profile.add_row(["Saldo", f"Rp. {user_data['saldo']:,}".replace(',', '.')])
    table_profile.add_row(["Mora", f"{user_data['mora']}"])

    print("\n+========================================================+")
    print("|                       Informasi Profil                 |")
    print("+========================================================+")
    print(table_profile)

    table_weapons = PrettyTable()
    table_weapons.field_names = ["No", "Senjata"]
    table_weapons.align["No"] = "r"
    table_weapons.align["Senjata"] = "l"

    if senjata:
        for idx, s in enumerate(senjata, start=1):
            table_weapons.add_row([idx, s])
    else:
        table_weapons.add_row(["-", "Belum memiliki senjata."])

    print("\n+========================================================+")
    print("|                   Senjata yang Dimiliki                |")
    print("+========================================================+")
    print(table_weapons)
    input("\nTekan enter untuk kembali ke menu utama...")

def menu_user_traveler(username):
    os.system('cls')
    mora = 0
    data_user = load_data_user()
    user_data = next((u for u in data_user if u["username"] == username), None)

    if not user_data:
        print("📍 Data pengguna tidak ditemukan.")
        return

    mora = user_data["mora"]

    while True:
        try:
            print("\n+================================================+")
            print(r"+\/\/\/\/\/\ 💯👤 MENU TRAVELER 👤💯 \/\/\/\/\/\/+")
            print("+================================================+")
            print("|          Ad Astra Abyssosque, Traveler!        |")
            print("|           Butuh senjata terkuat untuk          |")
            print("|              Melibas Spiral Abyss?             |")
            print("|       Belilah senjata di Teyvat Blacksmith     |")
            print("|           Dan ratakanlah pasukan Abyss!        |")
            print("+================================================+")
            print("|               1. Lihat Senjata                 |")
            print("|               2. Beli Senjata                  |")
            print("|               3. Tukar Mora                    |")
            print("|               4. Top up saldo                  |")
            print("|               5. Informasi Profil              |")
            print("|               6. Keluar Program                |")
            print("+================================================+")
            pilihan = int(input("Masukkan pilihan: "))
            if pilihan == 1:
                lihat_senjata()
            elif pilihan == 2:
                new_mora = beli_senjata(username)
                if new_mora is not None:
                    mora = new_mora
            elif pilihan == 3:
                result = tukar_mora(username)
                if result is not None:
                    saldo, mora = result
            elif pilihan == 4:
                top_up_saldo(username)
            elif pilihan == 5:
                informasi_profil(username)
            elif pilihan == 6:
                keluar_program()
            else:
                print("📍 Pilihan tidak valid. Silakan coba lagi.")
        except ValueError:
            print("📍 Input tidak valid. Silakan coba lagi.")

def beli_senjata(username):
    data_toko = load_data_toko()
    if not data_toko:
        print("📍 Data toko tidak ditemukan atau kosong.")
        return None

    os.system("cls")
    print("\n+================================================+")
    print("|                  BELI SENJATA                  |")
    print("+================================================+")

    data_pembelian = load_data_pembelian()
    data_voucher = load_data_voucher()

    jam = datetime.now().hour
    kategori_waktu = "Pagi" if 6 <= jam < 12 else "Siang" if 12 <= jam < 18 else "Malam" if 18 <= jam < 24 else "Pagi"

    print(f"Senjata yang tersedia pada waktu {kategori_waktu}: ")
    if kategori_waktu not in data_toko:
        print("Tidak ada senjata yang tersedia untuk kategori waktu ini.")
        return None

    data_user = load_data_user()
    user_data = next((u for u in data_user if u["username"] == username), None)
    if not user_data:
        print("📍 Data pengguna tidak ditemukan.")
        return None

    mora = int(user_data["mora"])

    print(f"Mora Anda saat ini: {mora} Mora\n")

    for item in data_toko[kategori_waktu]:
        print(f"{item['no']}. {item['items']} - {item['jenis']} - Harga: {item['harga']} Mora")

    try:
        data_user = load_data_user()
        user_data = next((u for u in data_user if u["username"] == username), None)
        if not user_data:
            print("📍 Data pengguna tidak ditemukan.")
            return None

        mora = int(user_data["mora"])

        pilihan = int(input("\nMasukkan nomor senjata yang ingin dibeli: "))
        item_terpilih = next((item for item in data_toko[kategori_waktu] if item["no"] == pilihan), None)

        if not item_terpilih:
            print("Senjata tidak ditemukan.")
            return mora

        harga = item_terpilih["harga"]
        diskon = 0

        print("\n+========================================================+")
        print("|                        VOUCHER                         |")
        print("+========================================================+")
        print("Voucher yang tersedia:")
        voucher_tersedia = [voucher for voucher in data_voucher if not voucher["used"]]
        if voucher_tersedia:
            for idx, voucher in enumerate(voucher_tersedia, 1):
                print(f"{idx}. {voucher['code']} - Diskon: {voucher['discount']}%")
        else:
            print("Tidak ada voucher yang tersedia.")

        kode_voucher = input("\nMasukkan kode voucher (atau tekan Enter untuk tidak menggunakan): ").strip()
        if kode_voucher:
            voucher = next((v for v in voucher_tersedia if v["code"] == kode_voucher), None)
            if voucher:
                diskon = voucher["discount"]
                for v in data_voucher:
                    if v["code"] == kode_voucher:
                        v["used"] = True
                        break
                save_data_voucher(data_voucher)
                print(f"Voucher berhasil digunakan! Diskon {diskon}%")
            else:
                print("📍 Voucher tidak valid atau sudah digunakan.")

        harga_setelah_diskon = harga - (harga * diskon // 100)
        print(f"Harga asli: {harga} Mora, Diskon: {diskon}%, Harga setelah diskon: {harga_setelah_diskon} Mora")

        if mora < harga_setelah_diskon:
            print("\nMora Anda tidak mencukupi untuk pembelian ini!")
            print("Apakah Anda ingin menukar saldo menjadi Mora?")
            print("1. Ya")
            print("2. Tidak")
            pilihan = int(input("Pilihan: "))
            if pilihan == 1:
                tukar_mora(username)
                return mora
            elif pilihan == 2:
                print("Pembelian dibatalkan.")
                return mora
            else:
                print("Pilihan tidak valid.")
                return mora

        mora -= harga_setelah_diskon
        user_data["mora"] = mora

        pembelian_user = next((p for p in data_pembelian if p["username"] == username), None)
        senjata = item_terpilih["items"]
        if pembelian_user:
            pembelian_user["items"] = f"{pembelian_user['items']}, {senjata}" if pembelian_user["items"] else senjata
        else:
            data_pembelian.append({"username": username, "items": senjata})

        save_data_user(data_user)
        save_data_pembelian(data_pembelian)
        save_data_voucher(data_voucher)

        print("\n+========================================================+")
        print("|                    PEMBELIAN BERHASIL                  |")
        print("+========================================================+")
        print(f"Berhasil membeli {senjata} seharga {harga_setelah_diskon} Mora!")
        input("\nTekan enter untuk melanjutkan...")
        return mora

    except ValueError:
        print("📍 Input tidak valid. Pastikan Anda memasukkan nomor yang sesuai.")
    except Exception as e:
        print(f"📍 Terjadi kesalahan: {e}")
    return mora

def tukar_mora(username):
    data_user = load_data_user()
    user_data = next((u for u in data_user if u["username"] == username), None)

    if not user_data:
        print("📍 Data pengguna tidak ditemukan.")
        return None, None

    try:
        konversi_mora = 100
        saldo = int(user_data["saldo"])
        mora = int(user_data["mora"])

        os.system("cls")
        print("\n+========================================================+")
        print("|                       TUKAR MORA                       |")
        print("+========================================================+")
        print(f"Saldo Anda saat ini: Rp. {saldo:,}".replace(',', '.'))
        jumlah_tukar = int(input("Masukkan jumlah uang yang ingin ditukar ke Mora (1 Mora = Rp. 100): Rp. "))

        if jumlah_tukar <= 0:
            print("📍 Jumlah yang dimasukkan tidak valid. Harus lebih besar dari 0.")
            input("\nTekan Enter untuk melanjutkan...")
            return saldo, mora

        if jumlah_tukar > saldo:
            print("📍 Saldo Anda tidak mencukupi untuk jumlah yang dimasukkan.")
            input("\nTekan Enter untuk melanjutkan...")
            return saldo, mora

        mora_earned = jumlah_tukar // konversi_mora
        saldo -= jumlah_tukar
        mora += mora_earned

        user_data["saldo"] = saldo
        user_data["mora"] = mora
        save_data_user(data_user)

        print("\n+========================================================+")
        print("|                    PENUKARAN BERHASIL                  |")
        print("+========================================================+")
        print(f"Berhasil menukar Rp. {jumlah_tukar:,} menjadi {mora_earned} Mora.")
        print(f"Saldo Anda sekarang: Rp. {saldo:,}".replace(',', '.') + f", Mora: {mora}")
        input("\nTekan Enter untuk melanjutkan...")
        return saldo, mora
    except ValueError:
        print("Input tidak valid. Masukkan angka yang sesuai.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    return None, None

def keluar_program():
    print("\n============== SELAMAT TINGGAL ==============")
    print("Terima kasih dan Sampai Jumpa :3")
    exit()

if __name__ == "__main__":
    main()