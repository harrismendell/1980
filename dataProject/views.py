from flask import render_template, g, request, redirect, url_for, send_from_directory
from flask.ext.login import login_user,  logout_user, current_user, login_required
from dataProject import app
import pymysql
from models import insert_band, insert_user, User, get_bands, get_records, \
    get_songs, find_specific_band, get_more_songs, insert_song, remove_song, remove_band, insert_record, export_db
from pymysql import InternalError, IntegrityError


# routes
@app.route('/')
def title_screen():
    if current_user.is_anonymous():
        return redirect('/login')  
    return render_template('explore.html')


@app.route('/export')
def export():
    if current_user.is_anonymous():
        return redirect('/login')
    export_db()
    return render_template('confirm_export.html')

# routes
@app.route('/exploredb', methods=['post'])
def explore_db():
    if current_user.is_anonymous():
        return redirect('/login')
    return render_template('explore.html')

# routes
@app.route('/explore_bands')
def explore_bands():
    if current_user.is_anonymous():
        return redirect('/login')  
    return render_template('explore_bands.html')

# routes
@app.route('/band_submit', methods=['post'])
def band_submit():
    if current_user.is_anonymous():
        return redirect('/login')
    try:
        data = get_bands(request.form)
    except IntegrityError:
        return render_template('duplicate.html')
    if data == "si":
        return render_template('sql_injection.html')
    return render_template('explore_band_data.html', data=data)

# routes
@app.route('/record_submit', methods=['post'])
def record_submit():
    if current_user.is_anonymous():
        return redirect('/login')
    try:
        data = insert_record(request.form['band'], request.form['record_title'], request.form['release'])
    except IntegrityError:
        return render_template('duplicate.html')
    if data == "si":
        return render_template('sql_injection.html')
    return render_template('confirm.html', object=request.form['record_title'])

# routes
@app.route('/records/<band_name>', methods=['post'])
def records(band_name):
    if current_user.is_anonymous():
        return redirect('/login')

    data = find_specific_band(band_name)  
    records = get_records(band_name)
    return render_template('explore_records.html', data=data, records=records)

# routes
@app.route('/songs', methods=['post'])
def explore_from_songs():
    if current_user.is_anonymous():
        return redirect('/login')
    data = get_more_songs(request.form)
    if data == "si":
        return render_template('sql_injection.html')
    return render_template('explore_song_data.html', songs=data)

# routes
@app.route('/songs/<band_name>', methods=['post'])
def songs(band_name):
    if current_user.is_anonymous():
        return redirect('/login')

    data = find_specific_band(band_name)  
    songs = get_songs(band_name)
    return render_template('explore_song_data.html', data=data, songs=songs)

# routes
@app.route('/explore_songs')
def explore_songs():
    if current_user.is_anonymous():
        return redirect('/login')  
    return render_template('explore_songs.html')

# routes
@app.route('/song_submit', methods=['post'])
def song_submit():
    if current_user.is_anonymous():
        return redirect('/login')
    try:
        msg = insert_song(request.form)
    except IntegrityError:
        return render_template('duplicate.html')
    if msg == "good":
        return render_template('confirm.html', object=request.form['song'])
    if msg == "si":
        return render_template('sql_injection.html')
    elif msg == "invalid date":
        return render_template('fail.html', msg="Please enter a song with a release date between 1980 and 1989")


@app.route('/contribute')
def contribute():
    if current_user.is_anonymous() or (current_user.is_admin == 0):
        return render_template('admin.html')   
    return render_template('contribute.html')
     

@app.route('/contribute_band')
def contribute_band():
    if current_user.is_anonymous() or (current_user.is_admin == 0):
        return render_template('admin.html')   
    return render_template('contribute_band.html') 

@app.route('/contribute_record')
def contribute_record():
    if current_user.is_anonymous() or (current_user.is_admin == 0):
        return render_template('admin.html')   
    return render_template('contribute_record.html')

@app.route('/contribute_song')
def contribute_song():
    if current_user.is_anonymous() or (current_user.is_admin == 0):
        return render_template('admin.html')   
    return render_template('contribute_song.html')  

@app.route('/remove/<song>', methods=['POST'])
def remove_song_view(song):
    if current_user.is_anonymous() or (current_user.is_admin == 0):
        return render_template('admin.html')
    remove_song(song)   
    return render_template('confirm_delete.html', object=song) 

@app.route('/remove_band/<band>', methods=['POST'])
def remove_band_view(band):
    if current_user.is_anonymous() or (current_user.is_admin == 0):
        return render_template('admin.html')
    remove_band(band)   
    return render_template('confirm_delete.html', object=band) 

@app.route('/submit', methods=['POST'])
def submit():
    try:
        insert_band(request.form['band'], request.form['start'], request.form['end'], request.form['genre'])
    except IntegrityError:
        return render_template('duplicate.html')
    return render_template('confirm.html', object=request.form['band'])

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup/confirm', methods=['post'])
def signup_confirm():
    user = insert_user(request.form['username'], request.form['password'])
    login_user(user)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/check', methods=['post'])
def login_check():
    try:
        user = User.get(request.form['username'])
        if (user and user.password == request.form['password']):
            login_user(user)
        else:
            return redirect('/login')
    except KeyError:
        return redirect('/login')

    return redirect('/')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

# Auth stuff
@app.before_request
def db_connect():
    g.db = pymysql.connect(host='stardock.cs.virginia.edu',
                           user='cs4750hbm2qc',
                           passwd='cs47501980',
                           db='cs4750hbm2qc',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

@app.teardown_request
def db_disconnect(exception=None):
    g.db.close()