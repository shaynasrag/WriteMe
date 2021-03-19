# attachment_tracker

## Introduction

### Backstory
This program was inspired by my sophomore fall university course, Attraction and Relationships, taught by Dr. Jennifer Hirsch. The goal of this program is to collect data, track progress and develop positive and healthy mindsets towards relationships.

This program is designed specifically for those who identify along the anxious attachment; however, since attachment theory exists on a spectrum, likely everyone would benefit from the introspection prompted by this program.

Further (implemented and intended) optimization of the backend structure of this code comes from my sophomore spring university course, Object Oriented Programming, taught by Dr. Timothy Barron. Optimizations include object oriented design structure built with CLI and Tkinter GUI frontend options, the use of sqlalchemy databases, default AND custom exception handling, and logging.
### Form
This program takes the form of Python's tkinter graphical user interface (GUI). It must be run on a local computer and requires the following dependencies on top of Python 3.8:
``tkinter``

``sqlalchemy``

My focus in developing this program is primarily on the backend design and efficiency. I default to CLI and GUI frontend options as a way to represent the data used.
 
## How to Use

### Purpose

This program is a mix of a therapeutic experience as well as an analytical, longitudinal collection of data. Some aspects of this program collect numerical representations of data, other parts prompt free-response submissions, and the remainder focus on mindfulness, introspection, and self-compassion. This is BOTH a self-help and an analytical tool.

### Data Storage

All data is stored locally in a sqlalchemy database.

### Submissions vs Statistics

There are two main functions of the GUI: to add a submission or to view the statistics agregated from the previous submissions. 

Submissions focus on specific relationships and the user is prompted to focus on a particular person. The submission can take on 3 possible forms dependent on factors of anxiety levels in the relationship as well as present conflicts and how they are addressed.

Statistics are split into 3 categories: graphical representations of numerical data, text renderings of submissions based on specific people (which may contain various categories), and text renderings of submissions based on specific categories (which may contain various people) within a given time frame. (My hope for the web-based version is to integrate more people and more categories in a single graph.)


## Youtube Walkthrough

Click the image below to view my walkthrough of the Tkinter GUI (deprecated version from January) in this repo. In the video, I discuss ways in which I am hoping to optimize the performance in the web app version.
[![Tkinter GUI Walkthrough](https://i9.ytimg.com/vi/_JiD7lCNH6I/mq3.jpg?sqp=CPT3zf8F&rs=AOn4CLDUyV28lsbSDzuV-QLigBMTcxQWiA)](https://www.youtube.com/watch?v=_JiD7lCNH6I)