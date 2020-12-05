# CS50-Final-Project: Data Tabulation and Plotter Web Application

This project is a web application designed for data viewing. You are able to upload files onto your user account
and then able to access this data in the form of a table or graph. The reason I chose such a project is
due to me having a physics background. Given that the context I would most likely to use programming in the
future will be analytical, I want to work on projects that will lend to that. Furthermore, I chose to go with
a web app as it allows me to explore a wide range of tools, and I would like to eventually build a web
application suitable for deployment.

## Technologies and Frameworks Used

- HTML5, CSS, Javascript
- Python and required packages
- Flask and required extenstions
- SQLite

## How does the web app work?

The main idea is that you can upload data files to the server which are connected to your user account via a sqlite3
database. You can retrive these files, and display them in the form of a table, and if the data is suitable, also plot
them in the form of a graph.

### Usage Instructions

- You cannot operate on the site without a user account so first a user account must be created which can be done by clicking the register link
in either the prompt or navbar.
- After creating your account, you can upload your files through the upload link in the navbar.
- These files can be accesed through the uploads link where you will see all the files you have uploaded.
- Clicking the analyse button gives you a preview table and allows you to take actions such as tabulating and plotting the data.
- The scatter plot has an advanced option, which allows you to do linear and quadratic fitting on the data.

### More Details

- User System: The user system is based on flask-wtf and flask-login, with data stored in a sqlite database, passwords are hashed and salted before storage and usernames are
               unique.
- Routing: Outside the homepage, registration and login pages all the routes are authenticated, and cannot be accessed by users not logged in. 
- Forms: All user input is collected through forms. To prevent users from accessing other users files and information all requests are posted as a minimal security measure
         and files may be only accesed through a user's own uploads page. Any attempts otherwise will be redirected.
- Database: Two databases are maintained, one which contains all users, and another which contains all uploaded files, connected to the users table by a foreign key.
- Uploads: Uploads are stored in hardcoded local folder, with username appended to files to prevent files with the same replacing another user's files. There are
           restrictions on the uploads, through valdidators and configuaration.
- Validation: Various validators are used, through both flask-wtf and manual validation, errors not handled by the browser are displayed at the bottom of the page.
 
## Future Improvements

- More security measures.
- File deletion needs to be implemented.
- File handling needs to be improved and extended.
- Plotting is done through conversion of matplotlib plot to base64 string, which is not ideal.
- More data analysis tools can be added.
- Design is not suitable for deployment; It needs a complete overhaul.

## Launching the application

 Clone the code or download, navigate to the folder in your prompt

### If Using Conda

- Create a new environment with the required packages from the yml file using the following command

    `conda env create -f freeze.yml`
    
- Activate the environment

    `conda activate cs50finaltabulationandplotterapp`
    
- The app can now be freely run and accessed at http://localhost:5000/

    `flask run`
    
### Otherwise

- will be updated in the future, but the requirements conda file should work with pip as well, install dependencies in both requirements files.






