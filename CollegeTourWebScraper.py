import requests
from bs4 import BeautifulSoup
import smtplib
import time
import schedule
import datetime

# Set up the email parameters
sender_email = ""
receiver_email = ""
# 16 digit password for sender email
password = ""

# Set up the message to send when a tour opening is found
message = "Subject: ALERT REGISTRATION OPEN APRIL 14"

emailSent = 0


# Scrapes the tour website, and sends an email update if a tour opening is found
def scrapeWebsite():
    global emailSent

    # Make the request to the tour website

    # 10:00am
    response1 = requests.get('https://admission.bc.edu/portal/campusvisit?id=631cd122-685f-4812-b2e1-2a4f1ddf3211')
    # 12:00pm
    response2 = requests.get('https://admission.bc.edu/portal/campusvisit?id=856e0f43-0432-4a71-ae25-f301576d7f89')
    # 2:00pm
    response3 = requests.get('https://admission.bc.edu/portal/campusvisit?id=1da30d38-c859-450b-8c24-89eaadeebdcf')

    # Parse the response to HTML
    soup1 = BeautifulSoup(response1.text, 'html.parser')
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    soup3 = BeautifulSoup(response3.text, 'html.parser')

    # Find the element that contains the 'no tours found' error
    data1 = soup1.find('p', class_='error')
    data2 = soup2.find('p', class_='error')
    data3 = soup3.find('p', class_='error')

    # Log the attempt to find a tour in the local console

    current_time = datetime.datetime.now()
    print("-------------------------------------------------------------------------------------------------------")
    print("---------- The current time is:", current_time, " -------------------------------------------")
    print("10:00 - ", data1)
    print("12:00 - ", data2)
    print("2:00 - ", data3)

    # If any of the time slots do not contain a 'tour not found' error, send an email notification
    if data1 is None or data2 is None or data3 is None:
        print("Error not found on some tour")
        # Set up the SMTP server and send the message
        if emailSent == 0:  # Ensures an email hasn't been sent yet about this opening to avoid spamming the inbox
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message)
                print("Email sent successfully!")
                emailSent = 1
        else:
            print("Email sent previously - not sent again")
    else:
        print("All tours contain errors - no email sent")
        emailSent = 0

    print("-------------------------------------------------------------------------------------------------------\n")


schedule.every(30).seconds.do(scrapeWebsite)

while True:
    schedule.run_pending()
    time.sleep(1)
