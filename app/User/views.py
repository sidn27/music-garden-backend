import requests
from flask import g
from flask import json
from flask import request

from app import db
from app.Music.models import Song
from app.User.jwt_utils import login_required, create_token
from app.utils import create_success_response, create_error_response
from .models import User, User_Song
from . import user_bp

@user_bp.route('/me', methods=['GET'])
@login_required
def me():
    try:
        user = User.query.filter_by(id=g.user_id).first()

        ret = user.export_data()
        ret['response'] = 'success'

        return create_success_response(ret)

    except Exception as e:

        return create_error_response(str(e))

@user_bp.route('/signIn')
def android_google():
    try:
        if 'google_token' not in request.args:
            return create_error_response("Missing google_token")

        url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + str(request.args['google_token'])

        response = requests.get(url)

        data = json.loads(response.text)

        if response.status_code == 200:

            email = data.get('email', None)
            name = data.get('name', None)
            image_url = data.get('picture', None)
            profile_sub = data.get('sub', 0)

            user = User.query.filter_by(email=email).first()

            # if user has registered with same email before, update

            if user is not None:

                user.name = name
                user.image_url = image_url

                db.session.add(user)

            # if user does not exist, create

            else:

                user = User()

                data = {
                    "name": name,
                    "image_url": image_url,
                    "email": email
                }

                user.import_data(data)

                db.session.add(user)


            db.session.flush()

            token = create_token(user)

            db.session.commit()

            response = {
                "token": token,
                "user_detail": user.export_data()
            }
            return create_success_response(response)

        else:
            return create_error_response(data.get('error_description', 'Failed to login. Please try again.'))

    except Exception as e:

        db.session.rollback()

        return create_error_response(str(e))

@user_bp.route('/addSong', methods=['GET'])
@login_required
def addSong():
    try:
        if 'song_id' not in request.args:
            create_error_response("Missing song_id")

        song = Song.query.get(request.args['song_id'])

        if song is None:
            return create_error_response("No such song exists")

        entry = User_Song()
        data = {}
        data['user_id'] = g.user_id
        data['song_id'] = request.args['song_id']

        entry.import_data(data)
        db.session.add(entry)

        db.session.commit()

        return create_success_response()

    except Exception as e:

        db.session.rollback()

        return create_error_response(str(e))
