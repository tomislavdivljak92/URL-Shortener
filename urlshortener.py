from flask import Flask,render_template,request,redirect, url_for,flash,abort,session,jsonify
import json
import os.path

app = Flask(__name__) #creation of an instance of the clas called Flask, stored in a variable app.
app.secret_key = "abrakadabra"

@app.route("/") # the route decorator tells flask what url should trigger a function.
def index(): # view func contains response to the request your app recieves.
    return render_template("index.html",codes=session.keys()) # returns a response to be dispayed by web browser.

@app.route("/your-url",methods=["GET","POST"]) #we specified two methodn we r going to use.
def your_url():
    if request.method == "POST":
        urls= {} #emphy dict for user input
        if os.path.exists("urls.json"):# checking if its exist
            with open("urls.json") as urls_file: # creating or opening json file
                urls = json.load(urls_file) # load file, if its there it opens it
        if request.form["code"] in urls.keys():
            flash("already been taken")
            return redirect(url_for("index"))

        urls[request.form["code"]] = {"url":request.form["url"]}
        with open("urls.json","w") as url_file:
            json.dump(urls,url_file)
            session[request.form["code"]]=True # whatever is captured, session is activated by true
        return render_template("your_url.html", code=request.form["code"])
    else:
        return redirect(url_for("index"))

@app.route("/<string:code>") # string that will capture the short name that the user input
def redirect_to_url(code): # finction will work with captured name
    if os.path.exists("urls.json"): # checking
        with open("urls.json") as urls_file:
            urls = json.load(urls_file) # load file in urls variable
            if code in urls.keys(): # is our short name present
                if "url" in urls[code].keys(): # is our link present in file
                    return redirect(urls[code]["url"]) # linked code with url
    return abort(404)



@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"),404

@app.route("/api") # storing user inputs into a list
def session_api():
    return jsonify(list(session.keys()))
