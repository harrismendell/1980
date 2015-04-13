from flask import render_template, g, request, redirect
from flask.ext.login import login_user,  logout_user, current_user, login_required
from dataProject import app
import pymysql
from models import insert_band, insert_user, User, get_bands, get_records, get_songs, find_specific_band, get_more_songs, insert_song


# routes
@app.route('/')
def title_screen():
    if current_user.is_anonymous():
        return redirect('/login')  
    return render_template('explore.html')

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
    data = get_bands(request.form)
    return render_template('explore_band_data.html', data=data)

# routes
@app.route('/records/<band_name>', methods=['post'])
def records(band_name):
    if current_user.is_anonymous():
        return redirect('/login')

    data = find_specific_band(band_name)  
    records = get_records(band_name)
    return render_template('explore_records.html', data=data, records=records)

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
    insert_song(request.form)
    return render_template('confirm.html', object=request.form['song'])

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

@app.route('/submit', methods=['POST'])
def submit():
    insert_band(request.form['band'], request.form['start'], request.form['end'], request.form['genre'])
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