import subprocess
import os

if os.environ.get('CHROMA_AUTH', 'false').lower() == 'true':
    user = os.environ.get('CHROMA_USER', 'admin')
    password = os.environ.get('CHROMA_PASSWORD', 'admin')
    #cmd=f"/usr/sbin/htpasswd -Bbn {user} {password} > server.htpasswd"
    #cmd = ["/usr/sbin/htpasswd", "-Bbn", f"{user}", f"{password}", ">", "server.htpasswd"]
    cmd = ["/usr/sbin/htpasswd", "-Bbc", "server.htpasswd", f"{user}", f"{password}"]

    result=subprocess.run(cmd, capture_output=True, shell=False)

    os.environ['CHROMA_SERVER_AUTH_CREDENTIALS_FILE'] = 'server.htpasswd'
    os.environ['CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER'] = 'chromadb.auth.providers.HtpasswdFileServerAuthCredentialsProvider'
    os.environ['CHROMA_SERVER_AUTH_PROVIDER'] = 'chromadb.auth.basic.BasicAuthServerProvider'

print(subprocess.run(["chroma run --path $HOME/chroma-data --port " + str(os.environ.get('CDSW_APP_PORT', 8000))], shell=True))
