# WriteMe

## Introduction

### Backstory
This program was inspired by my sophomore fall university course, Attraction and Relationships, taught by Dr. Jennifer Hirsch. The goal of this program is to collect data, track progress and develop positive and healthy mindsets towards relationships.


Further (implemented and intended) optimization of the backend structure of this code comes from my sophomore spring university course, Object Oriented Programming, taught by Dr. Timothy Barron. Optimizations include object oriented design structure built with CLI and Tkinter GUI frontend options, the use of sqlalchemy databases, default AND custom exception handling, and logging.

This project combines two of my greatest passions: psychology and computer science. The goal of this project is to develop intuitive and maintainable code that positively impacts the world.

### Form
This program takes the form of Python's tkinter graphical user interface (GUI). It must be run on a local computer and requires the following dependencies on top of Python 3.8:

``tkinter``

``sqlalchemy``

My focus in developing this program is primarily on the backend design and efficiency. I default to CLI and GUI frontend options as a way to represent the data used.

## How it works

### Structure of the Journal

The following image shows how the Journal is structured. When the program is first accessed, an instance of the journal is created. Every use of the journal creates an instance of a submission and within every submission, a user can submit multiple entries. The user can submit multiple entries on multiple people, and all of those entries are stored in one submission at the time of access. Repeated use accumulates multiple submissions.

![image](https://user-images.githubusercontent.com/54994003/120746447-14f9ba80-c4b4-11eb-8cc0-3380df877af9.png)


### Structure of the Entry

This goal of each entry is to create an interactive environement in which the user can work through an interpersonal conflict in relation to a particular person. Each entry is based in a relationship between the user and another person and can follow one of the paths depicted in the image below. The graphic below displays a high level overview of the possible forms an entry can take. Note that there are more questions asked (indicated by the rectangles)and there are more responses requested (indicated by the circles) than displayed in this graphic.

![image](https://user-images.githubusercontent.com/54994003/120749074-c13da000-c4b8-11eb-90ff-67f2cc59c8bb.png)


## How to Use

### Purpose

This program is a mix of a therapeutic experience as well as an analytical, longitudinal collection of data. Some aspects of this program collect numerical representations of data, other parts prompt free-response submissions, and the remainder focus on mindfulness, introspection, and self-compassion. This is BOTH a self-help and an analytical tool.

### Data Storage

All data is stored locally in a sqlalchemy database.

### How to Run

Command Line Interface: ``python JournalCLI.py``

Graphical User Interace (Tkinter GUI -- coming soon): ``python JournalGUI.py``

## Youtube Walkthrough

Coming soon!
