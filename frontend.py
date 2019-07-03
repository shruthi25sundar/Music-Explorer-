from flask import Flask, request, session, render_template, redirect, url_for, flash, send_file
import os
from functools import wraps
from App import main as mnclass

app = Flask(__name__)

app.secret_key = os.urandom(24)
app.config['SECRET_KEY'] = 'thisisthesecretkeyforhousepriceprediction'


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            return redirect(url_for('search_album_detail'))
        return render_template('example-2.html', error="Invalid Credentials!!")
    if request.method == 'GET':
        # This is the login page.
        return render_template('example-2.html')


@app.route('/search_album_detail', methods=['GET', 'POST'])
@login_required
def search_album_detail():
    if request.method == 'GET':
        return render_template('example-3.html')
    if request.method == 'POST':
        tm_nm = request.form['search']
        if len(tm_nm) == 0:
            return render_template('example-3.html', error="Please enter Album name to be searched!!")
        try:
            result = mnclass.MainFun.team_search(tm_nm)
            return render_template('example-3.html',
                                   mssg=True,
                                   len=len(result['album']),
                                   album=result['album'],
                                   artist=result['artist'],
                                   runtime=result['runtime'],
                                   genre=result['genre'],
                                   composer=result['composer'],
                                   releasedate=result['releasedate'],
                                   description=result['description'],
                                   result=result)
        except:
            return render_template('example-3.html', error="Please enter a valid Album name!")


@app.route('/ArtistInfo', methods=['GET', 'POST'])
@login_required
def ArtistInfo():
    if request.method == 'GET':
        return render_template('example-1.html')
    if request.method == 'POST':
        artist_name = request.form['search']
        if len(artist_name) == 0:
            return render_template('example-1.html', error="Please enter Artist name to be searched!")
        else:
            try:

                result = mnclass.MainFun.SearchArtist(artist_name)
                return render_template('example-1.html',
                                       mssg=True,
                                       name=result['name'],
                                       genre=result['genre'],
                                       dob=result['dob'],
                                       Desc=result["Desc"],
                                       image=result["image"],
                                       cntry=result['cntry'].split("_")[0],
                                       externalLink=result['cntry'])
            except IndexError:
                return render_template('example-1.html', error="Please enter a valid Artist name (e.g. Barry)")
            except:
                return render_template('example-1.html', error="Something wrong - try for another artist")


@app.route('/pl_search/<pl_nm>', methods=['GET', 'POST'])
@login_required
def pl_search(pl_nm):
    if request.method == 'GET':
        try:
            result = mnclass.MainFun.SearchArtist(pl_nm)
            return render_template('example-1.html',
                                   mssg=True,
                                   name=result['name'],
                                   genre=result['genre'],
                                   dob=result['dob'],
                                   Desc=result["Desc"],
                                   image=result["image"],
                                   cntry=result['cntry'].split("_")[0],
                                   externalLink=result['cntry'],
                                   )
        except IndexError:
            return render_template('example-1.html', error="Please enter a valid Artist name (e.g. Barry)")
        except:
            return render_template('example-1.html', error="Something wrong - tyr for another artist")

    if request.method == 'POST':
        artist_name = request.form['search']
        if len(artist_name) == 0:
            return render_template('example-1.html', error="Please enter Artist name to be searched!")
        else:
            try:
                result = mnclass.MainFun.SearchArtist(artist_name)
                return render_template('example-1.html',
                                       mssg=True,
                                       name=result['name'],
                                       genre=result['genre'],
                                       dob=result['dob'],
                                       Desc=result["Desc"],
                                       image=result["image"],
                                       cntry=result['cntry'].split("_")[0],
                                       externalLink=result['cntry'],
                                       )
            except IndexError:
                return render_template('example-1.html', error="Please enter a valid Artist name (e.g. Barry)")
            except:
                return render_template('example-1.html', error="Something wrong - tyr for another artist")


@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    return render_template('example-2.html')


@app.route('/report_pdf')
def report_pdf():
    return send_file('files/Report.pdf',
                     mimetype='text/csv',
                     attachment_filename='Report.pdf',
                     as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
