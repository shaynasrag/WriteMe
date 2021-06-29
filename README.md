# WriteMe

## Introduction

Welcome to WriteMe, an interactive journal with the goal of resolving interpersonal conflicts and maintaining stability in relationships.

### Backstory
I started learning about relational psychology in my sophomore fall university course, Attraction and Relationships, by Dr. Jennifer Hirsch. I started reading more about the topic, and began to think of how I can use the information I've learned to create a helpful tool for people. This program is a mix of a therapeutic experience as well as an analytical, longitudinal collection of data. Some aspects of this program collect numerical representations of data, other parts prompt free-response submissions, and the remainder focus on mindfulness, introspection, and self-compassion. This is both a self-help and an analytical tool. The structure of conflict resolution in this journal was inspired by The Attachment Theory Workbook by Annie Chen, LMFT.

I also needed a side project for my resume, so in December 2020, I wrote 300 lines of the World's Worst Code. The project was not maintainble or readable...but it worked. I was satisfied until I took Object Oriented Programming with Timothy Barron in my sophomore spring semester and realized that there is a way to write good code. I went back and re-vamped this whole project using object oriented design and let it sit again for a little while. Just like with psychology books, I love reading books about code. I started reading Clean Code by Robert C. Martin and realized that there was an even better way to write code: short functions, intuitive variable names, modularization, etc. So I went back again, and again, and again. With many late nights and countless hours of optimization thoughts running in the back of my head, I've continued to optimize and condense this program until I couldn't make it any shorter. I'm sure one day soon I'll wake up with a new way to optimize, but for now, please enjoy the many hours of work I put into writing what should appear to be very simple code.

This project combines two of my greatest passions: psychology and computer science. The goal of this project is to develop intuitive and maintainable code that positively impacts the world.

### Form
This program takes the form of Python's tkinter graphical user interface (GUI). It must be run on a local computer and requires the following dependencies on top of Python 3.8:

``tkinter``

``sqlalchemy``

## How it works

### Structure of the Journal

The following image shows how the Journal is structured. When the program is first accessed, an instance of the journal is created. Every use of the journal creates an instance of a submission and within every submission, a user can submit multiple entries. The user can submit multiple entries on multiple people, and all of those entries are stored in one submission at the time of access. Repeated use accumulates multiple submissions.

![image](https://user-images.githubusercontent.com/54994003/120746447-14f9ba80-c4b4-11eb-8cc0-3380df877af9.png)


### Structure of the Entry

This goal of each entry is to create an interactive environement in which the user can work through an interpersonal conflict in relation to a particular person. Each entry is based in a relationship between the user and another person and can follow one of the paths depicted in the image below. The graphic below displays a high level overview of the possible forms an entry can take. Note that there are more questions asked (indicated by the rectangles) and there are more responses requested (indicated by the circles) than displayed in this graphic.

![image](https://user-images.githubusercontent.com/54994003/120749074-c13da000-c4b8-11eb-90ff-67f2cc59c8bb.png)


## Usage

### How to Run

Command Line Interface: ``python3 main.py -CLI``

Graphical User Interace: ``python3 main.py -GUI``

### Data Storage

All data is stored locally in a sqlalchemy database.

## Youtube Walkthrough

Coming soon!
