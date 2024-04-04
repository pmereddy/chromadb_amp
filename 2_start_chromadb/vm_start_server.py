import subprocess
import os
import bcrypt

if os.environ.get('CHROMA_AUTH', 'false').lower() == 'true':
    user = os.environ.get('CHROMA_USER', 'admin')
    password = os.environ.get('CHROMA_PASSWORD', 'admin')
    #cmd = ["/usr/sbin/htpasswd", "-Bbc", "server.htpasswd", f"{user}", f"{password}"]
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open("server.htpasswd", "w") as file:
        file.write(f"{user}:{hashed_password.decode()}\n")
    
    os.environ['CHROMA_SERVER_AUTH_CREDENTIALS_FILE'] = 'server.htpasswd'
    os.environ['CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER'] = 'chromadb.auth.providers.HtpasswdFileServerAuthCredentialsProvider'
    os.environ['CHROMA_SERVER_AUTH_PROVIDER'] = 'chromadb.auth.basic.BasicAuthServerProvider'

print(subprocess.run(["chroma run --path $HOME/chroma-data --port " + str(os.environ.get('CDSW_APP_PORT', 8000))], shell=True))
