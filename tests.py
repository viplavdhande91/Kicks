import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import sys

sender_address = 'vpp.19p10242@mtech.nitdgp.ac.in'
PASSWORD = '*viplavgate012345678#'


names = ['IB']
rec_email = 'viplavdhande91@gmail.com'


df_1 = ([1,2,3,5])
df_2 = ([10,20,30,50])
df_test =pd.concat([pd.DataFrame(df_1),pd.DataFrame(df_2)],axis=1)



recipients = ['viplavdhande91@gmail.com'] 
emaillist = [elem.strip().split(',') for elem in recipients]
msg = MIMEMultipart()
msg['Subject'] = "dataframe table TEST FROM GMAIL"
msg['From'] = sender_address

html = """\
        <html>
          <head></head>
          <body>
            {0}
          </body>
        </html>
""".format(df_test.to_html(index=False))

part1 = MIMEText(html, 'html')
msg.attach(part1)

try:
    """Checking for connection errors"""

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()#NOT NECESSARY
    server.starttls()
    server.ehlo()#NOT NECESSARY
    server.login(sender_address,PASSWORD)
    server.sendmail(msg['From'], emaillist , msg.as_string())
    server.close()

except Exception as e:
    print("Error for connection: {}".format(e))