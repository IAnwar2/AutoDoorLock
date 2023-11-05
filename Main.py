import os
import cv2
from tkinter import simpledialog, messagebox

import FaceRecog as fr

masterUsername = "1"
masterPassword = "1"
skipStartup = False
quitInStartup = False


credentials_file_path = 'credentials.txt'


# Make sure folder will exist
if not os.path.exists(fr.main_folder_path):
    os.makedirs(fr.main_folder_path)

# Make sure file with user info exists
if not os.path.exists(credentials_file_path):
    # If the file doesn't exist, create an empty file
    with open(credentials_file_path, 'w'):
        pass 


def write_credentials_to_file(username, password):
    # Open the file in 'a' mode (append) to add new credentials without overwriting existing content
    with open(credentials_file_path, 'a') as file:
        file.write(f'{username}:{password}\n')


def find_credentials_in_file(username, password):

    try:
        # Open the file in 'r' mode (read)
        with open(credentials_file_path, 'r') as file:
            # Iterate through each line in the file
            for line in file:
                # Split the line into username and password based on the colon
                stored_username, stored_password = line.strip().split(':')
                
                # Check if the stored_username matches the target username
                if stored_username == username and stored_password == password:
                    return True

        # If the inputs is not found
        return False

    except FileNotFoundError:
        print(f"The file '{credentials_file_path}' does not exist.")
        return False
    
def count_files_in_folder(folder_path):
    try:
        files = os.listdir(folder_path)
        return len(files)
    except FileNotFoundError:
        print(f"The folder '{folder_path}' does not exist.")
        return 0

def capture_and_save_image(name, path):
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Capture a single frame
    ret, frame = cap.read()

    imgNum = str(count_files_in_folder(path) + 1)

    # Save the captured frame to a specific folder with the user's name
    image_path = f'{path}/{name}-{imgNum}.jpg'
    cv2.imwrite(image_path, frame)

    # Release the webcam
    cap.release()


def Startup():
    global quitInStartup

    choice = simpledialog.askstring("Input", "Log in or create new account or quit (l/c/q):")

    while choice != "l" and choice != "c" and choice != "q":
        choice = simpledialog.askstring("Input", "Log in or create new account or quit (l/c/q):")

    if choice == 'q': # Quit
        quitInStartup = True
    elif choice == 'l': # Log in
        entered_user = simpledialog.askstring("Input", "Enter Username:")
        entered_pass = simpledialog.askstring("Input", "Enter Password:")

        while not find_credentials_in_file(entered_user, entered_pass):
            messagebox.showinfo("Incorrect Login","Either your Username or Password were invalid. Try Again")
            entered_user = simpledialog.askstring("Input", "Enter Username:")
            entered_pass = simpledialog.askstring("Input", "Enter Password:")

        messagebox.showinfo("Login",f"You logged in as {entered_user}")
        fr.loggedInUser = entered_user
    else: # Create new account
        entered_master_user = simpledialog.askstring("Input", "Enter Master Username:")
        entered_master_pass = simpledialog.askstring("Input", "Enter Master Password:")

        while entered_master_user != masterUsername or entered_master_pass != masterPassword:
            entered_master_user = simpledialog.askstring("Input", "Enter Master Username:")
            entered_master_pass = simpledialog.askstring("Input", "Enter Master Password:")
        
        # create new account - username, password
        new_user = simpledialog.askstring("Input", "Enter new Username:")
        new_pass = simpledialog.askstring("Input", "Enter new Password:")

        write_credentials_to_file(new_user,new_pass)

        # Make sure user folder will exist
        if not os.path.exists(f'{fr.main_folder_path}/{new_user}'):
            os.makedirs(f'{fr.main_folder_path}/{new_user}')

        fr.loggedInUser = new_user
        messagebox.showinfo("Picture Needed","No pictures currently saved to this profile. Your picture will be taken")
        AddPic()

def AddPic():
    capture_and_save_image(fr.loggedInUser, f'{fr.main_folder_path}/{fr.loggedInUser}')


def main():
    global skipStartup
    global quitInStartup

    # Initialize the variables
    skipStartup = False
    quitInStartup = False

    while True:

        if not skipStartup:
            Startup()
        
        if quitInStartup:
            break

        entered_master_user = simpledialog.askstring("Input", "Start Recog, add new pic, Log out, or Quit? (s,a,l,q):")
        
        while entered_master_user != "a" and entered_master_user != "l" and entered_master_user != "q" and entered_master_user != "s":
            entered_master_user = simpledialog.askstring("Input", "Start Recog, add new pic, Log out, or Quit? (s,a,l,q):")

        if entered_master_user == "s":
            skipStartup = True
            fr.startRecognition()
        if entered_master_user == "a":
            skipStartup = True
            messagebox.showinfo("Picture Needed","To add picture, your picture will be taken")
            AddPic()
        elif entered_master_user == "l":
            skipStartup = False
        elif entered_master_user == "q":
            break
        
if __name__ == "__main__":
    main()