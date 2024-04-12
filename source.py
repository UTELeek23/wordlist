import time
import multiprocessing
from itertools import product, chain

def wordlist_with_number_phone(lock):
    print("Start generating wordlist with number phone...")
    preflix = ['039','038','037','036','035','034',
              '033','032','096','097','098','086',
              '083','084','085','081','088','082',
              '070','079','077','076','078',
              ]
    with open("suffix.txt", "r") as f:
        suffix = f.read().split("\n")
    
    with open("Secui.txt", "a") as f: 
        for prefix, suf in product(preflix, suffix):
            number = prefix + suf
            lock.acquire()
            f.write(number + "\n")  # Ghi từng số điện thoại vào file
            lock.release()
    

def wordlist_with_name(lock):
    first_names = ['nguyen','le','bui','pham','tran','vu','dang','do','ho','bui','ngo','huynh','ly','luong','mai','cao','truong']
    last_names =['an', 'bao', 'binh', 'dat', 'duc', 'dung', 'duy', 'gia', 'huy', 'khanh', 'khoa', 'kiet', 'lam', 'linh',
                  'loc', 'long', 'minh', 'ngoc', 'nhan', 'phong', 'phu', 'phuc', 'quang', 'quoc', 'sang', 'son', 'thang']
    middle_names = ['thi','van']
    print("Start generating wordlist with name...")
    with open("Secui.txt", "a") as f:  
        for first, middle, last in chain(product(first_names, middle_names, last_names), product(first_names, last_names, last_names)):
            full_name = first + middle + last
            lock.acquire()
            f.write(full_name + "\n")  # Ghi từng tên vào file
            lock.release()

def common_wordlist(lock):
    print("Start generating common wordlist...")
    s=""
    f=open("Secui.txt", "a")
    #1->9
    for i in range(1,10):
        s+=str(i)
        if(len(s)>=8):
            lock.acquire()
            f.write(s+'\n')
            lock.release()
    s=""
    for i in range(9,-1,-1):
        s+=str(i)
        if(len(s)>=8):
            lock.acquire()
            f.write(s+'\n')
            lock.release()
    #0->9
    s=""
    for i in range(0,10):
        s+=str(i)
        if(len(s)>=8):
            lock.acquire()
            f.write(s+'\n')
            lock.release()
    lock.acquire()
    f.write('12345678910'+'\n')
    lock.release()
    #abababab+aaaaaaaa
    s=""
    for i in range(0,10):
        for j in range(0,10):
            s1=str(i)
            s2=str(j)
            s=""
            for ki in range(4):
                s+=s1+s2
            lock.acquire()
            f.write(s+'\n')
            lock.release()
    #'a'*10
    for i in range(ord('a'),ord('z')+1):
        f.write(chr(i)*10+'\n')
    for i in range(0,9):
        f.write(str(i)*10+'\n')
    #'abc'*3
    for i in range(0,10):
        for j in range(0,10):
            for k in range(0,10):
                s=str(i)+str(j)+str(k)
                s=s*3
                if(i!=j and j!=k):
                    lock.acquire()
                    f.write(s+'\n')
                    lock.release()
    f.close()

def main():
    # wordlist_number_phone = multiprocessing.Manager().list()
    # wordlist_names = multiprocessing.Manager().list()
    pass

if __name__ == "__main__":
    start = time.time()
    lock = multiprocessing.Lock()
    p1 = multiprocessing.Process(target=wordlist_with_number_phone, args=(lock,))
    p2 = multiprocessing.Process(target=wordlist_with_name, args=(lock,))
    p3 = multiprocessing.Process(target=common_wordlist, args=(lock,))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    print("Main done")
    print("Time to generate wordlist: ", time.time() - start)
