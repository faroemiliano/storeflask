from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#inicializar instancia de la aplicacion

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#inicio base de datos
db= SQLAlchemy(app)

#crear modelo base de datos 

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
   

# creo las rutas    
# pagina principal
@app.route('/') 
def index():
    return render_template('index.html')

#crear el producto
@app.route('/add_producto', methods=['GET','POST'])
def add_productos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        new_product = Producto(nombre=nombre, precio=precio, cantidad=cantidad)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('lista_productos'))
    return render_template('add_productos.html')

#catalogo de productos
@app.route('/lista_productos')
def lista_productos():
    productos = Producto.query.all()
    return render_template('lista_productos.html', productos=productos)


#update
@app.route('/update/<int:id>', methods=['GET','POST'] )
def update_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        producto.cantidad = request.form['cantidad']
        db.session.commit()
        return redirect(url_for('lista_productos'))
    return render_template('update_producto.html', producto = producto)


#elimina
@app.route('/delete/<int:id>')
def delete_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('lista_productos'))



if __name__ == '__main__':
    app.run(debug=True)