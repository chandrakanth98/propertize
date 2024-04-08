# propertize

Propertize is a property management software designed to simplify interactions between landlords and tenants. It provides all necessary information about owned properties and their tenants in a simple and easy-to-use manner.

Simply put, Propertize helps you prioritize the right things.
#### [Live demo page](https://propertize-unique-f40dd5b3e2d4.herokuapp.com/)


![Responsive Mockup](/static/img/readme/all-devices-black.png)




# Features


### Landlord

- ___Dashboard___
    - Widgets displaying:
        - Rent income
        - Overdue rent
        - Unpaid Invoices
        - Unpaid expenses
    - Latest Tenant Requests
        - Offers immediate insight into tenant maintenance requests.
    - Latest Property Notices
        - Displays the most recent notices posted for landlords properties.
    - Lates Invoices
        - Overview of latest transactions to help with catching discrepensies

![Dashboard](/static/img/readme/dashboard.png)


- ___Properties___
    - Overview of owned properties and ability to add new properties.

![Properties page](/static/img/readme/properties.png)


- ___Property___
    - Property overview containing a table with all property tenants
    - Ability to post notices that can be seen by all tenants
        - Mark notice as Important to make it stand out in red
    - Edit property
        - Change information or property picture.

![Property page](/static/img/readme/property.png)


- ___Tenants___
    - Searchable table containing all tenants to easily find and modify tenants.
    - Tenant profile showing all their information
        - Contact information
        - Ability to edit lease data including rent, grace periods, overdue fees and more.
        - Overview of their latest invoices and maintenance requests

![Tenants table](/static/img/readme/tenants.png)

- ___Invitation Codes___
    - Simplifies tenant/contractor assignment by providing a one-use code.
        - Automatically assigns all relevant data after entering code.
    - Tenant code creator
        - Create codes with individualized data including rent amount, lease end, property and Apt. #
    - Contractor code creator
        - Create codes containing the properties the contractor will work at.

![Invitation codes](/static/img/readme/tenant_code.png)

- ___Maintenance___
    - Requests
        - Organizes all open requests in a easy to use overview.
            - Categorizes requests as Submitted, In-progress, or Urgent.
        - Clickable request card
            - Individual request page containing all contact information and notes
            - Option to edit request status, notes and assigned contractor.
        - Searchable table with all past and current requests
    - Contractors
        - Searchable table listing all contractors
        - Functionality for creating contractor codes as mentioned earlier.

![Maintenance page](/static/img/readme/maintenance.png)


- ___Finances___
    - Rent invoices
        - Generates invoices for all active tenants monthly, based on their profile data.
        - Ensures other invoices can exist without stopping rent invoice generation
        - Manages overdue invoices with tenant specific grace periods and fees.
        - Sets due dates to month-end on invoices and updates tenants "Next Rent Due" to the next month.
        ##### NOTE: Due to heroku idling all workers after 30min of inactivity the schedule i have setup in the backend wont succeed with running the task.
        ##### To work around this for demo purposes the function to generate invoices can be manually triggered by visiting the transactions page.

![Invoice page](/static/img/readme/invoice.png)
    - Transactions
        - Searchable table listing all transactions
        - Invoice
            - Individual Invoice pages showing all invoice information
            - Includes functionality to edit invoices, mark them as paid, or void them.
    - Create invoices
        - Create invoice and assign it to a user
        - Create expense invoice
            - Create external expense to help with bookkeeping or P/L purposes

![Transaction page](/static/img/readme/transactions.png)


## Tenant

- ___Profile___
    - Contact information card
        - Displays contact details
        - Ability to edit information

    - Assigned Property Information Card:
        - Shows property photo and address information
    - Lease Information and Latest Invoices Card
        - Color coded invoice status
        - Open invoice by clicking it
    - Property Contact Information and Latest Maintenance Requests Card
        - Color coded request status
        - Open maintenance request by clicking it

![Profile page](/static/img/readme/profile.png)
- ___Transactions___
    - Searchable table listing all transactions
        - Individual Invoice pages showing all invoice information
        - Button to pay transaction now ***Not yet implemented
- ___Property___
    - Property Details
    - Property Description
    - Property contact information
    - List view with property notices
        - Ordered with newest at the top
        - Important notices color coded red

![Tenant property page](/static/img/readme/propertytenant.png)

- ___Maintenance___
    - Create maintenance request
        - Specify location
        - Add detailed description
        - Mark as urgent
    - List view showing all tenant maintenance requests
        - Click card to go to individual request page
            - Edit description
            - Cancel request if it's not in progress
            - Card showing contact information to tenant and assigned contractor
            - See contractor note if it exists
            - See scheduled date after the contractor has set it

![Tenant requests page](/static/img/readme/requests.png)
![Individual request](/static/img/readme/indrequest.png)


## Contractor

- ___Maintenance___
    - Requests
        - Organizes all open requests in a easy to use overview.
            - Categorizes requests as Submitted, In-progress, or Urgent.
        - Clickable request card
            - Individual request page containing all contact information and notes
            - Option to edit request status, notes and assigned contractor.
        - Searchable table with all past and current requests
    - Individual request page
        - Displays information
            - Displays tenant submitted information
            - Shows contact information to both
            - Property information
            - Scheduled date
        - Ability to edit request and add contractor note, change status and set scheduled date

![Contractor edit form](/static/img/readme/editreq.png)
    
- ___Properties___
    - Overview of all assigned properties
    - Property page
        - Property Details
        - Property Description
        - Property contact information
        - List view with property notices
            - Ordered with newest at the top
            - Important notices color coded red

    




## Upcoming Features
 ___propertize v2___
- Complete design overhaul
    - Currently its a simple bootstrap site that doesnt stand out in any way
    

- Ability to pay invoices
    - Pay invoices through stripe's portal and have invoice marked as paid

- Document handling
    - Upload lease or important documents to tenant profile.
- Direct Messaging
    - Enables tenants to send and receive messages to/from the landlord and contractor.
    - Allows landlords and contractors to communicate with tenants.




## Idea


This idea began as a means for big company property owners to assign property and tasks to their workers. Having firsthand experience with such a platform, I knew the concept could be improved upon greatly. As planning progressed, it transformed into a comprehensive property management platform, with a stronger focus on improving the partnership between landlords and tenants.

In all the places I've lived, systems for rent invoices, maintenance requests, and property notices have been terrible. Drawing from my experiences as a tenant and contractor, I built upon those insights to develop functionalities tailored for the landlord.



# Planning

## Website owners goals


- Develop a comprehensive property management platform
- Enhance landlord-tenant partnerships by addressing common problems
- Simplify maintenance requests for tenants and contractors


## User Goals

- Easily manage rental properties and interactions with tenants.
- Access property information and tenant details easily.
- Submit and track maintenance requests with clear status.
- Help contractors efficiently handle maintenance requests


## Following user stories was implemeneted in the project:


-As a user, I want to create a profile with role-based access, so I can interact with the platform according to my role.
-As a landlord, I want a dashboard to manage my properties, tenants, and related information effectively.
-As a tenant, I want to submit maintenance requests easily, providing details, and urgency levels.
-As a landlord, I want to prioritize and assign contractors to maintenance requests efficiently.
-As a landlord, I want to track rental income, expenses, and tenant rent payments for each property.
-As a tenant, I want to view rent payment history, due dates, and amounts owed conveniently.
-As a landlord or contractor, I want to post important messages and updates for tenants to stay informed.

[Github Projects](https://github.com/users/zimmoc/projects/2/views/1)




<hr>

___Proof of Concept___
- User Profiles and Role-Based Dashboards:
    - Implement user profile creation with role-based dashboards for different user types such as landlords, tenants, and contractors.

- Property Management for Landlords:
    - Develop functionalities to enable landlords to efficiently manage their properties, tenants, and related information, including rent agreements, payments, and tenant details.

- Maintenance Request System:
    - Create a system allowing tenants to submit maintenance requests with detailed descriptions, and urgency level.
    - Implement features for landlords to assign priority to requests and allocate contractors for resolution.
    - Enable contractors to view assigned requests, update their status, and schedule property visits.

- Contractor Management:
    - Develop features for contractors to mark requests as in-progress, add estimated visit dates, and update status upon completion.
    - Allow contractors to attach invoices, receipts for expenses, and input hours with additional notes upon completing tasks.

___Minimum Viable Product___
- Financial Tracking:
    - Implement functionality for landlords to track rental income, expenses, and tenant rent payments for each property.
    - Include reminders for late payments, and allow landlords to add late fees if necessary.

- Tenant Financial Management:
    - Develop a tenant financial portal allowing tenants to view rent payment history, due dates, and amounts owed.

- Message Board and Communication:
    - Implement a message board where landlords and contractors can post important information.
    - Include the option to tag urgent messages.

## Project structure
___App Structure___
- Users App:
    - Implement a custom user model within its own app to manage user authentication and permissions.

- User Management App:
    - Develop functionalities for user profiles and role-based dashboards, ensuring each user has access to relevant features based on their role.

- Property Management App:
    - Create property-related functionalities such as managing properties, tenants, and rental agreements within this dedicated app.

- Tenants App:
    - Develop a tenant financial portal to provide tenants with insights into outstanding rent, due dates, payment history, and upcoming payments.

- Maintenance App:
    - Implement functionalities for managing maintenance requests and contractor assignments within this specialized app.

- Financial Tracking App:
    - Develop features for financial tracking, including rental income, expenses, and tenant payments, within this dedicated app.
- Messaging App:
    - Create message board functionalities and peer-to-peer messaging features within this specialized app for communication among users.

## Entity-Relationship Diagram

![ERD](/static/img/readme/schema.png)

The end product is pretty much this for all the core function tables

## Used Technologies

### Languages Used

- HTML, CSS, Python, JS

### Framework, Libraries and Programs

- Frameworks were used to speed up 
    - Django
    - Bootstrap
- Libraries 
    - Gunicorn
      - was used as python http server for WSGI applications
    - dyscopg2
      - was used as PostgresSQL Database adapter
    - django-allauth
      - was used to create user authentication
    - django-crispy-forms
      - was used to control rendering behavior of Django forms
    - whitenoise
      - was used to serve static non-media files
    - django_tables2
      - was used to render tables
    - django_filters
        - was used to create search for tables
    - celery
        - was used as task que
    - django_celery_beat
        - was used to schedule tasks
    - django_celery_results
        - was used to give task feedback in admin panel
    
- Programs
    - Docker
        - was used to host local redis server during dev
    - [erdlab](https://erdlab.io/)
        - was used to create the entity relationship diagram
    - GitHub
        - was used to store the project site
    - VS Code
        - was used to write the code and commit it to GitHub
    - Heroku 
        - was used to deploy the project 
    - Heroku Redis
        - was used as broker for celery tasks
    - Cloudinary
        - was used to serve static media files  
    - Grammarly
        - was used to fix my grammar
    

# Testing

### [Rent Invoice Generation](/finance/tests_invoice_task.py)
___Purpose___

The purpose of testing the rent invoice generation functionality is to ensure that it accurately generates invoices for tenants to pay without any errors or faults. This is important as it involves handling sensitive data related to financial transactions between landlords and tenants. 
These python tests were used in conjunction with manually testing the same scenarios.

- Test coverage
    - Generate rent invoice
        - Verify that the function correctly generates rent invoices based on the tenant profile
        - Updates the user and tenant data it's supposed to
    - Avoiding inactive users
        - Verify that no invoice is generated if a tenant is marked as inactive
    - Rent not due until next month
        - Testing that no invoice will be generated if the tenant's next_rent_due data is in a future month
    - Old unpaid transactions
        - If invoice is overdue and past grace period it will generate next months rent invoice and add that overdue amount to the new invoice
    - Already existing invoice
        - If invoice is already generated for current month skip
    - Multiple unpaid transactions
        - More then one unpaid transaction overdue
    - Tenant with 0 rent
        - Test behavior when tenant has 0 rent set
    - Tenant with negative rent
        - Test behavior when tenant has negative rent set
    - Unpaid invoice but not overdue
        - Case where invoice is unpaid bot not overdue
    - Overdue invoice grace period
        - Tests the grace period a tenant is given before overdue fee's gets added
    - Method to avoid invoices
        - Checks invoice note content


##### [Home page rendering](/dashboards/test_views.py)

Getting a user role and rendering their role specific home page is vital in creating a multi role app. 

- Role specific home page
    - Create different role accounts in setup
    - Check all accounts that they render expected page by checking content in response
- New user without a role assigned
    - Make sure new user get redirected to page to enter inv code


##### Manual focused

- Navigation Links
    - Testing was performed to ensure all navigation links navigated to the correct pages as per design. This was done by clicking on the navigation links on each page as all 3 roles
- Invitation code forms
    - Tenant code tested by creating a code and adding it as a new user
    - Contractor code tested by creating a code and adding it as a new user
        - Wrote tests in python to do the same as mentioned above
    - Test removing generated codes
    - Testing already used code
    - Enter code assigning already assigned properties to contractor
- Accounts
    Steps taken:
    - Test user login
    - Register new account
    - Logout user
    - Change password
- Forms
    - Testing all forms by manually adding expected data and posting
    - Went through all edit forms and editing something




### Validator

#### HTML

Tested HTML files through [w3c](https://validator.w3.org/nu/)
- Lots of errors related to django and template tags
- Redundant test for a django app

#### CSS

All custom css ran through [Jigsaw](https://jigsaw.w3.org/css-validator/validator)

![Jigsaw](/static/img/readme/css.png)

#### JS

All custom js ran through [JSHint](https://jshint.com/)


### Performance

- __Tests performed using [Lightouse](https://chromewebstore.google.com/detail/lighthouse/blipmdconlkpinefehnmjammfjpmpbjk)__

![lighthouse_scores](/static/img/readme/score.png)





# Heroku Deployment
The site was deployed to Heroku. The steps to deploy are as follows:

Prerequisites:
- Create 'Procfile' in your project folder(Note caps and no file tag)
- Add our gunicorn worker: 'web: gunicorn propertize.wsgi'
- Add our celery with beat worker: 'worker: celery -A propertize worker -B'
- Freeze and export our installed libraries
    - pip freeze --local > requirements.txt

<hr>

- Navigate to heroku and create an account
- Click the new button in the top right corner
- Select create new app
- Enter app name
- Select region and click create app
- Click the resources tab and search for Heroku Redis
- Follow redis installation steps
- Go to the settings tab and then click reveal config vars
- Make sure the following config vars exist:
  - SECRET_KEY: (Your secret key)
  - DATABASE_URL: (Database url)
  - REDIS_TLS_URL: (redis server)
  - CLOUNDINARY_URL: (cloudinary api url)
- Click the deploy tab
- Scroll down to Connect to GitHub and sign in / authorize when prompted
- In the search box, find the repositoy you want to deploy and click connect
- Scroll down to Manual deploy and choose the main branch
- Click deploy
- Double check that both workers(Dynos) are enabled under resources*

The app should now be deployed.


# Run Locally
Note that you need your own database and redis server

Clone the project

```bash
  git clone https://github.com/zimmoc/propertize.git
```

Go to the project directory

```bash
  cd propertize
```

Install dependencies
- Recommended to do this in a virtual python env


```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python3 manage.py runserver
```

 

# Credits

All installed libraries have been implented with the help of their respective documentation and examples

Countless of stackoverflow posts whenever i had problems.

Random forum posts from 2010, found through googling problems

### Content 


- Bootstrap theme taken from: [SB Admin](https://github.com/startbootstrap/startbootstrap-sb-admin)
- The icons used were taken from [Font Awesome](https://fontawesome.com/)
- Favicon/Logo by [Font Awesome](https://fontawesome.com/)
