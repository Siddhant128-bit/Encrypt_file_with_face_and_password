import tkinter as tk
from tkinter import *
from PIL import ImageTk,Image
import pyAesCrypt
import os
import shutil
from stat import *
from os import stat, remove
import sys
import cv2
import face_recognition
import datetime
import numpy

root=tk.Tk()
root.geometry('520x520')
root.title('Face Locker')
root.iconbitmap('UI_Data\logo.ico')
frame0=LabelFrame(root)
frame0.configure(bg='black')
frame0.configure(highlightbackground='black')

bufferSize = 64 * 1024

universal_image_name=''
def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1





def encrypt():
    key=3
    frame1=LabelFrame(root,padx=5,pady=5)
    frame1.configure(bg='Black')
    frame1.pack()
    file_name=''
    passworld=''
    def main_menu1():
        frame1.destroy()
        main()


    def save_image(image_name):
        cap = cv2.VideoCapture(0)
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            cv2.imshow('frame',frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        image_name='Data/'+image_name
        cv2.imwrite(image_name+'.jpg',frame)
        cap.release()
        cv2.destroyAllWindows()
        image_name=image_name+'.jpg'
        image=face_recognition.load_image_file(image_name)
        image_encoding=face_recognition.face_encodings(image)
        image_name1=os.path.basename(image_name)
        n1=len(image_name1)
        encoding_name=''
        for i in range(n1-4):
            encoding_name=encoding_name+image_name1[i]
        encoding_name='Data/'+encoding_name
        numpy.savetxt(encoding_name+'.txt',(image_encoding))
        shutil.copy2(image_name,'UI_Data/Backup/')
        shutil.copy2(encoding_name+'.txt','UI_Data/Backup/')
        #with open(encoding_name+'.txt','w+')as f:
            #f.writelines(image_encoding)


    def get():
        file_name=Entrye1.get()
        password=Entrye2.get()
        image_name=Entrye3.get()
        print(file_name)
        print(password)
        print(image_name)
        t_file_name1=os.path.basename(file_name)
        t_file_name=''
        n1=len(t_file_name1)
        for i in range(n1-4):
                t_file_name=t_file_name+t_file_name1[i]

        print(t_file_name1)
        print(t_file_name)
        save_image(image_name)
        # encrypt
        with open(file_name, "rb") as fIn:
            with open(file_name+".aes", "wb") as fOut:
                pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)

        os.chmod(file_name, S_IWRITE )
        shutil.copy2(file_name+'.aes','Data/')
        os.remove(file_name)

        # get encrypted file size
        encFileSize = stat(file_name+".aes").st_size
        encFileSize=str(encFileSize)
        #print(encFileSize)
        passcodes=''
        #print(t_file_name)
        with open('Data/'+t_file_name+'.txt','w+')as f:
            f.writelines(file_name)
            f.writelines('*')
            f.writelines(password)
            f.writelines('#')
            f.writelines(encFileSize)

        with open('Data/'+t_file_name+'.txt','r+')as f:
            passcodes=f.readlines()
        #print(passcodes)
        temp_encrypt=""
        for i in passcodes[0]:
            ow=ord(i)
            nw=ow+key
            i=chr(nw)
            temp_encrypt=temp_encrypt+i
        print(temp_encrypt)
        temp_encrypt=listToString(temp_encrypt)
        with open('Data/'+t_file_name+'.txt','w+')as f:
            f.writelines(temp_encrypt)
        shutil.copy2('Data/'+t_file_name1+'.aes','UI_Data/Backup/')
        shutil.copy2('Data/'+t_file_name+'.txt','UI_Data/Backup/')
        main_menu1()



    label1=Label(frame1,text='Welcome to Encryption',bg='Black',fg='Blue')
    label1.pack()
    label2=Label(frame1,text='Enter File Name(With Directory): ',bg='Black',fg='Blue')
    label2.pack()
    Entrye1=Entry(frame1,width=100,bg='Black',fg='Blue')
    Entrye1.pack()
    label3=Label(frame1,text='Enter Password: ',bg='Black',fg='Blue')
    label3.pack()
    Entrye2=Entry(frame1,width=100,bg='Black',fg='Blue')
    Entrye2.pack()
    label4=Label(frame1,text='Enter Photo Name: ',bg='Black',fg='Blue')
    label4.pack()
    Entrye3=Entry(frame1,width=100,bg='Black',fg='Blue')
    Entrye3.pack()
    buttone1=Button(frame1,text='Continue',fg='green',command=get,bg='black')
    buttone1.pack()
    button=Button(frame1,text='Back',fg='Red',bg='Black',command=main_menu1)
    button.pack()

    #file_name=input('Enter file name: ')
    #password=input('Enter the password: ')


def decrypt():
    key=3
    f=0

    frame1=LabelFrame(root,padx=5,pady=5)
    frame1.configure(bg='Black')
    frame1.pack()
    file_name=''
    passworld=''
    def main_menu1():
        frame1.destroy()
        main()

    def load_image(image_name):
        f=0
        f1=0
        x=1
        image_name='Data/'+image_name
        image=face_recognition.load_image_file(image_name+'.jpg')
        image_name1=os.path.basename(image_name)
        encoding=face_recognition.face_encodings(image)
        encoding1=numpy.loadtxt(image_name+'.txt')
        numpy.sum(encoding)
        print(encoding)
        cap = cv2.VideoCapture(0)
        print('Face Identification')
        x=datetime.datetime.now()
        t_sec=x.second
        target=t_sec+10
        while(x!=0):
            x=datetime.datetime.now()
            t_sec=x.second
            ret, frame = cap.read()
            cv2.imwrite('test.jpg',frame)
            image=face_recognition.load_image_file(f"{'test.jpg'}")
            unknown_encoding=face_recognition.face_encodings(image)
            count=0
            if t_sec==target:
                print('Valid Face not Detected')
                x=0

            for c in unknown_encoding:
                results = face_recognition.compare_faces(encoding, c)
                print(results)
                if True in results:
                    f=1
                    print('Valid Face Detected')
                    x=0
                    break

        os.remove('test.jpg')
        comparison= numpy.array([])
        comparision=encoding==encoding1
        equal_arrays = comparison.all()
        print(equal_arrays)
        if f==1 and equal_arrays==True:
            print('Valid Face Provided and accepted')
            os.remove(image_name+'.jpg')
            os.remove(image_name+'.txt')
            f1=1

        elif f==1 and equal_arrays==False:
            print('Valid Face but Photo Altered')
            f1=0


        return(f1)


    def get():
        file_name=Entrye1.get()
        typed_password=Entrye2.get()
        image_name=Entrye3.get()
        image_name2=os.path.basename(image_name)
        t_file_name1=os.path.basename(file_name)
        print(t_file_name1)
        t_file_name=''
        password=''
        encFileSize=''
        n1=len(t_file_name1)
        for i in range(n1-8):
            print(t_file_name1[i])
            t_file_name=t_file_name+t_file_name1[i]

        print(t_file_name)

        with open('Data/'+t_file_name+'.txt','r+')as f:
            passcodes=f.readlines()

        temp_encrypt=''
        for i in passcodes[0]:
            ow=ord(i)
            nw=ow-key
            i=chr(nw)
            temp_encrypt=temp_encrypt+i
        temp_encrypt=listToString(temp_encrypt)
        print('To be stored: '+temp_encrypt)
        #with open('Data/'+t_file_name+'.txt','w+')as f:
            #f.writelines(temp_encrypt)

        #with open('Data/'+t_file_name+'.txt','r+')as f:
            #file_Data=f.readlines()
        file_Data.append(temp_encrypt)
        print(file_Data)

        n_file_name=t_file_name+'.txt'
        n_file_name='Data/'+n_file_name
        file_name=''
        count=0
        count_p=0
        n=len(file_Data[0])
        #print(n)
        for i in file_Data[0]:
            if i!='*':
                file_name=file_name+i
                count=count+1
            elif i=='*':
                break

        count=count+1
        count_p=count
        for i in range(count,n):
            if file_Data[0][i]!='#':
                password=password+file_Data[0][i]
                count_p=count_p+1
            elif file_Data[0][i]=='#':
                break
        count_p=count_p+1
        for i in range(count_p,n):
            encFileSize=encFileSize+str(file_Data[0][i])
            #print(encFileSize)

        print(encFileSize)
        encFileSize=int(encFileSize)
        f=load_image(image_name)
        print(f)
        if typed_password!=password or f==0:
            print('Access Denied')
            main_menu1()

        elif typed_password==password and f==1:
            print('Access Granted')
            with open(file_name+".aes", "rb") as fIn:
                try:
                    with open(file_name, "wb") as fOut:
                    # decrypt file stream
                        pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
                except ValueError:
                    # remove output file on error
                    remove(file_name)

            os.remove(file_name+".aes")
            os.remove('Data/'+t_file_name1)
            os.remove(n_file_name)
            os.remove('UI_Data/Backup/'+t_file_name+'.txt')
            os.remove('UI_Data/Backup/'+t_file_name1)
            os.remove('UI_Data/Backup/'+image_name2+'.jpg')
            os.remove('UI_Data/Backup/'+image_name2+'.txt')
            main_menu1()
        else:
            print('Invalid Action')
            main_menu1()


    label1=Label(frame1,text='Welcome to Decryption',bg='Black',fg='Blue')
    label1.pack()
    label2=Label(frame1,text='Enter File Name(With Directory): ',bg='Black',fg='Blue')
    label2.pack()
    Entrye1=Entry(frame1,width=100,bg='Black',fg='Blue')
    Entrye1.pack()
    label3=Label(frame1,text='Enter Password: ',bg='Black',fg='Blue')
    label3.pack()
    Entrye2=Entry(frame1,width=100,bg='Black',fg='Blue')
    Entrye2.pack()
    label4=Label(frame1,text='Enter Photo Name: ',bg='Black',fg='Blue')
    label4.pack()
    Entrye3=Entry(frame1,width=100,bg='Black',fg='Blue')
    Entrye3.pack()
    buttone1=Button(frame1,text='Continue',fg='green',command=get,bg='black')
    buttone1.pack()
    button=Button(frame1,text='Back',fg='Red',bg='Black',command=main_menu1)
    button.pack()


    file_Data=[]
    #print('Welcome to Decrption')
    #file_name=input('Enter Encrypted file name: ')
    #typed_password=input('Enter password: ')






def main():

    frame=LabelFrame(root)
    frame.pack(padx=20,pady=20)
    frame.configure(bg='black')
    def encrypt_menu():
        frame.destroy()
        encrypt()

    def decrypt_menu():
        frame.destroy()
        decrypt()

    Button0=Button(frame,text='Encrypt',command=encrypt_menu,bg='Black',fg='Blue')
    Button0.pack()
    label01=Label(frame,text='',bg='black')
    label01.pack()
    Button1=Button(frame,text='Decrypt',command=decrypt_menu,bg='black',fg='Blue')
    Button1.pack()
    label02=Label(frame,text='',bg='black')
    label02.pack()
    Button2=Button(frame,text='Quit',fg='red',command=root.quit,bg='Black')
    Button2.pack()

def check():
    m_password=Entrye1.get()
    if m_password=='Siddhant' or m_password=='siddhant' or m_password=='Sristi' or m_password=='sristi' or  m_password=='FaceLocker'or  m_password=='facelocker'or  m_password=='Face Locker'or  m_password=='face locker':
        frame0.destroy()
        main()

def info():
    os.system('info.txt')


img=ImageTk.PhotoImage(Image.open('UI_Data\Face_logo.jpg'))
img_Label=Label(image=img,bg='Black')
img_Label.pack()
img1=ImageTk.PhotoImage(Image.open('UI_Data/name_tag.png'))
img_Label1=Label(image=img1,bg='Black')
img_Label1.pack()
frame0.pack()
label0=Label(frame0,text='Enter PassCode to Access the System : ',bg='black',fg='Blue')
label0.pack()
Entrye1=Entry(frame0,width=100,bg='black',fg='Blue')
Entrye1.pack()

buttonp=Button(frame0,text='Start',command=check,bg='Black',fg='Blue')
buttonp.pack()

buttonp0=Button(frame0,text='Some Info',command=info,bg='Black',fg='Blue')
buttonp0.pack()

buttonp1=Button(frame0,text='Quit',command=root.quit,bg='Black',fg='Red')
buttonp1.pack()

label1=Label(root,text='System by Siddhant Sharma',bg='black',fg='Blue')
label1.pack()
root.configure(bg='black')
root.mainloop()
