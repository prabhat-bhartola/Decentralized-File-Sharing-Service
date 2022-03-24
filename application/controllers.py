from flask import Flask, request, redirect, jsonify
from flask import render_template
from flask import current_app as app
from flask import send_file, send_from_directory, safe_join, abort

from application.models import *
from application import tools


# @app.route("/get-ip", methods=["GET"])
# def get_user_ip():
# 	return request.remote_addr


@app.route("/")
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
				new_user = Users(user_ip, "anonymous", "host sd", "client sd")

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
def send_message():
	"""
	FOR IMPLEMENTING CHAT FUNCTIONALITY
	"""

	if request.method == "GET":

		chats = Chats.query.all()

		result = []
		for chat in chats:
			result.append({
				"written_by": chat.author_ip,
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
				The filename is wrong or the file path entered by the user is wrong.
				This file will be deleted.
			"""
			return render_template("file_not_found.html", message = msg)

		return render_template("file_not_found.html", message = "The user seems to be not connected to the WIFI")


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

			new_file = Files(file_name, file_type, 00, abs_path, desc, ip)

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