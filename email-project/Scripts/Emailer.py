import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr, formatdate
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

def main():
        print("hello world")

if __name__ == "__main__":
    main()

class Emailer:
    # Tester information:
    # sender_name = "Johnny Appleseed"
    # sender_email = "t69206445@outlook.com"
    # sender_password = "tHi5isT3ster3M4!L"

    def __init__ (self, name, email, password, port_number = 587, server = "smtp.office365.com"):
        self.port = port_number
        self.smtp_server = server
        self.sender_name = name
        self.sender_email = email
        self.sender_password = password

    def send_email(self, recipient_name, recipient_email, subject = "", body = "", attachment_paths = None):
        """
        This function sends an email that can have attachments to a specified user
        Args:
            recipient_name (str): Name of recipient
            recipient_email (str): Email address of the recipient
            subject (str, optional): The subject of the email. Defaults to "".
            body (str, optional): The message of the email. Defaults to "".
            attachment_paths (str or list, optional): Any attachments for the email in the form of paths. Defaults to None.

        Returns:
            bool: returns true if the email sent successfully
        """
        # Create a MIMEMultipart object because we need to send attachments and text
        message = MIMEMultipart()

        # Sets up the basic details of the email (To whom, from whom, date)
        message["From"] = formataddr((self.sender_name.strip(), self.sender_email.strip()))
        message["To"] = formataddr((recipient_name.strip(), recipient_email.strip()))
        message["Date"] = formatdate(localtime = True)
        
        # Add the subject and the body to the message
        message["Subject"] = subject
        message.attach(MIMEText(body))

        # If there was an attachment specified but it failed to add, the function will return False
        if (not add_attachments(attachment_paths, message)):
            return False

        # This object controls aspects of the SSL/TLS protocol
        context = ssl.create_default_context()

        try:
            # Connects to the SMTP server with the specified port
            server = smtplib.SMTP(self.smtp_server, self.port)

            # Initiates a secure connection using TLS
            server.starttls(context=context)

            # Authenticate login details
            server.login(self.sender_email, self.sender_password)
        
            # Send the email
            server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            # Disconnect
            server.quit()
            
            # Returns true if the email sent successfully
            return True
            
        except Exception as e:
            print("Error sending mail:", str(e))    

        # Returns false if there was an error somewhere in the process
        return False


def add_attachments(attachment_paths, message):
    """
    This is a helper method for send_email, and it handles the inputs for attachment_paths
    Args:
        attachment_paths (str or list): either a list of or single pathname
        message (MIMEMultipart): the email object

    Returns:
        bool: returns true if the attachment(s) added successfully
    """
    success = True

    # If there are no attachments to be added, return true
    if (not attachment_paths):
        return True
    
    # If there are a list of attachments
    elif (isinstance(attachment_paths, list)):
        for path in attachment_paths:
            success &= add_path_to_message(message, path)

    # If there is only one attachment
    elif (isinstance(attachment_paths, str)):
        success &= add_path_to_message(message, attachment_paths)
    
    # If the attachment pathname is invalid
    else:
        return False
    
    return success
        

def add_path_to_message(message, path):
    """
    This is a helper method for add_attachments, and it does the actual "attaching" part
    Args:
        message (MIMEMultipart): _description_
        path (str): the path of the attachment

    Returns:
        bool: returns true if the attachment added
    """
    try:
        # Creates an attachment object
        part = MIMEBase('application', "octet-stream")

        # Opens and processes the file with the given path
        with open(path, 'rb') as file:
            part.set_payload(file.read())

        # Encodes the attachment's payload to Base64 format
        encoders.encode_base64(part)

        # Sets the name of the attachment
        part.add_header('Content-Disposition', 'attachment; filename={}'.format(Path(path).name))
        
        # Add attachment to email
        message.attach(part)
        return True
    
    except Exception as e:
        print("The inputed path is not a real path:", path)

    # Returns false if the attachment could not be added
    return False

    