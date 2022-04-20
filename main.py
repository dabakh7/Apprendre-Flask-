from flask import Flask,render_template
# from mocks import Post
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy





 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

conn = psycopg2.connect(
    host="localhost",
    database="suppliers",
    user="postgres",
    password="Dabakh7")

class Post(db.Model):
    __tablename__='posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)

    def __repr__(self):
        return '<Post "{}">'.format(self.title) ##pour l'affichage détaillé des posts


###Pour gérer les pluriels

@app.context_processor
def utility_processor():
    def pluralize(count, singular, plural=None):
        if not isinstance(count, int):
            raise ValueError('"{}" must be an integer'.format(count))

        if plural is None:
            plural = singular + 's'

        if count == 1:
            string = singular
        else:
            string = plural

        return "{}{}".format(count, string)

    return dict(pluralize=pluralize)

##Pour générer une date dans le footer

@app.context_processor
def inject_now():
    return {'now' : datetime.now()}


@app.route('/') #permet d'ajouter des métadonnés
def home():
    return render_template('pages/home.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/contact')
def contact():
    return render_template('pages/contact.html')

@app.errorhandler(404)
def erreur_not_found(error):
    return render_template('erreurs/404.html'),404

##pour indexer pous les posts
@app.route('/blog')
def posts_index():
    posts = Post.all()
    return render_template('posts/index.html',posts=posts)

@app.route('/blog/posts/<int:id>')
def posts_show(id):
    # post = posts[id-1]
    post = Post.find(id)
    return render_template('posts/show.html', post=post)


###Fonction qui crée la connection
# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn

if __name__=='__main__': ###il permet de dire que si on execute ce qui en bat qu'il fasse c qui suit
    db.create_all()
    app.run(debug=True)
