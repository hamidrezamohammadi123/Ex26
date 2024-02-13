"""  

Develop a basic Library Management System using Python and MySQL.
This system should handle the cataloging of books and the management of library users (members) and employees,
without the complexity of tracking book borrowings and returns(This program does not require lending or borrowing books).

1-User Management:Register new library members.Member loginShow profile details.
2-Employee Management:Add new employees.Show employee details.
3-Book Management:Add new books to the library catalog.Update book information (author, publication year, genre).
4-Search Functionality:Enable searching for books by title, author, or genre.

Attention:
The number and type of errors that could occur were very large, 
as a result, even though the program was simpler without using try, and I preferred to use it for all functions
so that I could check the errors that occur.

I installed mysql twice so that I can connect to it with python.

"""



import mysql.connector
from mysql.connector import Error


conn = mysql.connector.connect(
    host=    'localhost', 
    database='library', 
    user=    'root', 
    password='12345678')


cursor = conn.cursor()

#----------------------        Creating tables if not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name  VARCHAR(50),
    last_name   VARCHAR(50),
    username    VARCHAR(50) UNIQUE,
    password    VARCHAR(50)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Employee (
    emp_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name  VARCHAR(50),
    age        INT,
    gender     VARCHAR(10),
    salary     DECIMAL(10,2)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Book (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title   VARCHAR(100),
    author  VARCHAR(100),
    genre   VARCHAR(50),
    publication_year INT
)
''')

#------------------------------------   User class  ----------------------------------
class User:
    def __init__(self, user_id, first_name, last_name, username, password):
        self.user_id    = user_id
        self.first_name = first_name
        self.last_name  = last_name
        self.username   = username
        self.password   = password

    def register(self):     #---------------- New user
        try:
            cursor.execute('INSERT INTO User (first_name, last_name, username, password) VALUES (%s, %s, %s, %s)', (self.first_name, self.last_name, self.username, self.password))
            conn.commit()
            print("Registered successfully")
        except Error as e:
            print("Error:", e)

    def login(self):        #---------------- Check user           
        try:
            cursor.execute('SELECT user_id FROM User WHERE username = %s AND password = %s', (self.username, self.password))
            result = cursor.fetchone()
            if result:
                print("Logged in successfully")
                return result[0]
            else:
                print("Invalid Entry")
                return None
        except Error as e:
            print("Error:", e)

    def show_profile(self):   #---------------  Show user 
        try:
            cursor.execute('SELECT * FROM User WHERE user_id = %s', (self.user_id,))
            result = cursor.fetchone()
            if result:
                print("User ID:"   , result[0])
                print("First Name:", result[1])
                print("Last Name:" , result[2])
                print("Username:"  , result[3])
                print("Password:"  , result[4])
            else:
                print("User not found")
        except Error as e:
            print("Error:", e)

#------------------------------------   Employee class  ----------------------------------
class Employee:
    def __init__(self, emp_id, first_name, last_name, age, gender, salary):
        self.emp_id     = emp_id
        self.first_name = first_name
        self.last_name  = last_name
        self.age        = age
        self.gender     = gender
        self.salary     = salary

    def add_employee(self):     #---------------- New employee
        try:
            cursor.execute('INSERT INTO Employee (first_name, last_name, age, gender, salary) VALUES (%s, %s, %s, %s, %s)', (self.first_name, self.last_name, self.age, self.gender, self.salary))
            conn.commit()
            print("Added successfully")
        except Error as e:
            print("Error:", e)

    def show_employee(self):    #---------------  Show employee
        try:
            cursor.execute('SELECT * FROM Employee WHERE emp_id = %s', (self.emp_id,))
            result = cursor.fetchone()
            if result:
                print("Employee ID:", result[0])
                print("First Name:" , result[1])
                print("Last Name:"  , result[2])
                print("Age:"        , result[3])
                print("Gender:"     , result[4])
                print("Salary:"     , result[5])
            else:
                print("Employee not found")
        except Error as e:
            print("Error:", e)

#------------------------------------   Book class  ----------------------------------
class Book:
    def __init__(self, book_id, title, author, genre, publication_year):
        self.book_id = book_id
        self.title   = title
        self.author  = author
        self.genre   = genre
        self.publication_year = publication_year

    def add_book(self):    #---------------- New book
        try:
            cursor.execute('INSERT INTO Book (title, author, genre, publication_year) VALUES (%s, %s, %s, %s)', (self.title, self.author, self.genre, self.publication_year))
            conn.commit()
            print("Added successfully")
        except Error as e:
            print("Error:", e)

    def update_book(self): # ---------------  Update book 
        try:
            cursor.execute('UPDATE Book SET title = %s, author = %s, genre = %s, publication_year = %s WHERE book_id = %s', (self.title, self.author, self.genre, self.publication_year, self.book_id))
            conn.commit()
            print("Updated successfully")
        except Error as e:
            print("Error:", e)

    def show_book(self):   #---------------  Show book
        try:
            cursor.execute('SELECT * FROM Book WHERE book_id = %s', (self.book_id,))
            result = cursor.fetchone()
            if result:
                print("Book ID:", result[0])
                print("Title:"  , result[1])
                print("Author:" , result[2])
                print("Genre:"  , result[3])
                print("Publication Year:", result[4])
            else:
                print("Book not found")
        except Error as e:
            print("Error:", e)

    def search_book(self, option, query):  #---------------- Search book
        try:
            if option   == 'Title':
                cursor.execute('SELECT * FROM Book WHERE title LIKE %s', ('%' + query + '%',))
            elif option == 'Author':
                cursor.execute('SELECT * FROM Book WHERE author LIKE %s', ('%' + query + '%',))
            elif option == 'Genre':
                cursor.execute('SELECT * FROM Book WHERE genre LIKE %s', ('%' + query + '%',))
            else:
                print("Invalid option")
                return
            results = cursor.fetchall()
            if results:
                print("Search Results:")
                for result in results:
                    print("Book ID:", result[0])
                    print("Title:"  , result[1])
                    print("Author:" , result[2])
                    print("Genre:"  , result[3])
                    print("Publication Year:", result[4])
                    print()
            else:
                print("No books found")
        except Error as e:
            print("Error:", e)


# ----------------------------     main function  ---------------------------
#   It was possible to use tkinter to shrink the main body of the program,
#   but I preferred to go with the regular program
def main(): 

    print("Welcome to Library Management System")
    print("Please choose an option:")
    print("1. User Management")
    print("2. Employee Management")
    print("3. Book Management")
    print("4. Search Functionality")
    print("5. Exit")

    choice = input("Enter your choice: ")


    if choice == '1':   # --------------------------User management  -------------------------------
        print("User Management")
        print("Please choose an option:")
        print("1. Register new user")
        print("2. Login user")
        print("3. Show user profile")
        print("4. Back to main menu")
        option = input("Enter your option: ")
        if option == '1':   
            print("Register new user")
            first_name = input("Enter first name: ")
            last_name  = input("Enter last name: ")
            username   = input("Enter username: ")
            password   = input("Enter password: ")
            user       = User(None, first_name, last_name, username, password)
            user.register()
        elif option == '2': 
            print("Login user")
            username = input("Enter username: ")
            password = input("Enter password: ")
            user     = User(None, None, None, username, password)
            user_id = user.login()
            if user_id:
                user.user_id = user_id
        elif option == '3': 
            print("Show user profile")
            user_id = input("Enter user ID: ")
            user    = User(user_id, None, None, None, None)
            user.show_profile()
        elif option == '4':  
            print("Back to main menu")
        else:
            print("Invalid option")


    elif choice == '2':  # --------------------------  Employee management  -------------------
        print("Employee Management")
        print("Please choose an option:")
        print("1. Add new employee")
        print("2. Show employee details")
        print("3. Back to main menu")
        option = input("Enter your option: ")
        if option == '1':
            print("Add new employee")
            first_name = input("Enter first name: ")
            last_name  = input("Enter last name: ")
            age        = int(input("Enter age: "))
            gender     = input("Enter gender: ")
            salary     = float(input("Enter salary: "))
            employee   = Employee(None, first_name, last_name, age, gender, salary)
            employee.add_employee()
        elif option == '2':
            print("Show employee details")
            emp_id   = input("Enter employee ID: ")
            employee = Employee(emp_id, None, None, None, None, None)
            employee.show_employee()
        elif option == '3':
            print("Back to main menu")
        else:
            print("Invalid option")


    elif choice == '3':  # -----------------------------  Book management  -------------------------
        print("Book Management")
        print("Please choose an option:")
        print("1. Add new book")
        print("2. Update book information")
        print("3. Show book details")
        print("4. Back to main menu")
        option = input("Enter your option: ")
        if option == '1':
            print("Add new book")
            title  = input("Enter title: ")
            author = input("Enter author: ")
            genre  = input("Enter genre: ")
            publication_year = int(input("Enter publication year: "))
            book = Book(None, title, author, genre, publication_year)
            book.add_book()
        elif option == '2':
            print("Update book information")
            book_id = input("Enter book ID: ")
            title   = input("Enter title: ")
            author  = input("Enter author: ")
            genre   = input("Enter genre: ")
            publication_year = int(input("Enter publication year: "))
            book = Book(book_id, title, author, genre, publication_year)
            book.update_book()
        elif option == '3':
            print("Show book details")
            book_id = input("Enter book ID: ")
            book    = Book(book_id, None, None, None, None)
            book.show_book()
        elif option == '4':
            print("Back to main menu")
        else:
            print("Invalid option")


    elif choice == '4':   #----------------------------- Search functionality   ---------------------------------
        print("Search Functionality")
        print("Please choose an option:")
        print("1. Search by title")
        print("2. Search by author")
        print("3. Search by genre")
        print("4. Back to main menu")
        option = input("Enter your option: ")
        if option == '1':
            print("Search by title")
            query = input("Enter a title or part of it: ")
            book  = Book(None, None, None, None, None)
            book.search_book('Title', query)
        elif option == '2':
            print("Search by author")
            query = input("Enter an author or part of it: ")
            book  = Book(None, None, None, None, None)
            book.search_book('Author', query)
        elif option == '3':
            print("Search by genre")
            query = input("Enter a genre or part of it: ")
            book  = Book(None, None, None, None, None)
            book.search_book('Genre', query)
        elif option == '4':
            print("Back to main menu")
        else:
            print("Invalid option")


    elif choice == '5':   #--------------------------- Exit  -----------------------------
        print("Exit")
        return
    else:                 #------------------------Invalid choice-------------------------
        print("Invalid choice")
    main()  # Calling  again


#-----------------    main  body  --------------------------
main()

