from sqlalchemy import create_engine,Column , String , Integer , ForeignKey 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.exc import IntegrityError


#create DataBase
engine = create_engine('sqlite:///database.db',echo=False)
Base= declarative_base()
Session=sessionmaker(bind=engine)
session=Session()


#models


class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True)
    name = Column(String , nullable=False)
    email = Column(String , nullable=False , unique=True)
    tasks = relationship('Task', back_populates='user',cascade='all, delete-orphan')
    
class Task(Base):
    __tablename__='tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='tasks')

Base.metadata.create_all(engine)


# Utils

def get_user_by_email(email):
    return session.query(User).filter_by(email=email).first()

def confirm_action(prompt) -> bool:
    while True:
        choice = input(prompt + " (y/n): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")



# Cruds Querry 
def add_user():
    name = input("Enter user name: ")
    email = input("Enter user email: ")
    if get_user_by_email(email):
        print("Email already exists. Please choose a different email.")
        return
    try:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        print(f"User added {name} successfully.")
    except IntegrityError:
        session.rollback()
        print(f"Error!")
        
        
def add_task():
    email = input("Enter user email: ")
    user = get_user_by_email(email)
    if not user:
        print("User not found.")
        return
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    try:
        task = Task(title=title, description=description, user=user)
        session.add(task)
        session.commit()
        print(f"Task added successfully.{title} - {description}")
    except IntegrityError:
        session.rollback()
        print("Error!")
        

def get_users():
    for user in session.query(User).all():
        print(f'ID:{user.id} , name : {user.name} , email : {user.email}')

def get_tasks():
    for task in session.query(Task).all():
        print(f'ID:{task.id}, title : {task.title}, description : {task.description}, user_id : {task.user_id}')

def get_user_task():
    user = input("enter email of user :")
    user = get_user_by_email(user)
    if not user:
        print("User not found.")
        return
    for task in user.tasks:
        print(f'ID:{task.id}, title : {task.title}, description : {task.description}, user_id : {task.user_id}')

def update_user():
    email = input("Enter user email: ")
    user = get_user_by_email(email)
    if not user:
        print("User not found.")
        return
    name = input("Enter new user name: ")
    email = input("Enter new user email: ")
    try:
        user.name = name
        user.email = email
        session.commit()
        print(f"User updated successfully.")
    except IntegrityError:
        session.rollback()
        print("Error!")

def delete_user():
    email = input("Enter user email: ")
    user = get_user_by_email(email)
    if not user:
        print("User not found.")
        return
    if confirm_action("Are you sure you want to delete this user?"):
        session.delete(user)
        session.commit()
        print("User deleted successfully.")
    else:
        print("Operation cancelled.")   

def delete_task():
    task_id = input("Enter task ID: ")
    task = session.query(Task).filter_by(id=task_id).first()
    if not task:
        print("Task not found.")
        return
    if confirm_action("Are you sure you want to delete this task?"):
        session.delete(task)
        session.commit()
        print("Task deleted successfully.")
    else:
        print("Operation cancelled.")

def main() ->None:
    actions ={
        '1':add_user ,
        '2':add_task ,
        '3':get_user_task,
        '4':get_users,
        '5':get_tasks,
        '6':update_user,
        '7':delete_user
    }
    
    while True:
        print("\n 1.add_user \n 2.add_task \n 3.get_user_task \n 4.get_users \n 5.get_tasks \n 6.update_user \n 7.delete_user \n 8.delete_task \n 9.exit")
        choice = input("Enter your choice: ")
        if choice =='9':
            print('bye bye')
            break
        action=actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please try again.")

main()
