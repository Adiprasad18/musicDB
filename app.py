from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'  # For flashing messages
db = SQLAlchemy(app)

# Models
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        if title and artist:
            new_song = Song(title=title, artist=artist)
            db.session.add(new_song)
            db.session.commit()
            flash('Song added successfully!')
            return redirect(url_for('add_song'))
        else:
            flash('Both title and artist are required.')
    return render_template('add_song.html')

@app.route('/view_songs')
def view_songs():
    songs = Song.query.all()
    return render_template('view_songs.html', songs=songs)

@app.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        if name:
            new_playlist = Playlist(name=name, description=description)
            db.session.add(new_playlist)
            db.session.commit()
            flash('Playlist created successfully!')
            return redirect(url_for('create_playlist'))
        else:
            flash('Playlist name is required.')
    return render_template('create_playlist.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
