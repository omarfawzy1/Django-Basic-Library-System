# Borrowing Library System
This is a simple borrowing library system built with Django and Python, using a SQLite database to store books information. It allows users to search for books, borrow them for a specific period of time, and return them. The system also has an admin page for managing books in the library.

## Features
Search for books by title, author, or ISBN. <br>
Borrow books for a specific period of time. <br>
Return books. <br>
Admin page for managing books in the library. <br>
## Screenshots
### Home screen
![Screenshot_20230307_041113](https://user-images.githubusercontent.com/60580509/223557651-fef804dd-7396-4525-9d59-8e1762602b12.png)

### Sign in page
![Screenshot_20230307_040741](https://user-images.githubusercontent.com/60580509/223557665-1db256ce-2132-4bf7-8610-fc3b8a53372d.png)

### Book information page
![Screenshot_20230307_041206](https://user-images.githubusercontent.com/60580509/223557744-41d052b1-9278-4219-88d5-395a4b9ce63f.png)

## How to Use
Clone the repository. <br>
Create a virtual environment and activate it. <br>
Install the dependencies from the requirements file: pip install -r requirements.txt <br>
Run the migrations: python manage.py migrate <br>
Create a superuser account to access the admin page: python manage.py createsuperuser <br>
Start the development server: python manage.py runserver <br> 
Open the app in your browser: http://localhost:8000 <br>

