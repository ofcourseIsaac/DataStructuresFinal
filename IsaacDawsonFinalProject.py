#***************************************************************
# Name :Lifting Tracker Final Project 
# Author: Isaac Dawson
# Created : 4/9/2024
# Course: CIS 152 - Data Structure
# Version: 1.0
# OS: Windows 11
# IDE: Visual Studio Code
# Copyright : This is my own original work 
# based onspecifications issued by our instructor
# Description : A program that helps the user make a workout plan that they can follow in the gym
#            Input: Set, Reps and Weight 
#            Ouput: Text File / GUI
#            BigO: O(N*7)
# Academic Honesty: I attest that this is my original work.
# I have not used unauthorized source code, either modified or
# unmodified. I have not given other fellow student(s) access
# to my program.
#***************************************************************
# Imports for the DataStructures, Time and GUI
import random
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
import queue

# Class for workout node, this is used to constuct a linked list that will be used when constructing a days workout plan
# The workouts (Bench press, Squat, Deadlift) are stored in a list and the data for those workouts are stored in a dictionary (reps: "x", set: "Y", Weight "Z") so we can store multiple sets of data per workout
class WorkoutNode:

    def __init__(self, day):
        self.day = day
        self.next = None
        self.workouts = []
        self.workout_data = {}


    # This method is used to add the data about workouts to the dictionary of the associated node
    def add_workout_data(self, workout, sets, reps, weight):
        
        # First if the workout being added is check if it already has data and if not create an empty list
        if workout not in self.workout_data:
            self.workout_data[workout] = []

        # after checking that append the dictionary data to the list
        self.workout_data[workout].append({'sets': sets, 'reps': reps, 'weight': weight})


# creates the linkedlist class that will be used to store the workoutnodes 
class WorkoutLinkedList:
    # constructs the linked list with a head
    def __init__(self):
        self.head = None


    # Creates a method for the linked list to insert an item to the end of the linked list
    def insert(self, day):
        
        # Create a node for the day of the week
        new_node = WorkoutNode(day)

        # if the linked list is empty then assign the head to the new node
        if not self.head:
            self.head = new_node

        # Otherwise assign current to the node at the front
        else:
            current = self.head

            # loop through the nodes until it reaches a node with no next node
            while current.next:
                current = current.next

            # once a node with no next is found point the current node at the new node
            current.next = new_node


    def find(self, day):
        # assign a varaible to the first item in the linked list
        current = self.head

        # aslong as there is an item in the list a loop will run to iterate through items 
        while current:

            # if the day of the current node matches the day we are looking for the return that 
            # otherwise change the current node to the node it is pointing to
            if current.day == day:
                return current
            current = current.next

        # if nothing matches return none
        return None

# Creates a class that exists to handle the main page of the GUI
class WeightLiftingPlanner:

    # Constructs the main window, assign it a title and background color
    def __init__(self, master):
        self.master = master
        self.master.title("Weight Lifting Planner")
        self.master.configure(bg='white')

        # load the image of the barbell and subsample it to make it fit for display
        self.logo_image = tk.PhotoImage(file="Barbell.png").subsample(12, 12)

        # creat a list that has all the days of a week
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Create an empty linked list using the class
        self.workout_list = WorkoutLinkedList()

        # create an empty queue object for storing the quote of the day, then fill this queue
        self.quotes_queue = queue.Queue()
        self.fill_quotes_queue()


    # a method that will fill the queue with quotes 
    def fill_quotes_queue(self):

        # 15 inspirational quotes for use
        quotes = [
            "The only bad workout is the one that didn't happen.",
            "Success isn’t always about greatness. It’s about consistency.",
            "Wake up with determination. Go to bed with satisfaction.",
            "Strive for progress, not perfection.",
            "You don’t have to be great to start, but you have to start to be great.",
            "If you wanna make people dream, you've gotta start by believing in that dream yourself!",
            "Whatever you lose, you'll find it again. But what you throw away you'll never get back.",
            "Fitness is not about being better than someone else. It’s about being better than you used to be.",
            "Go Make Your Body Sexy!",
            "Go Beyond Plus Ultra",
            "Beleive in the me that beleives in yous",
            "Surpass your limits, right here, right now!",
            "Everyone has a plan until they get punched in the face",
            "Becoming better is nothing something that happens overnight but over weeks",
            "A real hardworker understands that they are capable of anything"
        ]
        
        # set the max size of the queue to 15 
        self.quotes_queue = queue.Queue(maxsize=15)

        # loop through the list of quotes and put them into the queue
        for quote in quotes:
            self.quotes_queue.put(quote)


    # Method for getting the next quote from the queue
    def get_next_quote(self):

        # check if the queue is empty and if it is refill it
        # this condition should never trigger in the program however Ideally this would be a program that was saved online
        # and by doing this the program would have a need to repopulate the queue with more qoutes, 
        # since after some time the quotes would all be used up due to only 15(2weeks) quoutes existing, however since the app
        # is not always online it will not activate because the queue is freshly populated with data each time the program opens. 
        if self.quotes_queue.empty():
            self.fill_quotes_queue()

        # gets the next quote and assigns it to a value, then puts the quote at the back of the line. Finally return the new quote
        next_quote = self.quotes_queue.get()
        self.quotes_queue.put(next_quote)
        return next_quote

    
    # create a method for building the main/master page of the GUI and program. 
    def create_main_page(self):

        # Creates a frame that is used for the main page
        self.main_frame = tk.Frame(self.master, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        # Get the current date and last weeks date, these will be used to diplay the current date for today
        # the week behind is the one that will be used to show the text document is for last week on the main page
        current_date = datetime.datetime.now().strftime("%d/%m/%Y")
        yesterday_date = datetime.datetime.now() - datetime.timedelta(days=7)
        yesterday_date_str = yesterday_date.strftime("%d/%m/%Y")

        # Create a label that says the name of the program and the date at the top 
        label = tk.Label(self.main_frame, text=f"Weight Lifting Planner \n{current_date}", bg='white')
        label.pack(pady=10)

        # Create a label that will be used to display a png image of a barbell
        logo_label = tk.Label(self.main_frame, image=self.logo_image, bg='white')
        logo_label.pack(side="top", pady=(20, 10)) 

        # Add a label that labels the output box of last weeks workouts, 
        # it labels it as last weeks then put the date from a week ago 
        label = tk.Label(self.main_frame, text=f"Last Weeks Plan - {yesterday_date_str}", bg='white')
        label.pack(pady=10)

        # Add a frame to contain the buttons and search results
        top_frame = tk.Frame(self.main_frame, bg='white')
        top_frame.pack(side="top", fill="x")

        # this frame will be used setup display for the txt file that is being read in, 
        # this file is the same one that is created by this program when ending a week
        results_frame = tk.Frame(top_frame, bg='white')
        results_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Creates a widget that uses the frame created above to output the data in the txt file 
        self.search_results_text = tk.Text(results_frame, bg='lightgray', wrap="word", height="18")
        self.search_results_text.pack(fill="both", expand=True)

        # Add a frame to contain the buttons
        buttons_frame = tk.Frame(top_frame, bg='white')
        buttons_frame.pack(side="bottom")

        # start by looping the entire days list
        for i, day in enumerate(self.days):

            # Create a button for each day of the week laid out horizontly  
            button = tk.Button(buttons_frame, text=day, command=lambda d=day: self.open_workout_page(d))
            button.pack(side="left", padx=5, pady=5)

        # Add a button that clears the week of workouts and prints them to a text file.
        clear_week_button = tk.Button(self.main_frame, text="Export Week", command=self.export_week)
        clear_week_button.pack(side="top", pady=(10, 20)) 

        # When the program is first opened run this method, 
        # it allows for the previous text file saved by the program to be read in as last weeks plan in the 
        self.search_workouts()

    # opens the text file that is saved with the data about workouts and reads it to a text box on the main page
    def search_workouts(self):
        try:
            with open("week_workouts.txt", "r") as file:
                content = file.read()

                # Clear previous search results and replace them with the new
                self.search_results_text.delete(1.0, "end")
                self.search_results_text.insert("end", content)

        # if no txt file exist an error occurs that creats a popup, the program will run fine after that
        except FileNotFoundError:
            messagebox.showerror("Error", "No workouts found for the week.")


    # Creates a method for building the workout Pages GUI
    def open_workout_page(self, day):
        
        # Hide the main page frame so we can view the workouts page
        self.main_frame.pack_forget()

        # Create a new frame for the workout page
        self.workout_frame = tk.Frame(self.master, bg='white')
        self.workout_frame.pack()

        # Add text to show what day the user has selected
        label = tk.Label(self.workout_frame, text=f"Workouts for {day}", bg='white')
        label.pack(pady=10)

        # This creats a dictionary that stores workouts based on which muscle group (key) they hit, 5 workouts are stored in a list (value) 
        # If I had more time I would have looked into finding a way to have more than the just the options hardcoded in. 
        muscle_groups = {
            "Shoulders": ["Shoulder Press", "Lateral Raises", "Upright Row", "Face Pulls", "Shrugs"],
            "Chest": ["Bench Press", "Incline Bench", "Cable Fly", "Chest Dip", "Chest press machine"],
            "Back": ["Back Row", "Seated Row", "Lat pulldowns", "1 arm dumbell row", "T-Bar Row"],
            "Arms": ["Curls", "Tricep Dips", "Tricep Pulldown", "Preacher Curl", "Backwards Bar Curl"],
            "Legs": ["Squats", "Lunges", "DeadLift", "Calf raises", "Hip Thrusts"]
        }

        # Loop through the muscle group dictionary
        for group, workouts in muscle_groups.items():

            # then create the label for the muscle group currently being looped
            group_label = tk.Label(self.workout_frame, text=group, bg='white', font=('Arial', 12, 'bold'))
            group_label.pack(pady=5, padx=10, anchor='w')

            # Create a frame so that each workout can have its own button
            button_row_frame = tk.Frame(self.workout_frame, bg='white')
            button_row_frame.pack(anchor='w')

            # Actually creates the buttons and places them on the screen. 
            for workout in workouts:
                add_workout_button = tk.Button(button_row_frame, text=f"Add {workout}", command=lambda w=workout: self.add_workout(day, w))
                add_workout_button.pack(side='left', padx=10, pady=2)

        # at the botton of the page add a button that allows the user to go back to the previous page. 
        back_button = tk.Button(self.workout_frame, text="Back to Main Page", command=self.close_workout_page)
        back_button.pack(pady=10)

        # check if the workouts for the day are in the linked list, if not insert them into the linked list
        if not self.workout_list.find(day):
            self.workout_list.insert(day)

    def close_workout_page(self):
        # Close the frame for the workout page and creates a pack 
        self.workout_frame.pack_forget()
        self.main_frame.pack()

    # creates the method that will be called when a button for a workout is pressed on the workouts page
    def add_workout(self, day, workout):

        # Get the node for the selected day from the linked list, then append the workout.
        day_node = self.workout_list.find(day)
        if day_node:
            day_node.workouts.append(workout)

            # Prompt the user for sets, reps, and weight separately, when user presses the button the Get valid input method is run
            sets = self.get_valid_input("Sets", f"Enter the number of sets for {workout}")
            reps = self.get_valid_input("Reps", f"Enter the number of reps for {workout}")
            weight = self.get_valid_input("Weight", f"Enter the weight for {workout} (lbs)")

            # add the lifts specific data for the day to the node so they can be accessed in the linked list. 
            if sets is not None and reps is not None and weight is not None:
                day_node.add_workout_data(workout, sets, reps, weight)


    # Method for getting valid input when the user is inputting liftting data
    def get_valid_input(self, input_type, prompt):
        
        # uses a never ending while loop to make sure the user actually input something
        while True:
            
            # creates a window that prompts the user for input
            value = simpledialog.askstring(input_type, prompt)

            # if the user presses cancel 
            if value is None:
                return None
            
            # Check if the value that was input is a number, if not output an error
            if not value.isdigit():
                messagebox.showerror("Invalid Input", f"Please enter a positive integer for {input_type}")
            
            # Convert to integer for comparsions
            else:
                value = int(value) 

                # Make sure the value is not negative 
                if value < 0:
                    messagebox.showerror("Invalid Input", f"Please enter a positive integer for {input_type}")
                
                # finally if the value passes all the tests return it to be added to the node. 
                else:
                    return value


    # this method exports the week worth of workouts and data so it can be written to a file so the user can look back at it in the future 
    # currently this method only writes to one file and just overwrites that same file on future uses of the program, however I would like to add 
    # the ablitiy to have it save based on the week for a more long term log of workouts. 
    def export_week(self):

        # Starts by grabbing the current date 
        current_date = datetime.datetime.now()

        # opens a text file that will be used to store the workout node data
        with open("week_workouts.txt", "w") as file:
            
            # loops through the days of the week 
            for day in self.days:

                # Check if a node exists for the current day and if not insert an empty list for the day
                if not self.workout_list.find(day):
                    self.workout_list.insert(day)

                # to denote the current day we are on first write the date and the day of the week
                file.write(f"{current_date.strftime('%d/%m/%Y')}:\n")
                file.write(f"{day}:\n")

                # assign day node with the workout list for the day
                day_node = self.workout_list.find(day)
                
                # check if there is workouts in the list for that day
                if day_node.workouts:

                    # Sort workouts by highest number of sets using insertion sort
                    # Initialize an empty list to store workouts with their associated data
                    workouts_with_data = []

                    # Iterate over each workout in the list of workouts for the current day, then get the workout data for the current workout
                    for workout in day_node.workouts:
                        workout_data = day_node.workout_data.get(workout, [])

                        # Append a tuple of workout and its data to the workouts_with_data list
                        workouts_with_data.append((workout, workout_data))

                    # starting at the second item iterate through the workouts (to avoid the workout name)
                    for i in range(1, len(workouts_with_data)):

                        # store the current workouts and its data and make another index that is one place to the left
                        key = workouts_with_data[i]
                        j = i - 1

                        # If the workout data is empty or if the number of sets in the keys data is greater than the current elements data set
                        # move the current element to the right to make space for the key
                        while j >= 0 and (not workouts_with_data[j][1] or key[1][0]['sets'] > workouts_with_data[j][1][0]['sets']):
                            workouts_with_data[j + 1] = workouts_with_data[j]
                            j -= 1
                        
                        # insert the key into the proper position. 
                        workouts_with_data[j + 1] = key

                    # write the name of the workout to the file
                    for workout, data in workouts_with_data:
                        file.write(f"  - {workout}\n")
                    

                        # If the workout has data write that information using a loop to get each workouts data
                        for d in data:
                            file.write(f"    * Sets: {d['sets']}, Reps: {d['reps']}, Weight: {d['weight']} lbs\n")
                
                # if no data exists for that day it is considered to be a rest day and written as such
                else:
                    file.write(f"  - Rest Day\n")
                file.write("\n")

                # using a queue at the end of the days data
                quote = self.get_next_quote()
                file.write(f"Quote of the Day:\n{quote}\n\n")

                # Increment the current date by one day
                current_date += datetime.timedelta(days=1)


def main():
    root = tk.Tk()
    app = WeightLiftingPlanner(root)
    app.create_main_page()
    root.mainloop()

if __name__ == "__main__":
    main()

#Big O-Complexity: O(N*7)
#I beleive this because every day of the week must be iterated through so the amount of data in the linked list of each week is what defines the worst case secnario

# Hello Dr Ruse, 
# I just wanted to thank you for everything I feel this class has truly helped me become and better programmer. Furthermore,
# I am sorry about the constant problems I was having this semester that lead to me often turning in work late. Thank you! 