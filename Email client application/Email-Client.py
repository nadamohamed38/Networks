import smtplib
import imaplib
import email
from email.mime.multipart  import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox
from plyer import notification

def send_email():
    #get data from inputs
    sender_email = sender_email_entry.get()
    sender_password = sender_password_entry.get()
    receiver_email = recipient_email_entry.get()
    subject = subject_entry.get()
    body = body_txt.get('1.0',tk.END)
    #try except for any error during login or sending email 
    try: 
        
        msg = MIMEMultipart() # create email message 
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body,'plain'))
        
        server = smtplib.SMTP("smtp.gmail.com",587 ) #create smtp connection with gmail ( server address for gmail ,port number used for sending emails with TLS encryption)
        server.starttls() #transmit 
        server.login(sender_email,sender_password) #login
        server.sendmail(sender_email,receiver_email,msg.as_string()) 
        server.quit()        
        messagebox.showinfo("Success","Email sent Successfully!")
    except Exception as e:
        print(f"Error sending email : {e}")
        messagebox.showinfo("Error",f"Error sending email : {e}")
        

def receive_email():
    email_address = recipient_email_entry.get()
    password= sender_password_entry.get() #used same email for sending and receiving
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com",993)#create imap connection with gmail ( server address for gmail ,port number used for sending emails with SSL encryption)
        mail.login(email_address,password)
        mail.select('inbox') #select folder you want to access
        _,msgnums = mail.search(None,'ALL') #get all emails
        ids = msgnums[0].split() 
        latest_id = ids[-1] #access the last element which is the most recent email ID.
        
        #fetch the latest email's full content from the mail server and convert it into a readable email object.
        _,data = mail.fetch(latest_id ,'(RFC822)')
        message = email.message_from_bytes(data[0][1])
        
        #print data
        print(f"From : {message.get('From')}")
        print(f"Subject : {message.get('Subject')}")
        
        sender = message['From']
        subject = message['Subject']
        body = ""
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() =="text/plain":
                    body = part.get_payload(decode=True).decode() # Extracts the email content (decoded from Base64) and converts the byte string into a normal Python string
                    print("Body : \n", body)
                    break
        else: #If the email is not multipart, it means it contains only a single plain text body.
            print("Body : \n",message.get_payload(decode=True).decode()) 
            
        messagebox.showinfo("New Email",f"From : {sender} \nSubject : {subject}\n\n{body}")
        
        notification.notify(
            title = "New Email",
            message = f"From : {sender} \nSubject : {subject}\n\n{body}",
            timeout = 10
        )
        mail.logout()
        
    except Exception as e:
        print(f"Error receiving emaul : {e}")
        messagebox.showinfo("Error",f"Error sending email : {e}")



"""""
# if you want to try without GUI but add fun arguments

sender_email = input("sender email: ")
sender_password =  input("sender password: ")
receiver_email = input("recipient email: ")
receiver_password =  input("recipient password: ")
subject = input("subject: ")
body = input("body: ")
send_email(sender_email,sender_password,receiver_email,subject,body)
receive_email(receiver_email , receiver_password)
"""
root = tk.Tk()
root.title("Email Client Application")
root.geometry("400x400")

tk.Label(root,text="Sender Email: ").pack()
sender_email_entry = tk.Entry(root,width=40)
sender_email_entry.pack()

tk.Label(root,text="Password: ").pack()
sender_password_entry = tk.Entry(root,width=40,show='*')
sender_password_entry.pack()

tk.Label(root,text="Recipient Email: ").pack()
recipient_email_entry = tk.Entry(root,width=40)
recipient_email_entry.pack()

tk.Label(root,text="Subject: ").pack()
subject_entry = tk.Entry(root,width=40)
subject_entry.pack()

tk.Label(root,text="Body: ").pack()
body_txt = tk.Text(root,width=40,height=5)
body_txt.pack()

send_btn = tk.Button(root,text="Send",command=send_email)
send_btn.pack(pady=5)

receive_btn = tk.Button(root,text="check email",command=receive_email)
receive_btn.pack(pady=5)

root.mainloop()
