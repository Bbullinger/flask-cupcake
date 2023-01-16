"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import app, db, Cupcake, serialize_cupcake
from secret import my_password


@app.route("/")
def home_page():

    return render_template("index.html")


@app.route("/api/cupcakes", methods=["GET"])
def get_all_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized_cupcakes)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["GET"])
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized_cupcake)


@app.route("/api/cupcakes", methods=["POST"])
def post_cupcakes():

    # Logic to check if every required property exists in post request
    if not request.json["flavor"]:
        return print("Missing 'flavor'")
    elif not request.json["size"]:
        return print("Missing 'size'")
    elif not request.json["rating"]:
        return print("Missing 'rating'")
    # If all properties included, create a new cupcake instance
    else:
        flavor = request.json["flavor"]
        size = request.json["size"]
        rating = request.json["rating"]
        image_url = request.json["image_url"]
        new_cupcake = Cupcake(flavor, size, rating, image_url)

        # add cupcake instance to database, and give user json response, and 201 status code
        db.session.add(new_cupcake)
        db.session.commit()
        json_cupcake = jsonify(cupcake=serialize_cupcake(new_cupcake))

        return (json_cupcake, 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def patch_cupcakes(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # change properties to givens from user patch request. defaults to previous property if no value given
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image_url = request.json.get("image_url", cupcake.image_url)

    db.session.commit()

    serialized_cupcake = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized_cupcake)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcakes(cupcake_id):

    cupcake = Cupcake.query.et_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="deleted")
