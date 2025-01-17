from flask import Blueprint, render_template
from flask import request
from flask import url_for
from flask import redirect
from models import Post
from .forms import PostForm
from app import app,db

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
def post_create():
  form = PostForm()
  
  if request.method == 'POST':
    title = request.form.get('title')
    body = request.form.get('body')
    
    try:
      post = Post(title=title, body=body)
      
      db.session.add(post)
      db.session.commit()
    
    except:
      print('Traceback')
    
    return redirect(url_for('posts.post_detail', slug=post.slug))
      
  return render_template('posts/post_create.html', form=form)
  

#localhost:5000/blog/
@posts.route('/')
def posts_list():
  
  q= request.args.get('q')
  
  if q:
    posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    
  else:
    posts = Post.query.order_by(Post.created.desc())
    
  page = request.args.get('page')
  
  if page and page.isdigit():
    page = int(page)
  
  else:
    page = 1

  pages = posts.paginate(page=page, per_page=3)
    
  return render_template('posts/posts.html', posts=posts, pages=pages) 

#localhost:5000/blog/first-post
@posts.route('/<slug>')
def post_detail(slug):
  post = Post.query.filter(Post.slug==slug).first()
  return render_template('posts/post_detail.html', post=post) 


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
def post_update(slug):
  post = Post.query.filter(Post.slug==slug).first()
  
  if request.method == 'POST':
    form = PostForm(formdata=request.form, obj=post)
    form.populate_obj(post)
    db.session.commit()
    return redirect(url_for('posts.post_detail', slug=post.slug))
  form=PostForm(obj=post)
  return render_template('posts/edit.html', post=post, form=form)