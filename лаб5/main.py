from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/api/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        items = Item.query.all()
        items_list = [{'id': item.id, 'name': item.name} for item in items]
        return jsonify(items_list)

    elif request.method == 'POST':
        data = request.get_json()
        new_item = Item(name=data['name'])
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item created successfully'}), 201


@app.route('/api/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_item(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == 'GET':
        return jsonify({'id': item.id, 'name': item.name})

    elif request.method == 'PUT':
        data = request.get_json()
        item.name = data['name']
        db.session.commit()
        return jsonify({'message': 'Item updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)