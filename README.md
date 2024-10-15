The Todo List SPECIAL!

* This is a simple application  in Python to add, edit, mark as done, list or shopping list.
* Simpel freindly user interface.
* ? button for how to use it.
* .exe file to start/run the application. Which is in the folder of 'dist'.
(i use CMD to repack it as an exe file using 'pyinstaller --onefile --windowed todo_list_gui.py')

--------------------------------------------------

First i made it  in C# but.. i like to have a nice visible user interface so re-did it in python to make it so simple as i could.

So i started with the interface, made some changes and finally i was enough happy or pleased with the UX/GUI.
Then i started to think around how i would like it to save down the list/s.
As i been working alot with json it was clear to me that json it is.
I used this for the json saving fuction:

'def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file)'
            
After that i started to build it up as i wanted it to work with the buttons and the saving to json.
When i  was happy i though i was done.. but..
Someone noticed that you can write with letter in the date input field, so had to look into that.
Found the problem and missed the 'def validate_date' configuration.
So now thats out of the world i was pleased once more.

----------------------------------------------------

If you clone this project and want to run it youself.
Just doubleclick the .exe file in the 'dist' folder.
-
You can play around and make you own changes but remember to repack the .exe file after the changes.
-
To repack the .exe:
win+r to open CMD, the write 'cd <your local path for the folder> C:/user/documents/...'.
press enter.
Now when you are in the right path you shall write this:
pyinstaller --onefile --windowed todo_list_gui.py
Then press enter and let it be done!
-
OBS!
Make sure you have PyInstaller installed, if not you can open a Terminal in VS and write this:
pip install pyinstaller
-
Enjoy!
