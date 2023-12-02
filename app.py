import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, redirect, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
    "mongodb://diskarmn:Diska123@ac-sjiapka-shard-00-00.3lnlkgx.mongodb.net:27017,ac-sjiapka-shard-00-01.3lnlkgx.mongodb.net:27017,ac-sjiapka-shard-00-02.3lnlkgx.mongodb.net:27017/?ssl=true&replicaSet=atlas-vnije0-shard-0&authSource=admin&retryWrites=true&w=majority"
)
db = client.hotel


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/room")
def room():
    return render_template("room.html")


@app.route("/facility")
def facility():
    return render_template("facility.html")


@app.route("/book")
def book():
    return render_template("book.html")


@app.route("/tampil", methods=["GET"])
def tampil():
    room = list(db.remaining.find({}, {"_id": False}))
    return jsonify({"room": room})


@app.route("/berhasil", methods=["GET"])
def berhasil():
    name = request.args.get("name")
    phone = request.args.get("phone")
    people = request.args.get("people")
    date = request.args.get("date")
    regularroom = request.args.get("regularroom")
    regularnight = request.args.get("regularnight")
    diskaroom = request.args.get("diskaroom")
    diskanight = request.args.get("diskanight")
    specialroom = request.args.get("specialroom")
    specialnight = request.args.get("specialnight")
    message = request.args.get("message")
    
    return render_template(
        "berhasil.html",
        name=name,
        phone=phone,
        people=people,
        date=date,
        regularroom=regularroom,
        regularnight=regularnight,
        diskanight=diskanight,
        diskaroom=diskaroom,
        specialroom=specialroom,
        specialnight=specialnight,
        message=message,
      
    )


@app.route("/booking", methods=["POST"])
def booking():
    nomor=db.guest.count_documents({})
    urutan=nomor + 1
    name = request.form["name"]
    phone = request.form["phone"]
    people = request.form["people"]
    date = request.form["date"]
    regularroom = request.form["regularroom"]
    diskaroom = request.form["diskaroom"]
    specialroom = request.form["specialroom"]
    specialnight = request.form["specialnight"]
    message = request.form["message"]
    regularnight = request.form["regularnight"]
    diskanight = request.form["diskanight"]
    price_regular = 450000 * int(regularnight) + 450000 * int(regularroom)
    price_diska = 650000 * int(diskanight) + 450000 * int(diskaroom)
    price_special = 950000 * int(specialnight) + 450000 * int(specialroom)
    total = price_regular + price_diska + price_special
    data = {
        "num":urutan,
        "name/group": name,
        "phone": phone,
        "people": people,
        "date": date,
        "regularroom": regularroom,
        "regularnight": regularnight,
        "diskaroom": diskaroom,
        "diskanight": diskanight,
        "specialroom": specialroom,
        "specialnight": specialnight,
        "message": message,
        "total": total,
        "status":"pesan"
    }
    db.guest.insert_one(data)
    # mengurangi nilai asli dari sisa kamar

    regular = db.remaining.find_one({}, {"_id": 0, "regular": 1})["regular"]
    diska = db.remaining.find_one({}, {"_id": 0, "diska": 1})["diska"]
    special = db.remaining.find_one({}, {"_id": 0, "special": 1})["special"]
    db.remaining.update_one(
        {},
        {
            "$set": {
                "regular": int(regular) - int(regularroom),
                "diska": int(diska) - int(diskaroom),
                "special": int(special) - int(specialroom),
            }
        },
    )
    return redirect(
        url_for(
            "berhasil",
            name=name,
            phone=phone,
            people=people,
            date=date,
            regularroom=regularroom,
            regularnight=regularnight,
            diskanight=diskanight,
            diskaroom=diskaroom,
            specialnight=specialnight,
            specialroom=specialroom,
            message=message,
        )
    )

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
