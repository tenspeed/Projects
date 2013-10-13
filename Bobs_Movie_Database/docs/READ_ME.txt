Bob!!!!! This is your movie database!!!! I hope it works out okay. In order for the program to work properly,
you need to create a folder somewhere that's easy to remember (like in My Documents or the Desktop) and move
the "bmdb" file to it. You'll also need to download and install the python interpreter which I've included a link to for you. Now, this first version sucks and you have to run it from the command prompt, but I know that in time you'll come to love it (until I figure out how to make a real GUI for it) :) When you run the program for the first time, it will create an empty text file called "bmdb.txt" in the same directory that you put the "bmdb" file into. From there, you can either use the program to manually type in new movies or you can exit and copy/paste your existing movies from a different source to the bmdb.txt file. If you copy/paste, there are special formatting instructions you must follow (which I'll explain below) or it won't work. Follow the "Setup Instructions" and then keep reading.

"Setup Instructions"

1) Go to http://www.python.org/getit/ and download the "Python 2.7.5 Windows Installer".

2) Run the Python 2.7.5 Windows Installer and follow the on-screen prompts.

3) Create a new folder inside your user profile (it should be something like "C:\Users\Bob" or whatever your    login name is) with a name of your choosing ("Movie Database" or something memorable).

4) Copy the "bmdb.py" file into the folder you just created.

5) Open the Start Menu and click 'Run'.

6) Type 'cmd' and hit enter.

7) You should see your default user directory "C:\Users\Bob" or something like that. Type "cd Movie Database       Folder Name", hit enter, and you should now be in C:\Users\Bob\Movie Database Folder Name.

8) Type "python bmdb.py" and hit enter to run the program!

9) If shit ain't workin, call me and I'll help :)

10) Whenever you want to run the program, just follow steps 4-7.


"Copy/Paste Instructions"

So assuming you got everything above working, you probably want to copy/paste your existing movie list instead of typing them in all over again. Each movie in the database has six identifying catagories associated with it: 'Title', 'Genre', 'Director', 'Year', 'Format', and 'Actors'. In the text file "bmdb.txt" where your movie information is saved, the categories are formatted as follows:

title1;genre1;director1;year1;format;actor1, actor2, actor3, actor4;title2;genre2;director2;year2;format;actor5, actor6;

Each category is separated by a ";" with no spaces. You can have multiple items in each category, but they should be lowercase and separated by a "," and a space, like I did for the 'Actors' in the example above. I've also provided an example text file, "bmdb_example.txt", to look at and use as a reference. You don't have to fill out everycategory but you should at least put something like 'unknown' or 'don't care' if you don't care about say, the director or genre of a certain movie. Just change the formatting of your word document and you should be able to copy/paste it into bmdb.txt without a problem! If you do have problems, double check the formatting. It might be easier if you do small chunks at a time as well. You can also just copy/paste the example file into bmdb.txt and run the program to see how its supposed to work.