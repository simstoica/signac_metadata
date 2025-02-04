import os
import json

from irods.session import iRODSSession

# Creates iRODS session object. It reads the iRODS environment
# file from the default location (~/.irods/irods_environment.json)
# and uses it to initialize the session. No SSL settings are
# specified, so the session will use the default SSL behavior.
# Specifically, it will use the existing irods session
def get_irods_session():
    env_file = os.path.expanduser('~/.irods/irods_environment.json')
    ssl_settings = {}
    return iRODSSession(irods_env_file=env_file, **ssl_settings)


def find_local_files_by_name(folder_path, filename):
    """
    Searches a folder and its subfolders for all files with a given name.

    Args:
        folder_path: The path to the folder to search.
        filename: The name of the file to search for.

    Returns:
        A list of the full paths to all files with the given name.
    """

    matching_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file == filename:
                matching_files.append(os.path.join(root, file))
    return matching_files


def read_local_json_file(file_path):
    """Reads a JSON file and parses its contents into a dictionary.

    Args:
        file_path: Path to the JSON file.

    Returns:
        A dictionary representing the JSON data, or None if an error occurs.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing JSON file: {e}")
        return None


def set_avu(irods_object, json_data):
    """Transforms a JSON dictionary into iRODS AVUs and assigns them to an iRODS collection atomically.

    Args:
        irods_collection: The iRODS collection object.
        json_data: The JSON data as a dictionary.
    """
    try:
        for key, value in json_data.items():
            irods_object.metadata.add(str(key), str(value))
    except Exception:
        print(f"Error setting AVUs on object {irods_object.path}")


def get_irods_object_from_local_path(session, file_path, local_path, irods_root_path="FILL_THIS_IN"):
    """Gets an iRODS object (file or collection) from a local path.

    Args:
        session: The iRODS session object.
        local_path: The local file path.
        irods_prefix: The iRODS prefix corresponding to the local root.

    Returns:
        The iRODS object (DataObject or Collection), or None if not found or on error.
    """
    # map_local_name_to_irods_object_name
    irods_path = file_path.replace(local_path, irods_root_path)
    print(file_path, local_path, irods_path)

    try:
        return session.data_objects.get(irods_path)
    except:  # noqa: E722 # bare except is ok here, we handle all exceptions the same
        pass  # Ignore if it's not a data object

    try:
        return session.collections.get(irods_path)
    except:  # noqa: E722 # bare except is ok here, we handle all exceptions the same
        pass  # Ignore if it's not a collection

    return None


if __name__ == "__main__":
    session = get_irods_session()

    local_path = "path/to/local/data"  # Example local path, replace as needed
    metdata_file_name = 'signac_statepoint.json'
    irods_root_poath = '/path/to/corresponding/irods/data'

    session = get_irods_session()

    found_files = find_local_files_by_name(local_path, metdata_file_name)
    for file_path in found_files:
        if data := read_local_json_file(file_path):
            if irods_object := get_irods_object_from_local_path(session, file_path, local_path,  irods_root_poath):
                set_avu(irods_object, data)
            else:
                print(f"iRODS object not found for local path: {file_path}")

    session.cleanup()
