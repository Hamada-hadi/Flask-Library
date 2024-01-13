from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, reader_schema, readers_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'hello': 'reader'}

@api.route('/books', methods = ['POST'])
@token_required
def create_reader(current_user_token):
    title = request.json['title']
    isbn = request.json['isbn']
    pages = request.json['pages']
    auther = request.json['auther']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    contact = Book(title, isbn, pages, auther, user_token = user_token )

    db.session.add(contact)
    db.session.commit()

    response = reader_schema.dump(contact)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = readers_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_reader_two(reader_user_token, id):
    fan = reader_user_token.token
    if fan == reader_user_token.token:
        book = Book.query.get(id)
        response = reader_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_reader(current_user_token,id):
    book = Book.query.get(id) 
    book.title = request.json['title']
    book.isbn = request.json['isbn']
    book.pages = request.json['pages']
    book.auther = request.json['auther']
    book.user_token = current_user_token.token

    db.session.commit()
    response = reader_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_reader(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = reader_schema.dump(book)
    return jsonify(response)










