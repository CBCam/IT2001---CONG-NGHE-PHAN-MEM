from flask import render_template, request, redirect
from saleapp import dao, app, login
from flask_login import login_user
from saleapp import admin


@app.route("/")
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = dao.load_products(cate_id=cate_id, kw=kw)
    return render_template('index.html', products=products)


@app.route('/login-admin', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.context_processor
def common_attr():
    categories = dao.load_categories()
    return {
        'categories': categories
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/products/<int:product_id>')
def details(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


if __name__ == '__main__':
    app.run(debug=True)