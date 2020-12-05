# Project description
this project is a coffee shop menue where end users can view, add,delete and upadte drinks based on autherty as followed :-
1- public users (without login) can :
    * can view short description of drinks available in coffee shop. 
2- barista users can: 
    * can view full detailed description of drinks available in coffee shop. 
3- manager users can: 
    * can view full detailed description of drinks available in coffee shop. 
    * add new drink in the coffee shop. 
    * update drink in the coffee shop.
    * delete drink in the coffee shop.
# Project dependencies
To run this project you will need the following to installed:- 
1- python3 
2- pip 
3- node
4- npm 

# Start backend
1- go to folder: 03_coffee_shop_full_stack/solved/backend. 
2- using command line run this command: pip install -r requirements.txt. 
3- go to folder: 03_coffee_shop_full_stack/solved/backend/src. 
4- using command line run this command: 
    export FLASK_APP=api.py
    flask run --reload
# Start frontend
1- go to folder: 03_coffee_shop_full_stack/solved/frontend.
2- using command line run this command: ionic serve. 
# Error handling 
using coffee shop API you may recieve one of these:
    * 404 –-> resource not found
    * 422 –-> unprocessable
    * 401 –-> not authorized to access API
in this format: 
    {
        "success": false,
        "error": error code,
        "message": Message
    }

