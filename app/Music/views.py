from flask import g, jsonify
from flask import request
from app import db
from app.User.jwt_utils import login_required
from app.User.models import User_Song
from app.utils import create_error_response, create_success_response, paginatedQuery, getPageCount, create_success_list_response
from . import music_bp
from .models import Artist, Album, Song


@music_bp.route('/addArtist', methods=['POST'])
def addArtist():

    try:
        data = request.json

        artist = Artist()

        artist.import_data(data)

        db.session.add(artist)

        db.session.commit()

        return create_success_response(artist.export_data())

    except Exception as e:

        db.session.rollback()

        return create_error_response(str(e))


@music_bp.route('/addAlbum', methods=['POST'])
def addAlbum():

    try:
        data = request.json

        album = Album()

        album.import_data(data)

        db.session.add(album)

        db.session.commit()

        return create_success_response(album.export_data())

    except Exception as e:

        db.session.rollback()

        return create_error_response(str(e))


@music_bp.route('/addSong', methods=['POST'])
def addSong():

    try:
        data = request.json

        song = Song()

        song.import_data(data)

        db.session.add(song)

        db.session.commit()

        return create_success_response(song.export_data())

    except Exception as e:

        db.session.rollback()

        return create_error_response(str(e))

@music_bp.route('/getArtistList', methods=['GET'])
def getArtistList():

    try:

        page_number = 0
        if 'page' in request.args:
            page_number = request.args['page']

        artists = paginatedQuery(Artist, page_number)

        artist_list = []

        for artist in artists:
            artist_list.append(artist.export_data())

        return create_success_list_response(artist_list, getPageCount(Artist))

    except Exception as e:

        return create_error_response(str(e))


@music_bp.route('/getAlbumList', methods=['GET'])
def getAlbumList():
    try:

        page_number = 0
        if 'page' in request.args:
            page_number = request.args['page']

        condition = None
        if 'artist_id' in request.args:
            albums = paginatedQuery(Album, page_number, Album.artist_id == request.args['artist_id'])
            condition = Album.artist_id == request.args['artist_id']

        else:
            albums = paginatedQuery(Album, page_number)

        album_list = []

        for album in albums:
            album_list.append(album.export_data())

        return create_success_list_response(album_list, getPageCount(Album, condition))

    except Exception as e:

        return create_error_response(str(e))


@music_bp.route('/getSongList', methods=['GET'])
@login_required
def getSongList():
    try:

        page_number = 0
        if 'page' in request.args:
            page_number = request.args['page']

        condition = None
        if 'album_id' in request.args:
            songs = paginatedQuery(Song, page_number, Song.album_id == request.args['album_id'])
            condition = Song.album_id == request.args['album_id']

        else:
            songs = paginatedQuery(Song, page_number)


        song_list = []

        for song in songs:
            userSong = User_Song.query.filter_by(User_Song.song_id == song.id).first()
            song_list.append(song.export_data(userSong.user_id == g.user_id))

        return create_success_list_response(song_list, getPageCount(Song, condition))

    except Exception as e:

        return create_error_response(str(e))

@music_bp.route('/getArtist', methods=['GET'])
def getArtist():
    try:

        response = {}

        if 'id' in request.args:
            artist = Artist.query.get(int(request.args['id']))

            if artist is not None:

                album_list = []

                albums = Album.query.filter_by(artist_id=artist.id)

                for album in albums:
                    album_list.append(album.export_data())

                response['artist'] = artist.export_data()
                response['album_list'] = album_list

                return create_success_response(response)

        return create_error_response("No data found")

    except Exception as e:

        return create_error_response(str(e))


@music_bp.route('/getAlbum', methods=['GET'])
@login_required
def getAlbum():
    try:

        response = {}

        if 'id' in request.args:
            album = Album.query.get(int(request.args['id']))

            if album is not None:

                song_list = []

                songs = Song.query.filter_by(album_id=album.id)

                for song in songs:
                    userSong = User_Song.query.filter_by(User_Song.song_id == song.id).first()
                    song_list.append(song.export_data(userSong.user_id == g.user_id))

                response['album'] = album.export_data()
                response['song_list'] = song_list

                return create_success_response(response)

        return create_error_response("No data found")

    except Exception as e:

        return create_error_response(str(e))


@music_bp.route('/getSong', methods=['GET'])
def getSong():
    try:

        response = {}

        if 'id' in request.args:
            song = Song.query.get(int(request.args['id']))

            if song is not None:

                response['song'] = song.export_data()

                return create_success_response(response)

        return create_error_response("No data found")

    except Exception as e:

        return create_error_response(str(e))


@music_bp.route('/getUserSongList', methods=['GET'])
@login_required
def getUserSongList():
    try:
        song_list = []

        songs = User_Song.query.join(Song).add_columns(Song.name, Song.stream_url, Song.album_id, Song.id).filter(User_Song.user_id == g.user_id)

        for song in songs:
            album = Album.query.get(song.album_id)
            song_list.append({
                "id": song.id,
                "name": song.name,
                "stream_url": song.stream_url,
                "image_url": album.image_url
            })

        return create_success_list_response(song_list, 0)

    except Exception as e:

        return create_error_response(str(e))


@music_bp.route('/getHome', methods=['GET'])
def getHome():
    try:
        songs = Song.query.order_by(Song.id.desc()).limit(5)
        artists = Artist.query.order_by(Artist.id.desc()).limit(5)
        albums = Album.query.order_by(Album.id.desc()).limit(5)

        sl = []
        arl = []
        all = []

        for song in songs:
            sl.append(song.export_data())

        for artist in artists:
            arl.append(artist.export_data())

        for album in albums:
            all.append(album.export_data())

        return jsonify({
            "response": "success",
            "artists": arl,
            "albums": all,
            "songs": sl
        })

    except Exception as e:
        return create_error_response(str(e))