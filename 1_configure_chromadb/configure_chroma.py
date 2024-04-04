import subprocess

print(subprocess.run(["sh 1_configure_chromadb/configure_chroma.sh"], shell=True))
