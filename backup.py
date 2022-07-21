import paramiko
import time
from ftplib import FTP

#Cartel

print("---------------Bienvenido al best programa de backups ever---------------")

#variables de authenticacion

try: 
    print("Ingresar el ip: ")
    ip = input(">>:")
    print("Ingresar el puerto ssh")
    puerto = int(input(">>:"))
    print("Ingresar el usuario ssh")
    user = input(">>:")
    print("Ingresar el password ssh")
    passw = input(">>:")
except TypeError:
    print("ojo, se puso mal algun valor")


#Se abre la sesion con la variable "ssh_open"

ssh_open = paramiko.SSHClient()          # Representacion de una High-level session. 
ssh_open.load_system_host_keys()
ssh_open.set_missing_host_key_policy(paramiko.AutoAddPolicy())  

ssh_open.connect(ip, puerto, user, passw)        

#FUNCION DONDE EMPIEZAN LOS COMANDOS QUE SE TIRAN SOBRE EL EQUIPO

commands = ssh_open.invoke_shell() # Tira un request de una shell.
commands.send("N\n")
time.sleep(.5)
commands.send("sys\n")
time.sleep(.5)   
commands.send("display current-configuration >> backup.txt\n")   
time.sleep(.5) #5 milisegundos de espera para seguir con el desarrollo del codigo. 
output = commands.recv(65535) #buffersize
output = output.decode("utf-8")

#empieza el translado del archivo a la pc host.
ftp = FTP("192.168.0.3") #se conecta al servidor ftp
ftp.login(user=user, passwd=passw) # authenticacion
with open("backup.txt", "wb")as fp: #en este caso se busca el archivo en el directorio 
    ftp.retrbinary("REtr backup.txt", fp.write) #se descarga el archivo
ftp.quit()# se cierra la sesion del ftp
print("Adiosss")
