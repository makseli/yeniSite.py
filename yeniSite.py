ServerName = raw_input("\n ** ServerName giriniz: ")
print(" \n ServerName \"" + ServerName + "\" olarak atandi !\n")

DocumentRoot = raw_input(" ** DocumentRoot giriniz (ontanimli /var/www/" + ServerName + ") : ")
if DocumentRoot == "": DocumentRoot = "/var/www/" + ServerName
print("DocumentRoot \"" + DocumentRoot + "\" olarak atandi !\n")

ServerAdmin =  raw_input(" ServerAdmin E-Posta giriniz (ontanimli= bilgi@" + ServerName + ") : ")
if ServerAdmin == "": ServerAdmin = "bilgi@" + ServerName
print(" \n ServerAdmin \"" + ServerAdmin + "\" olarak atandi !\n ")

ErrorLog = raw_input(" ** ErrorLog giriniz (ontanimli= /var/log/"+ServerName+"): ")
if ErrorLog == "": ErrorLog = "/var/log/"+ServerName
print("ErrorLog \"" + ErrorLog + "\" olarak atandi !\n")

CustomLog = raw_input(" ** CustomLog giriniz (ontanimli= /var/log/CA_"+ServerName+"): ")
if CustomLog == "": CustomLog = "/var/log/CA_"+ServerName+""
print("CustomLog \"" + CustomLog + "\" olarak atandi !\n")

metin = """<VirtualHost *:80>
        ServerAdmin \""""+ServerAdmin+"""\"
        DocumentRoot \""""+DocumentRoot+"""\"
        ServerName \""""+ServerName+"""\"
        ErrorLog \""""+ErrorLog+"""\"
        CustomLog \""""+CustomLog+"""\" common
</VirtualHost>"""

import os;
os.getcwd()
dosyaAdi = "/etc/apache2/sites-enabled/"+ServerName+""
VHostDosya = open(dosyaAdi, "w")
VHostDosya.write(metin)
VHostDosya.close()
print("yeni \"" + dosyaAdi + "\" dosya olusturuldu !\n")

LokalHostDosya = open("/etc/hosts", "a")
LokalHostDosya.write("127.0.0.1		" + ServerName)
LokalHostDosya.close()

os.system("sudo /etc/init.d/apache2 restart")

exit();
