#!/usr/bin/env python
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

script = sys.argv[0]
if len(sys.argv) != 7 and len(sys.argv) != 8 and len(sys.argv) != 9 and len(sys.argv) != 10 and len(sys.argv) != 11:
    print 'Usage: '+ script +' smtp_server, port, from_email, to_emails, subject, body_text, password(optional), lan_id(optional), cc_emails(optional), file_to_attach(optional)'
    print "for optional arguments, please use empty string '' to fill"
    sys.exit(1) 

def send_email(smtp_server, port, from_email, to_emails, subject, body_text, password = None, lan_id = None, cc_emails = None, file_to_attach = None):
	# prepare msg
	text = """
	Hi Team,
	{body}
	"""

	html = """
	<html><body><p>Hi Team,</p>
	<p>{body}</p>
	</body></html>
	"""
	
	text = text.format(body=body_text)
	html = html.format(body=body_text)

	msg = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html,'html')])

	msg['From'] = from_email
	msg['To'] = to_emails
	msg['Subject'] = subject
	rcpt_list = to_emails.split(",")

	if cc_emails is not None and cc_emails != '':
		msg['Cc'] = cc_emails
		rcpt_list = rcpt_list + cc_emails.split(",")

	# print rcpt_list	

	# prepare attachment
	if file_to_attach is not None and file_to_attach != '':
		base_path = os.path.dirname(os.path.abspath(__file__))
		file_location = base_path+'/'+file_to_attach
		try:
			part = MIMEBase('application', 'octet-stream')
			part.set_payload(open(file_location, "rb").read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; filename= %s" % file_to_attach)
			msg.attach(part)
		except Exception as e:
		   	print e
	
	try:
		server = smtplib.SMTP(smtp_server, port)
		#server.set_debuglevel(1)
		server.ehlo()
		server.starttls()

		if password is not None and password != '':
			lan_id_s = lan_id
			if lan_id_s is not None and lan_id_s != '':
				server.login(lan_id_s, password)
			else:
				server.login(msg['From'], password)

		server.sendmail(msg['From'], rcpt_list, msg.as_string())

		print "successfully sent email to %s" % (', '.join(rcpt_list))
			
	except Exception as e:
		print e
	finally:
		server.quit()


	smtp_server = sys.argv[1]
	port = int(sys.argv[2])
	from_email = sys.argv[3]
	to_emails = sys.argv[4]
	subject = sys.argv[5]
	body_text = sys.argv[6]
	
	password = None
	if len(sys.argv) >= 8:
		password = sys.argv[7]

	lan_id = None
	if len(sys.argv) >= 9:
		lan_id = sys.argv[8]
	
	cc_emails = None
	if len(sys.argv) >= 10:
		cc_emails = sys.argv[9]

	file_to_attach = None	
	if len(sys.argv) == 11:
		file_to_attach = sys.argv[10]

	# print smtp_server
	# print port
	# print from_email
	# print to_emails
	# print subject
	# print body_text
	# print password
	# print cc_emails
	# print file_to_attach

	if smtp_server != 'applicationrelay.corp.roy.com' and smtp_server != 'applicationrelay.corptst.roy.com' and smtp_server != 'applicationrelay.apps.roy':
		print 'SMPT server is not validated'
		sys.exit(1)

	send_email(smtp_server, port, from_email, to_emails, subject, body_text, password, lan_id, cc_emails, file_to_attach)

if __name__ == '__main__':
	main()	
