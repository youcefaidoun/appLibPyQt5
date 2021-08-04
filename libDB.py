import datetime

from peewee import *


db = SqliteDatabase('libDB.db')

BOOK_STATUS=(
    (1,"New"),
    (2,"User"),
    (3,"Damaged"),
    )
class Category(Model):
    category_name = CharField(unique=True)
    parent_category = IntegerField(null=True) #recursive relationship
    class Meta:
        database = db

class Author(Model):
    name = CharField(unique=True)
    location = CharField(null=True)
    class Meta:
        database = db

class Publisher(Model):
    name = CharField(unique=True)
    location = CharField(null=True)
    class Meta:
        database = db

class Books(Model):
    title = CharField(unique=True)
    description = TextField(null=True)
    category = ForeignKeyField(Category , backref="category", null=True)
    code = CharField(null=True)
    barcode = CharField()
    #parts
    part_order = IntegerField(null=True)
    price = DecimalField(null=True)
    publisher = ForeignKeyField(Publisher , backref="publisher", null=True)
    author = ForeignKeyField(Author , backref="author" ,null=True)
    image = CharField(null=True)
    status = CharField(choices=BOOK_STATUS) #choices
    date = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db

class Clients(Model):
    name = CharField()
    mail = CharField(null=True , unique=True)
    phone = CharField(null=True)
    date = DateTimeField(default=datetime.datetime.now)
    national_id = IntegerField(null=True ,unique=True)
    class Meta:
        database = db

class Employee(Model):
    name = CharField()
    mail = CharField(null=True ,unique=True)
    phone = CharField(null=True)
    branch = IntegerField()
    date = DateTimeField(default=datetime.datetime.now)
    national_id = IntegerField(null=True ,unique=True)
    periority = IntegerField(null=True)
    password = CharField()
    class Meta:
        database = db

class Branch(Model):
    name = CharField()
    code = CharField(null=True ,unique=True)
    location = CharField(null=True)
    class Meta:
        database = db

PROCESS_TYPE =(
    (1,"Rent"),
    (2,"Retrieve")
    )
class Daily_Mouvements(Model):
    book =  ForeignKeyField(Books , backref="book")
    client = ForeignKeyField(Clients , backref="book_client")
    type = CharField(choices=PROCESS_TYPE)   #[rent - retrieve]
    date = DateTimeField(default=datetime.datetime.now)
    branch =  ForeignKeyField(Branch , backref="Daily_branch" ,null=True)
    book_from = DateField(null=True)
    book_to = DateField(null=True)
    employee = ForeignKeyField(Employee , backref="Daily_employee", null=True)
    class Meta:
        database = db

class History(Model):
    employee = ForeignKeyField(Employee , backref="History_employee")
    actions = CharField()
    tables = CharField()
    date = DateTimeField(default=datetime.datetime.now)
    branch = ForeignKeyField(Branch , backref="History_branch", null=True)
    class Meta:
        database = db
class Permission(Model):
    employee_name = CharField()
    books_tab = IntegerField()
    clients_tab = IntegerField()
    dashboard_tab = IntegerField()
    history_tab = IntegerField()
    reports_tab = IntegerField()
    settings_tab = IntegerField()

    add_book = IntegerField()
    edit_book = IntegerField()
    delete_book = IntegerField()
    import_book = IntegerField()
    export_book = IntegerField()

    add_client = IntegerField()
    edit_client = IntegerField()
    delete_client = IntegerField()
    import_client = IntegerField()
    export_client = IntegerField()

    add_branch = IntegerField()
    add_publisher = IntegerField()
    add_auther = IntegerField()
    add_category = IntegerField()
    add_employee = IntegerField()
    edit_employee = IntegerField()

    is_admin = IntegerField()
    class Meta:
        database = db

db.connect()
db.create_tables([Category,Author,Publisher,Books,Clients,Employee,Branch,Daily_Mouvements,History,Permission])
