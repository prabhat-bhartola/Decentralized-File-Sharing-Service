from flask import Flask, request, redirect, jsonify
from flask import render_template
from flask import current_app as app
from flask import send_file, send_from_directory, safe_join, abort
import os
from application.models import *
from application import tools


@app.route("/")
def home():
	'''
	Show all files and chats in home page
	'''

	if request.method == "GET":

		try:

			files = Files.query.all()
			chats = Chats.query.all()

			return render_template("home.html", files=files)

		except:

			return render_template("went_wrong.html")
	# elif request.method == "POST":

	# 	try:

	# 		message = request.form["message"]

	# 		new_message = Chats("anonymous", message)
	# 		db.session.add(new_message)
	# 		db.session.commit()
	# 		# return redirect("/home")
	# 		return redirect(request.referrer)
	# 		# return jsonify({'result': 'success'})
	# 	except Exception as e:
	# 		print(e)
	# 		return render_template("went_wrong.html")	
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
				"written_by": chat.written_by,
				"datetime_created": chat.datetime_created,
				"message": chat.message
			})
		return render_template("load_chats.html", chats=chats)

	elif request.method == "POST":

		message = request.form["message"]

		if len(message):

			new_message = Chats("anonymous", message)
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
		If file is not present, Remove it from the database
		'''
		curr_file = Files.query.filter_by(file_no=file_no).first()
		db.session.delete(curr_file)

		db.session.commit()

		return render_template("file_not_found.html")


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

			file_type = tools.get_type_from_ext(file_name)

			new_file = Files(file_name, file_type, 00, abs_path, "User", desc)

			db.session.add(new_file)
			db.session.commit()

			return redirect("/")

		except:

			return render_template("went_wrong.html")

	else:
		return render_template("went_wrong.html")