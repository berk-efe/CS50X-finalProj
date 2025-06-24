# CS50X-finalProj

#### https://youtu.be/Zwl-fmtALdk
#### Description:

CS50X final project, it is a simple api wrapper webpage showing you latest video game sales.
<br><br>
In the beginning of the project i checked the APIs rules and authentication and free limits. I am only using this API for education purposes, no selling so it is okay to use. Later i used Postman to idenify and test the API while reading its documentation. I tested several API points and only used one. 
<br><br>
I tried my best to make a good docstring for my single function. I should have just made several functions with same endpoint but it came to my mind just now...
<br><br>
Index Page:
Index page has "Highlights" which takes some deals with "-trending" filter(All filter are documented on the Is There Any Deals API page but i added some of them to functions docstring). Under highlights there are three fancy buttons which forwards you to /games with filters.
<br><br>
Games Page:
This page is a little bit more complex. On the left side there are simple filters you can use. They instantly make a GET request to the given page. On the right side we have our results. The star icons on the right side of the deals are "save_game" buttons or whatever you want to call it. They save your deal and you can unsave them or see a list of saved deals on your /profile page.
<br><br>
Profile Page:
It is very very very straight forward. There are nothing but just your saved deals. Thats practically it for that page.
<br><br>
Login, Logout, Login_required and Register are copied and pasted from the previous assignment. They are exactly the same.
<br><br>
There are some important points such as inject_globals() function. I wanted to have user_id no matter what with a simpler syntax so i searched for context processors and added it to my code. I also use env variables so i do not flash my API keys. You can get your own key, assign the env variable and you are good to go.
<br><br>
Let me explain get deals function further.

````python
Get deals, you can get deals **sorting** and **limiting**<br>There are several sorting **options** such as:<br>
**trending:** get the most trending deals
<br>
**price:** get the cheapest deals
<br>
**cut:** get deals with the highest sale rate
<br>
...
<br>
you can reverse sort them with minus(-)

Args:
    sort (str, optional): sorting option. Defaults to "-trending".
    limit (int, optional): limit. Defaults to 6.
    shops (list[int], optional): list of shop IDs to filter deals. Defaults to DEFAULT_SHOPS.

Returns:
    Union[dict, None]: Returns a dictionary with game data or None if an error occurs.

````
you can also filter by shops, i added some default shops to the function but you can pass your own list of shop IDs.
<br><br>
i have added a footer base.html (which called layout.html in the previous assignment) so you can easily change the footer in one place. Again added an extra html file for navbar so our code is cleaner.
<br><br>
Here is a quick schema of the database:
```sql
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    email TEXT NOT NULL);
CREATE TABLE sqlite_sequence(name,seq);

CREATE TABLE IF NOT EXISTS "deals"(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    game_id TEXT NOT NULL,
    game_title TEXT NOT NULL,
    game_banner TEXT NOT NULL,
    game_url TEXT NOT NULL,
    game_price NUMERIC NOT NULL,
    game_regular NUMERIC NOT NULL,
    game_cut INTEGER NOT NULL,
    game_shop_name TEXT NOT NULL, currency TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id));
sqlite> 
```

At first i couldnt find a way to use SQL effectively, because i forgot i have to use SQL. So this project developed as a simple python script which gets the data and prints it to the fancy page. Later i realized that i must use SQL since it is in the assignment. I immediently copied all user related code from the previous assignment and added a deals table. Then it came to my mind that i can use SQL to save deals. So i added a deals table and now you can save your deals.
<br><br>
I hope you like it, i tried my best to make it as clean as possible. I also added a requirements.txt file so you can install the dependencies easily. This site is really looking useable so i also added a telegram bot which sends me messages about my saved deals. You can find it in my github page.
<br><br>

So yeah! it was a great project. I did learn flask jinja and such but practising SQL helped me a lot.
<br><br>

Thanks a lot David J. Malan and CS50X team.

