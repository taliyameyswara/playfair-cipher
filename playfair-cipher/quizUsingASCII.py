# === Fungsi untuk memformat teks sebelum enkripsi ===
import re


def format_message(msg):
    # Mengganti huruf J dalam teks menjadi huruf I
    msg = msg.replace('q', 'y')

    # Menggunakan ekspresi reguler untuk menghapus semua karakter selain huruf dan spasi
    msg = re.sub(r'[^a-zA-Z\s]', '', msg)

    i = 1
    while i < len(msg):
        # Mengecek apakah dua huruf dalam teks sama
        if msg[i-1] == msg[i]:
            # Jika sama, masukkan huruf 'w' di antara kedua huruf
            msg = msg[:i] + 'w' + msg[i:]
        i += 2

    if len(msg) % 2 != 0:  # Jika jumlah huruf ganjil,
        msg += 'w'  # tambahkan 'w' pada akhir teks

    # Mengembalikan teks berupa teks yang sudah diformat untuk dienkripsi
    return msg
# === Fungsi untuk membuat matriks 5x5 ===


def generate_matrix(key):
    # Inisialisasi matriks 5x5
    mat = [['' for _ in range(5)] for _ in range(5)]

    # Inisialisasi variabel flag dengan 26 elemen False
    flag = [False] * 26

    # Untuk melacak posisi saat ini dalam matriks
    # x untuk baris, y untuk kolom
    x, y = 0, 0

    # Menambahkan huruf dari kunci ke dalam matriks
    for char in key:
        # Mengganti huruf J dengan huruf I
        # ================ DISINI ================
        if char == 'q':
            char = 'y'

        # Variabel untuk menentukan posisi (index) huruf dalam alfabet
        index = ord(char) - ord('a')

        # Mengecek apakah huruf belum ada dalam matriks
        if not flag[index]:
            # Jika belum ada, maka huruf akan dimasukkan kedalam matriks
            mat[x][y] = char
            # Kemudian flag akan diinisialisasi menjadi True
            flag[index] = True
            # Increment untuk posisi kolom (y) saat ini ke kolom berikutnya
            y += 1

        if y == 5:  # Jika sudah sampai ke kolom ke-5
            x += 1  # maka baris (xa) akan di-increment,
            y = 0  # dan mengatur kolom kembali pada kolom pertama (ke-0)

    # Menambahkan huruf selanjutnya (huruf yang belum terdapat pada kunci)
    # (A-Z kecuali J yang diganti dengan I)
    for char in range(ord('a'), ord('z')+1):
        # ================ DISINI ================
        if char == ord('q'):  # Mengabaikan huruf J
            continue

        # Algoritma sama dengan loop sebelumnya
        index = char - ord('a')

        if not flag[index]:
            mat[x][y] = chr(char)
            flag[index] = True
            y += 1

        if y == 5:
            x += 1
            y = 0

    return mat  # Mengembalikan matriks yang berisi huruf


# === Fungsi untuk memformat teks hasil dekripsi ===
def format_message_decrypt(msg):
    # Mengganti huruf 'j' dalam teks menjadi 'i'
    # msg = msg.replace('j', 'i')

    # Mengganti huruf 'i' yang seharusnya menjadi 'j' kembali
    # ================ DISINI ================
    msg = msg.replace('q', 'y')

    # Menghilangkan huruf 'z' di akhir teks jika jumlah huruf ganjil
    if msg.endswith('w'):
        msg = msg[:-1]

    i = 1
    while i < len(msg) - 1:
        # Menghapus huruf z yang berada diantara huruf yang sama
        if msg[i-1] == msg[i+1]:
            msg = msg.replace('w', '')
        i += 2

    # Mengembalikan teks yang sudah diformat sebagai hasil dekripsi
    return msg


# === Fungsi untuk menyesuaikan posisi huruf pada matriks ===
def get_position(mat, char):
    # Loop untuk baris sebanyak 5x
    for row in range(5):
        # Loop untuk kolom sebanyak 5x
        for col in range(5):
            # Mengecek apakah elemen pada matriks pada posisi (row)(col) sama dengan huruf yang dicari
            if mat[row][col] == char:
                # Jika sama, kembalikan nilai kolom dan baris
                return (row, col)


# === Fungsi untuk mengenkripsi ===
# def encrypt(message, mat):
#     ciphertext = ''  # Variabel untuk menyimpan hasil dari enkripsi
#     i = 0

#     while i < len(message):
#         # Pasangan 2 Huruf
#         char1 = message[i]  # Huruf pertama
#         char2 = message[i+1]  # Huruf kedua

#         pos1 = get_position(mat, char1)  # Posisi pertama pada matriks
#         pos2 = get_position(mat, char2)  # Posisi keuda pada matriks

#         x1, y1 = pos1  # Baris dan kolom huruf pertama
#         x2, y2 = pos2  # Baris dan kolom huruf kedua

#         # Jika berada pada baris yang sama, geser ke kanan
#         if x1 == x2:
#             # Menambahkan huruf pertama hasil enkripsi
#             ciphertext += mat[x1][(y1 - 1) % 5]
#             # Menambahkan huruf kedua hasil enkripsi
#             ciphertext += mat[x2][(y2 - 1) % 5]
#         # Jika berada pada kolom yang sama, geser ke bawah
#         elif y1 == y2:
#             ciphertext += mat[(x1 - 1) % 5][y1]
#             ciphertext += mat[(x2 - 1) % 5][y2]
#         # Jika berada pada baris dan kolom yang berbeda
#         else:
#             ciphertext += mat[x2][y1]
#             ciphertext += mat[x1][y2]

#         i += 2

#     return ciphertext

def encrypt(message, mat):
    ciphertext = ''  # Variabel untuk menyimpan hasil dari enkripsi
    i = 0

    while i < len(message):
        # Karakter saat ini
        char1 = message[i]
        # Karakter berikutnya (jika ada)
        char2 = message[i+1] if i+1 < len(message) else None

        # Cek jika karakter adalah huruf alfabet (A-Z atau a-z)
        if char1.isalpha():
            # Mengambil posisi huruf dalam matriks
            pos1 = get_position(mat, char1)
            x1, y1 = pos1  # Baris dan kolom huruf pertama

            # Jika karakter berikutnya adalah huruf alfabet juga
            if char2 and char2.isalpha():
                pos2 = get_position(mat, char2)
                x2, y2 = pos2  # Baris dan kolom huruf kedua

                # Jika berada pada baris yang sama, geser ke kanan
                if x1 == x2:
                    # Menambahkan huruf pertama hasil enkripsi
                    ciphertext += mat[x1][(y1 - 1) % 5]
                    # Menambahkan huruf kedua hasil enkripsi
                    ciphertext += mat[x2][(y2 - 1) % 5]
                # Jika berada pada kolom yang sama, geser ke bawah
                elif y1 == y2:
                    ciphertext += mat[(x1 - 1) % 5][y1]
                    ciphertext += mat[(x2 - 1) % 5][y2]
                # Jika berada pada baris dan kolom yang berbeda
                else:
                    ciphertext += mat[x2][y1]
                    ciphertext += mat[x1][y2]

                i += 2  # Lewati 2 karakter
            else:
                # Jika hanya ada satu karakter, enkripsi karakter tersebut
                # dan lanjutkan ke karakter berikutnya
                ciphertext += mat[x1][(y1 - 1) % 5]
                i += 1
        else:
            # Jika karakter bukan huruf alfabet, tambahkan ke ciphertext tanpa perubahan
            ciphertext += char1
            i += 1

    return ciphertext


# === Fungsi untuk mendekripsi ===
def decrypt(ciphertext, mat):
    plaintext = ''
    i = 0

    while i < len(ciphertext):
        char1 = ciphertext[i]
        char2 = ciphertext[i+1]

        pos1 = get_position(mat, char1)
        pos2 = get_position(mat, char2)

        x1, y1 = pos1
        x2, y2 = pos2

        if x1 == x2:
            plaintext += mat[x1][(y1 + 1) % 5]
            plaintext += mat[x2][(y2 + 1) % 5]
        elif y1 == y2:
            plaintext += mat[(x1 + 1) % 5][y1]
            plaintext += mat[(x2 + 1) % 5][y2]
        else:
            plaintext += mat[x2][y1]
            plaintext += mat[x1][y2]

        i += 2

    return plaintext

# Output Matriks


def matrix(mat):
    print("\nMatriks:")
    for row in mat:
        print(' '.join(row))


msg = 'Pada jaman dahulu kala, di lembah gunung Telomayo hiduplah sepasang suami istri yang bernama Ki Hajar dan Nyai Selakanta. Mereka hidup sederhana dan belum dikarunia keturunan. Ki Hajar akhirnya memutuskan untuk pergi bertapa di Gunung Telomoyo untuk memohon kepada Yang Maha Kuasa agar dikarunia seorang anak. Setelah beberapa lama Ki Hajar bertapa di gunung, sang istri kemudian hamil. Perut Nyai Selakanta pun semakin hari semakin membesar hingga akhirnya melahirkan seorang anak. Namun betapa terkejutnya Nyai Selakanta, ternyata yang dilahirkan olehnya bukanlah bayi manusia melainkan seekor Naga. Ajaibnya naga tersebut dapat berbicara dan Nyai Selakanta pun menamainya Baru Klinting. Hari demi hari Naga Baru Klinting semakin besar. Hingga pada suatu hari dia bertanya kepada ibunya, ”Ibu di manakah keberadaan ayahku”?. Nyai Selakanta pun memberitahukan bahwa ayahnya sedang bertapa di lereng Gunung Telomoyo. Naga Baru Kiinting pun pergi kesana dan bertemu seorang pria tua yang merupakan ayahnya. Ki Hajar tidak percaya begitu saja dengan Naga Baru Klinting, “jika kamu memang anakku, coba lingkari gunung ini dengan tubuhmu”. Naga Baru Klinting melaksanakan dan berhasil. Ki Hajar akhimya percaya, setelah melihat klintingan (lonceng kecil) yang dikalungkan Nyai Selakanta di leher Baru Klinting. Dan supaya dirinya berubah menjadi manusia, ia harus bertapa di Bukit Tugur. Naga Baru Khlintingpun dengan senang hati melaksanakan perintah ayahnya tersebut. Pada saat itu, penduduk desa yang berada di bawah Bukit Tugur sedang berburu binatang buruan di hutan. Tiba-tiba mereka melihat Naga Baru Klinting yang diam di dalam Gua. Oleh karena mereka tidak satupun mendapatkan binatang, akhirnya para penduduk itu memotong tubuh Naga Baru Klinting untuk di jadikan makanan. Kemudian para penduduk desa itu pulang dan mengadakan pesta besarbesaran karena telah mendapatkan daging yang banyak. Ketika mereka sedang menikmati makanan pesta, datanglah seorang anak kecil yang kumel dan bau. Anak itu mendekat dan berharap untuk diberikan makanan. Namun penduduk desa menolaknya, ”Pergilah kau dasar pengemis!, tubuhmu kotor dan bau!”. Melihat kejadian itu seorang nenek tua yang bemama Nyai Latung merasa kasihan. ”Nak ikutlah ke rumah nenek!” kata nenek itu. Anak itu lalu mengikuti ke rumahnya. Disana ia diberi makanan yang banyak. hingga menghabiskan semua makanan yang dihidangkan. “Terimakasih, Nenek sangat baik tidak seperti penduduk desa itu!” kata anak itu. Sebelum pergi anak itu berpesan bahwa jika nanti mendengar suara gemuruh, carilah sebuah lesung dan naiklah diatasnya.Kemudian anak tersebut kembali ke pesta yang meriah itu. Ia kembali meminta makanan kepada warga desa. ”Pak kasihanilah saya pak?, berilah makanan sedikit saja”. Akan tetapi, penduduk desa itu makin menjadi marah, “kamu lagi, sana pergi jauh. kamu sudah mengganggu pesta disini”, kata seorang warga desa sambil menendang anak itu hingga tersungkur. Anak itu kemudian bangkit dan mengeluarkan sebuah lidi lalu ditancapkannya di tanah, Wahai kalian penduduk desa, jika kalian bisa mencabut lidi ini, Aku akan pergi dan tidak mengganggu kalian lagi”, pinta anakitu.Satu persatu warga desa mencoba mencabut lidi itu. Tetapi anehnya tidak ada seorangpun dapat mencabutnya. “Payah kalian, hanya mencabut lidi sekecil itu saja tidak mampu,“ ejek anak itu Akhirnya anak itu mencabut lidi yang tertancap di tanah. Tiba-tiba lubang tanah bekas tancapan lidi tersebut mengeluarkan air yang semakin lama semakin deras. Air tersebut berubah menjadi banjir yang besar hingga menenggelamkan seluruh desa yang angkuh tersebut. Tak seorangpun dapat selamat kecuali nenek tua yang menaiki Iesungnya. Tak lama setelah itu, Ki Hajsar mendatangi anak kecil tersebut dan mengajaknya pergi menemui Nyai Selakanta. Ternyata anak kecil itu adalah penjelmaan dari Naga Baru Klinting yang tubuhnya telah dimakan penduduk desa. Hingga saat ini rendaman air itu masih ada dan menjadi telaga yang dikenal dengan Telaga Rawa Pening.'

plaintext = msg.replace(' ', '').lower()

key = "taliya"
mat = generate_matrix(key)
matrix(mat)
formatted_msg = format_message(plaintext)
ciphertext = encrypt(formatted_msg, mat)
print("Formatted Text:\n", formatted_msg, "\n[", ' '.join(
    formatted_msg[i:i+2] for i in range(0, len(formatted_msg), 2)), "]")
print("\n")
print("Encrypted Text:\n", ciphertext, "[", ' '.join(
    ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)), "]")

# print(ciphertext)
