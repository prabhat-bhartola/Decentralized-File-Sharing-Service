from flask import Flask, request, redirect, jsonify
from flask import render_template
from flask import current_app as app
from flask import send_file, send_from_directory, safe_join, abort

from application.models import *
from application import tools

from application import config
from flask_socketio import send
import socket

socketio = config.socketio


@socketio.on('message')
def get_initial_data(data):
	"""
	Get local description and socket id of the client and store them in database.
	"""

	socket_id = data["socket_id"]
	localDesc = data["local_desc"]

	user_ip = str(request.remote_addr)

	user = Users.query.filter_by(ip_addr=user_ip).first()

	user.host_sdp = str(localDesc)
	user.socket_id = str(socket_id)

	db.session.commit()


@socketio.on('client_initialized')
def get_client_ld(data):
	"""
	Runs after initializing the client RTCpeer connection
	Sends local description back to the host 
	"""
	# print(data)
	# socketio.emit('finalize-conn', {'localDesc': data}, "_DKcGph1fETiCsg1AAAF")
	user_file_info = db.session.query(Files, Users)\
			.filter(Files.u_ip == Users.ip_addr and Files.file_no == file_no).first()
	
	host_sid = user_file_info.Users.socket_id
	# print(host_sid)

	socketio.emit('complete-handshake', data, to=host_sid)


@socketio.on('get-download-sd')
def get_download_sd(localDesc):
	print(localDesc)


def get_server_ip():
	"""
	Get the ip address of the server
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	server_ip = s.getsockname()[0]
	s.close()

	return str(server_ip)

@app.route("/get-sdp-of-uploader/<int:file_no>", methods=["GET"])
def get_sdp(file_no):
	"""
	Get the sdp of the uploader from file number
	"""
	user_file_info = db.session.query(Files, Users)\
			.filter(Files.u_ip == Users.ip_addr and Files.file_no == file_no).first()

	return user_file_info.Users.host_sdp


@app.route("/", methods=["GET", "POST"])
def home():
	'''
	Show all files and chats in home page.
	STORE/UPDATE the session description protocol of user along with user info like ip address etc.
	'''

	if request.method == "GET":

		try:
			# INSERT THE NEW GENERATED SDP INTO USER TABLE
			# NEW QUERY FOR FETCHING FILES
			user_ip = str(request.remote_addr)

			user = Users.query.filter_by(ip_addr=user_ip).first()

			if user is None:
				# GET THE SDP AND INSERT WITH ALL OTHER DETAILS
				new_user = Users(user_ip, "anonymous", "")

				db.session.add(new_user)
				db.session.commit()

			else:
				#GET THE NEW SDP AND UPDATE IT
				pass

			files = Files.query.all()
			# chats = Chats.query.all()

			return render_template("home.html", files=files)

		except:

			return render_template("went_wrong.html")

	else:

		return render_template("went_wrong.html")


@app.route("/chat", methods=["GET", "POST"])
def send_recieve_message():
	"""
	FOR IMPLEMENTING CHAT FUNCTIONALITY
	"""

	if request.method == "GET":

		chats = Chats.query.order_by(Chats.chat_no.asc()).all()

		result = []
		for chat in chats:

			if chat.author_ip == get_server_ip():
				written_by = "~PRABHAT BHARTOLA"
			else:
				written_by = "~" + chat.author_ip[:3] + ".XXX.XX." + chat.author_ip[11:]

			result.append({
				"written_by": written_by,
				"date_created": chat.date_created,
				"time_created": chat.time_created,
				"message": chat.content
			})
		return render_template("load_chats.html", chats=result)

	elif request.method == "POST":

		message = request.form["message"]

		if len(message):

			author_ip = request.remote_addr
			new_message = Chats(message, author_ip)
			db.session.add(new_message)

			db.session.commit()

			return jsonify({'result': 'success'})

		else:

			return jsonify({'result': 'fail'})
	else:
		pass


@app.route("/download/<int:file_no>/", methods=["GET", "POST"])
def download_file(file_no):
	'''
	Download file as an attachment

	Parameters
	----------
	file_no : int -> A unique number assigned to every file
	'''

	try:

		file_info = Files.query.filter_by(file_no=file_no).first()
		file_name = str(file_info.file_name)
		file_path = str(file_info.file_path)

		return send_from_directory(directory=file_path, path=file_path, filename=file_name, as_attachment=True)

	except Exception as e:
		'''
		If file is not present, Set currently hosted to 0
		'''
		# NEW QUERY FOR UPDATING CLIENT STATUS

		user = db.session.query(Files, Users)\
			.filter(Files.u_ip == Users.ip_addr).first()

		if user.Users.conn_status == 1:
			req_file = Files.query.filter_by(file_no=file_no)
			req_file.delete()

			db.session.commit()

			msg = """
				The name of the file or the path entered by the user is wrong.
				This file will be deleted.
			"""
			return render_template("file_not_found.html", message = msg)

		return render_template("file_not_found.html", message = "The user seems to be not connected to the WIFI")
		# return send_from_directory(directory="/home/prabhat/Downloads", path="/home/prabhat/Downloads", filename="kali.jpg", as_attachment=True)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
	'''
	Upload file information into the database
	'''

	if request.method == "GET":

		try:
			return render_template("upload_file.html")

		except:
			return render_template("went_wrong.html")

	elif request.method == "POST":
		'''
		Get file info using HTML form and store in database
		'''

		try:
			file_name = request.form["file_name"]
			abs_path = request.form["abs_path"]
			desc = request.form["description"]
			ip = str(request.remote_addr)

			file_type = tools.get_type_from_ext(file_name)

			new_file = Files(file_name, file_type, "-", abs_path, desc, ip)

			db.session.add(new_file)
			db.session.commit()

			return redirect("/")

		except:

			return render_template("went_wrong.html")

	else:
		return render_template("went_wrong.html")


@app.route("/donate", methods=["GET"])
def donate():
	return render_template("donate.html")


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/contact")
def contact():
	return render_template("contact.html")