import os

#Membaca file
nama_file = input("Masukkan nama file: ")
if os.name=='nt':
    file_path = os.path.join("..\\test", nama_file)
else:
    file_path = os.path.join("test", nama_file)
f = open(file_path, "r")

A=f.read().split('\n')

#Menyimpan list matkul unik pada matkul []
#Menyimpan dalam bentuk DA Graph pada edges []
matkul = []
edges = []
for line in range(len(A)):
    j=0
    #menghitung berapa koma yang telah dilewati
    #bila 0 maka menjadi simpul tujuan dari <matkul> pada baris tersebut)
    koma = 0
    #menyimpan kode matkul
    temp=""
    #mengecek apakah masih ada <matkul_x> pada line
    ada = True
    while(ada):
        #Bila ditemui tanda koma, maka akan melompat 2 karakter
        #Karena format pada .txt <matkul_1>, <matkul_2>, .....
        if (A[line][j] == ','):
            if temp not in matkul:
                matkul.append(temp)
            if (koma == 0):
                dest = temp
            else:
                edges.append((temp,dest))
            temp = ""
            j+=2
            koma+=1
        #Bila ditemui tanda titik akan dilanjutkan ke baris berikutnya
        elif (A[line][j] == '.'):
            if temp not in matkul:
                matkul.append(temp)
            #prevent bila dalam 1 baris hanya ada 1 mata kuliah
            if (koma != 0):
                edges.append((temp,dest))
            ada = False
        else:
            temp+=(A[line][j])
            j+=1

#Membuat indegreelist berdasarkan urutan mata kuliah di list matkul[]
indegreelist = [0 for i in range (len(matkul))]
for i in range (len(matkul)):
    for (src,dest) in edges:
        if (matkul[i] == dest):
            indegreelist[i]+=1

semester = 1
#sisaMatkul diperlukan untuk matkul sisa yang belum diambil (saat edges sudah kosong)
sisaMatkul = matkul.copy()
#dituliskan maksimum 8 semester asumsinya
while (edges != [] and semester<8):
    print("Semester", semester, ':')
    #tempIndegree diperlukan agar saat penghapusan edge tidak langsung ter-update
    #dapat membuat course dan pre req course diambil bersamaan
    tempIndegree = indegreelist.copy()
    for counter, i in enumerate(indegreelist):
        if (i == 0) :
            #penanda agar tidak terbaca 2 kali (diberi -999)
            tempIndegree[counter] -= 999
            #Menampilkan matkul yang diambil
            print(matkul[counter], end=' ')
            #Hapus matkul yang telah diambil
            sisaMatkul.remove(matkul[counter])
            for (src,dest) in edges:
                if (src == matkul[counter]):
                    #Hapus edge dari list
                    indexEdges = 0
                    for (src,dest) in edges:
                        if (src == matkul[counter]):
                            #Kurangi indegree dest yang akan di-pop
                            for j in range (len(matkul)):
                                if(dest == matkul[j]):
                                    tempIndegree[j] -= 1
                            #Decrease list edges
                            edges.pop(indexEdges)
                        indexEdges += 1
    print("")
    semester+=1
    #update indegreelist
    indegreelist = tempIndegree
#menampilkan sisa matkul yang butuh diambil pada semester terakhir
print("Semester", semester, ':')
for i in sisaMatkul:
    print(i, end=' ')

print("")
