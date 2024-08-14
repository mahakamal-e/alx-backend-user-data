#!/usr/bin/env python3
""" Flask app Module """
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """ Return JSON playload"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """implement endpoint to register user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({'email': user.email, 'message': 'user created'})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """login endpoint"""
    email = request.form.get('email')
    password = request.form.get('password')
    check_valid = AUTH.valid_login(email, password)

    if check_valid:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout end-point."""
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')

    abort(403)

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """profile end-point"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify({"email": user.email})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
