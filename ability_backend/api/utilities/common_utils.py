# regex validation
import os
import uuid


validation_dict = {
    "name": r'^[a-zA-Z0-9\s\-_]+$',
    "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    "license": r'^[0-9]{9}$',
    "password": r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$',
    "phone": r'^\d{10}$'
}


def write_file(file):
    return_val = False
    upload_folder = 'uploads'
    try:
        os.makedirs(upload_folder, exist_ok=True)
        random_suffix = str(uuid.uuid4())

        # Append the UUID to the original file name
        unique_file_name = f"{file.name}_{random_suffix}"
        file_path = os.path.join(upload_folder, unique_file_name)

        # Save the file to the server
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return_val = file_path
    except Exception as e:
        print(f"Exception occured file creating writing file: {e}")
    return return_val