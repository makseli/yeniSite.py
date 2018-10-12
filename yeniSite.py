import os,commands;
os.getcwd()

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

if commands.getoutput("whoami") != "root":
	print(bcolors.FAIL+" \n LUTFEN yeniSite.py dosyasini SUDO izni ile calistirdiginiza emin olunuz  \n"+bcolors.ENDC)
	exit();


phpv = commands.getoutput("php -r \@phpinfo\(\)\; | grep 'PHP Version' -m 1")

phpv = phpv.replace("PHP Version => ", "")

PHPV = "php5"

if phpv[0] == "7":
	PHPV = "php/php7."+phpv[2]
	print("PHP 7 kullaniyorsunuz")

print PHPV

Encin = raw_input("\n ** hangisini kullaniyorsunuz ? apache2 veya nginx giriniz ( ontanimli nginx ) : ")
if Encin != "apache2": Encin = "nginx"
print(bcolors.OKGREEN+" \n Kullandiginiz Encin \"" + Encin + "\" olarak atandi !\n"+bcolors.ENDC)

ServerName = raw_input("\n ** ServerName giriniz: ")
print(bcolors.OKGREEN+" \n ServerName \"" + ServerName + "\" olarak atandi !\n"+bcolors.ENDC)

DocumentRoot = raw_input(" ** DocumentRoot giriniz (ontanimli /var/www/" + ServerName + ") : ")
if DocumentRoot == "": DocumentRoot = "/var/www/" + ServerName
print(bcolors.OKGREEN+"DocumentRoot \"" + DocumentRoot + "\" olarak atandi !\n"+ bcolors.ENDC)

ServerAdmin =  raw_input(" ServerAdmin E-Posta giriniz (ontanimli= bilgi@" + ServerName + ") : ")
if ServerAdmin == "": ServerAdmin = "bilgi@" + ServerName
print(bcolors.OKGREEN+" \n ServerAdmin \"" + ServerAdmin + "\" olarak atandi !\n "+ bcolors.ENDC)

ErrorLog = raw_input(" ** ErrorLog giriniz (ontanimli= /var/log/"+ServerName+".err): ")
if ErrorLog == "": ErrorLog = "/var/log/"+ServerName+".err"
print(bcolors.OKGREEN+"ErrorLog \"" + ErrorLog + "\" olarak atandi !\n"+ bcolors.ENDC)

CustomLog = raw_input(" ** CustomLog giriniz (ontanimli= /var/log/"+ServerName+".clg): ")
if CustomLog == "": CustomLog = "/var/log/"+ServerName+".clg"
print(bcolors.OKGREEN+"CustomLog \"" + CustomLog + "\" olarak atandi !\n"+ bcolors.ENDC)

if Encin != "nginx":
	metin = """<VirtualHost *:80>
			ServerAdmin \""""+ServerAdmin+"""\"
			DocumentRoot \""""+DocumentRoot+"""\"
			ServerName \""""+ServerName+"""\"
			ErrorLog \""""+ErrorLog+"""\"
			CustomLog \""""+CustomLog+"""\" common
	</VirtualHost>"""
	dosyaYolu = "/etc/apache2/sites-available/"

else:
	metin = """server {
  server_name """+ServerName+""";
  listen 80;
  root """+DocumentRoot+""";
  
  index index.php;
  location / {
    try_files $uri $uri/ @rewrites;
  }
  location @rewrites {
    rewrite ^ /index.php last;
  }
  location ~ \.php {
    fastcgi_index index.php;
    fastcgi_split_path_info ^(.+\.php)(.*)$;
    include /etc/nginx/fastcgi_params;
    fastcgi_pass unix:/var/run/"""+PHPV+"""-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
  } 
  }"""
	dosyaYolu = "/etc/nginx/sites-available/"
	
	

VHostDosya = open(dosyaYolu+ServerName+".conf", "w")
VHostDosya.write(metin)
VHostDosya.close()

print(bcolors.WARNING+"yeni \"" + dosyaYolu + ServerName +".conf"+ "\" dosya olusturuldu !\n"+bcolors.ENDC)

LokalHostDosya = open("/etc/hosts", "a")
LokalHostDosya.write("\n" +"127.0.0.1         " + ServerName)
LokalHostDosya.close()

if Encin != "nginx":
	os.system("sudo ln -s "+dosyaYolu+ServerName+".conf /etc/apache2/sites-enabled/"+ServerName+".conf")
	os.system("sudo service apache2 restart")
else:
	os.system("sudo ln -s "+dosyaYolu+ServerName+".conf /etc/nginx/sites-enabled/"+ServerName+".conf")
	os.system("sudo service nginx restart")

exit();
