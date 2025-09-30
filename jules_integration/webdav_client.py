import os
from webdav3.client import Client

class WebDAVClient:
    """
    A client to interact with a WebDAV server.

    This client reads connection details from environment variables:
    - WEBDAV_HOSTNAME: The full URL of the WebDAV server (e.g., https://webdav.example.com).
    - WEBDAV_LOGIN: The username for authentication.
    - WEBDAV_PASSWORD: The password for authentication.
    """
    def __init__(self):
        hostname = os.getenv("WEBDAV_HOSTNAME")
        login = os.getenv("WEBDAV_LOGIN")
        password = os.getenv("WEBDAV_PASSWORD")

        if not all([hostname, login, password]):
            raise ValueError(
                "Please set the WEBDAV_HOSTNAME, WEBDAV_LOGIN, and "
                "WEBDAV_PASSWORD environment variables."
            )

        self.options = {
            'webdav_hostname': hostname,
            'webdav_login': login,
            'webdav_password': password
        }
        self.client = Client(self.options)

    def list_files(self, remote_path="/"):
        """
        Lists files and directories on the WebDAV server.

        Args:
            remote_path (str): The remote directory path to list. Defaults to root.

        Returns:
            list: A list of files and directories.
        """
        try:
            return self.client.list(remote_path)
        except Exception as e:
            print(f"Error listing files at '{remote_path}': {e}")
            return []

    def download_file(self, remote_path, local_path):
        """
        Downloads a file from the WebDAV server.

        Args:
            remote_path (str): The path to the file on the server.
            local_path (str): The local path to save the file.

        Returns:
            bool: True if download was successful, False otherwise.
        """
        try:
            self.client.download_sync(remote_path=remote_path, local_path=local_path)
            print(f"Successfully downloaded '{remote_path}' to '{local_path}'")
            return True
        except Exception as e:
            print(f"Error downloading file '{remote_path}': {e}")
            return False

    def get_file_content(self, remote_path):
        """
        Downloads the content of a remote file into memory.

        Args:
            remote_path (str): The path to the file on the server.

        Returns:
            bytes: The content of the file, or None if an error occurs.
        """
        try:
            buffer = self.client.resource(remote_path).read()
            return buffer.decode('utf-8')
        except Exception as e:
            print(f"Error reading remote file content for '{remote_path}': {e}")
            return None

if __name__ == '__main__':
    # This is an example of how to use the client.
    # To run this, you must have the environment variables set.
    print("Attempting to connect to WebDAV server...")
    print("Please ensure WEBDAV_HOSTNAME, WEBDAV_LOGIN, and WEBDAV_PASSWORD are set.")

    try:
        webdav_client = WebDAVClient()
        print("Successfully created WebDAV client.")

        # Example: List files in the root directory
        print("\nListing files in root directory:")
        files = webdav_client.list_files()
        if files:
            for f in files:
                print(f"- {f}")
        else:
            print("No files found or could not connect.")

    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")