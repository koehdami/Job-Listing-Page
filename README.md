# Job-Listing-Page
Job Listing Page for creating and applying to job listings.

What does the App do?

Index.
I created an app that allows users to create job listings that other users can apply to. The page has various routes, with the index route serving as the landing page. The focus here was on web design, aiming to create an appealing appearance for users when they first arrive on the page. I used familiar styling components such as cards and image banners.

Profile.
The next route to discuss is the profile page. Here, users can view their name, note their current job and title, and also see their own job listings. In future updates, there are plans to allow attaching a CV and Certificates, but for now, it felt too heavy-weight to implement.

Jobs.
The Jobs Page is the core of this platform. Here, users can view all listed jobs and sort them by categories, language, and time. The search algorithm posed a significant challenge here; I aimed to enable users to select categories and search by title. Implementing all these different attributes proved to be quite challenging.

Contact.
The Contact Page is a standard contact page. Logged-in users already have the form pre-filled, while anonymous users can fill it out manually. All requests are stored in the database.

Login/Logout/Register.
Basic user authentication like used in previous projects.

CreateListing.
This is a form for creating new listings that will be displayed on the Jobs Page, here I used the built in django form for form validation.

MyListings.
This section displays your own listings, where you can also edit and remove them.

deletePosting and editPosting.
These are the routes used for editing and removing your own postings.

jobs/<str:id>.
Here, users can see all attributes of a specific job listing and apply to it. If it's the user's listing, they can also remove and edit it.

apply.
This route is used for applying to listings. Currently, the information is only stored in the database. In the future, there are plans for enabling the listing owners to check who applied to the job, review their CVs and Certificates, and even chat with them.



Distinctiveness and Complexity

**What Sets This Page Apart**

I've crafted this page using a complex web of nested database models to make our search engine work. My main goal was to create a strong and user-friendly design that works well on mobile devices, which took a lot of effort.

Additionally, this page forms a solid basis for future improvements and includes many features commonly seen on modern job listing sites. I've also added lightweight unit testing, that was taught in this course.


Difference to other Projects

Picking a unique project was tough, but I did some online research and found that creating a "job listing page" is a great practice project for full-stack developers. While it includes some familiar features from past projects, I think it offers a different perspective.

This project shifts the focus to the "jobs" themselves, with their various attributes that require thorough evaluation. This different approach sets it apart and provides an interesting development challenge.



Run my application

I've intentionally avoided using any third-party libraries in this project. You should be able to run the project with: "python manage.py runserver" after creating and implementing the migrations.


Conclusion

Even though the webpage isn't complete, I'm already very proud of it. I've invested a lot of time in crafting a solid web design that looks great on mobile devices. This project felt more challenging than the ones we studied in this course.
The work on the backend, including authentication, route creation, model development, and the implementation of a search engine, has turned this webpage into a solid foundation with a lot of potential.
