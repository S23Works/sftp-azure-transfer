import os
import paramiko
from azure.storage.blob import BlobServiceClient

# Configuración SFTP
SFTP_HOST = "localhost"
SFTP_PORT = 22
SFTP_USER = "testuser"
SFTP_PASSWORD = "testpass"
SFTP_FOLDER = "Done"

# Configuración Azure
AZURE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=https;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IF"
    "suFq2UVErCz4I6tiqIvPcneZCMpLkKqxZfDpP5YQ==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)
AZURE_CONTAINER = "pdfs-container"

# Carpeta local temporal
LOCAL_DIR = "C:/temp_pdfs"
os.makedirs(LOCAL_DIR, exist_ok=True)


def process_sftp_files():
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)

    sftp = paramiko.SFTPClient.from_transport(transport)

    # Listar archivos del SFTP
    files = sftp.listdir_attr(SFTP_FOLDER)

    # Filtrar PDFs y tomar solo 5
    pdf_files = [f for f in files if f.filename.lower().endswith(".pdf")]
    pdf_files = sorted(pdf_files, key=lambda x: x.st_mtime)[:5]

    blob_service_client = BlobServiceClient.from_connection_string(
        AZURE_CONNECTION_STRING
    )

    for file in pdf_files:
        remote_path = f"{SFTP_FOLDER}/{file.filename}"
        local_path = os.path.join(LOCAL_DIR, file.filename)

        print(f"Descargando: {file.filename}")
        sftp.get(remote_path, local_path)

        # Subir a Azure
        blob_client = blob_service_client.get_blob_client(
            container=AZURE_CONTAINER,
            blob=file.filename
        )

        with open(local_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"Subido a Azure: {file.filename}")

    sftp.close()
    transport.close()


if __name__ == "__main__":
    process_sftp_files()
    print("Proceso completado (máximo 5 PDFs)")