import paramiko
from azure.storage.blob import BlobServiceClient

# Configuración SFTP
SFTP_HOST = "localhost"
SFTP_PORT = 22
SFTP_USER = "testuser"
SFTP_PASSWORD = "testpass"
SFTP_FOLDER = "Done"

# Configutación Azure
AZURE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=https;"
    "AccountName=devstoreaccount1"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IF"
    "suFq2UVErCz4I6tiqIvPcneZCMpLkKqxZfDpP5YQ==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)
AZURE_CONTAINER = "pdfs-container"
BLOB_NAME = "archivo.txt"


def download_from_sftp():
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)

    sftp = paramiko.SFTPClient.from_transport(transport)
    local_file = "archivo.txt"
    sftp.get(SFTP_FOLDER, local_file)

    sftp.close()
    transport.close()

    return local_file


def upload_to_azure(file_path):
    blob_service_client = BlobServiceClient.from_connection_string(
        AZURE_CONNECTION_STRING
    )

    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME,
        blob=BLOB_NAME
    )

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)


if __name__ == "__main__":
    file_path = download_from_sftp()
    upload_to_azure(file_path)
    print("Archivo transferido correctamente")