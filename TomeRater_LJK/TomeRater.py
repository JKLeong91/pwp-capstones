import re

class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = dict()

    def get_email(self):
        return self.email

    def change_email(self, email):
        # update the email
        self.email = email
        # notify the user
        print('User Email has been updated!')

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        return float(sum(self.books.values())/len(self.books.values()))

    def __repr__(self):
        return f'User {self.name}, email: {self.email}, books read: {len(self.books)}'

    def __eq__(self, other_user):
        return (self.name == other_user.name and self.email == other_user.email)

class Book(object):
    def __init__(self, title, isbn, price):
        self.title = title # a string 
        self.isbn = int(isbn) # an integer
        self.ratings = list() # a list type
        self.price = price

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def get_price(self):
        return self.price

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print(f'This book\'s ISBN has been updated to {self.isbn}')

    def add_rating(self, rating):
        if 0 <= rating <= 4:
            self.ratings.append(rating)
            print('Rating has been updated. ')
        else:
            print("Invalid Rating.")
    
    def get_average_rating(self):
        total_rating = 0
        for rating in self.ratings:
            total_rating += rating
        return total_rating / len(self.ratings)

    def __repr__(self):
        return f'{self.title } ISBN: {self.isbn}'


    def __eq__(self, other_book):
        return (self.title == other_book.title and self.isbn == other_book.isbn)

    def __hash__(self):
        return hash((self.title, self.isbn))
 

class Fiction(Book):
    def __init__(self, title, author, isbn, price):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return f'{self.title} by {self.author}'


class Non_Fiction(Book):

    def __init__(self, title, subject, level, isbn, price):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return f'{self.title}, a {self.level} manual on {self.subject}'

class TomeRater(object):
    def __init__(self):
        self.users = dict()
        self.books = dict()
        
    def create_book(self, title, isbn, price):
        return Book(title, isbn, price)

    def create_novel(self, title, author, isbn, price):
        return Fiction(title, author, isbn, price)

    def create_non_fiction(self, title, isbn, subject, level, price):
        return Non_Fiction(title, isbn, subject, level, price)

    def add_book_to_user(self, book, email, rating=None):
        if not email in self.users:
            print(f'No user with email {email} !')
        else:
            if rating is None:
                rating = 0

            user = self.users[email]
            user.read_book(book, rating)
            book.add_rating(rating)

        if book not in self.books:
            self.books[book] = 1
        else:
            self.books[book] += 1

    def add_user(self, name, email, user_books=None):
        # check if user already exists
        if email in self.users:
            print('User already exists')
            return

        # check for valid email
        if not re.match(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', email, re.I):
            print('Invalid email address !')
            return 

        user_object = User(name, email)
        self.users[email] = user_object
        if user_books:
            for book in user_books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        print('--- Catalog ---')
        for book in self.books:
            print(book)
        print()

    def print_users(self):
        print('--- Users ---')
        for user in self.users.values():
            print(user)
        print()

    def most_read_book(self):
        return max(self.books, key=self.books.get)

    def highest_rated_book(self):
        return max(self.books, key=lambda x: x.get_average_rating())

    def most_positive_user(self):
        return max(self.users.values(), key=lambda x: x.get_average_rating())

    def most_expensive_book(self):
        return max(self.books, key=lambda x: x.price)

    def get_n_most_read_books(self, n):
        return sorted(self.books, key=self.books.get, reverse=True)[:n]

    def get_n_most_prolific_readers(self, n):
        return sorted(self.users, key=lambda x: len(self.users.get(x).books), reverse=True)[:n]
        
    def get_n_most_expensive_books(self, n):
        return sorted(self.books, key=lambda x: x.price, reverse=True)[:n]

    def get_worth_of_user(self, user_email):
        if not user_email in self.users:
            print('The user with that email does not exists!')
            return
        return sum([book.price for book in self.users[user_email].books])
        #return sum(user_books.price for book in self.users[user_email])

    def __str__(self):
        output = '------ Users -----\n'
        for user in self.users:
            output += f'{user}\n'

        output +=  '\n------ Books -----\n'
        for book in self.books:
            output += f'{book}\n'
        return output

    def __eq__(self, other_tomrate):
        return self.users == other_tomrate.users and \
            self.books == other_tomrate.books