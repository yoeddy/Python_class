'''
COM 110 - Programming Assignment 4
Carly Trapeni
Professor William Tarimo

This program creates a word cloud from a text. The words are placed randomly with sizes
and colors that correspond with the frequency of each word. A word cloud is helpful
because you can gain new information or a new perspective on the text.
'''

from graphics import *
from random import randrange

def main():

    # Getting users input of fileName and maxCount and passing the graphics window to be able to draw into it 
    fileName, maxCount, word_cloud = drawGraphics()
    # Creating a dictionary by reading the fileName, passing the fileName and the number of words to return and returning a dictionary of the words and their frequencies
    counts = textRead(fileName, maxCount)
    # Passing the dictionary and the graphics window to be used in the function that draws the word cloud
    drawWordCloud(counts,word_cloud)

def drawBackground(pt1,pt2,color,name):
    
    # Creating the form of the background
    background = Rectangle(pt1,pt2)
    background.setFill(color)
    background.draw(name)

def drawGraphics():

    # Creating a graphics window
    word_cloud = GraphWin("Word Cloud",800,800)
    
    # Setting the coordinates of the graphic window
    word_cloud.setCoords(0,0, 100,100)

    # Drawing a background
    drawBackground(Point(0,0), Point(100,100),"lightgrey",word_cloud)

    # Drawing instructions
    intro = Text(Point(50,50),"Welcome to my Wordcloud Generator.")
    intro.setSize(30)
    intro.setStyle("bold")
    continue_click = Text(Point(50,40),"Click to continue.")
    intro.draw(word_cloud)
    continue_click.draw(word_cloud)
    word_cloud.getMouse()
    intro.undraw()
    continue_click.undraw()
    explanation = Text(Point(50,50),"This program will generate a word cloud based on the text file that you input. \nThe word cloud places the words in the text file randomly with the sizes of the word \ncorresponding to its frequency. The bigger the word appears, the more oftens its mentioned\n in the text and the more important it is. \nThe colors are also random. A word cloud is helpful \nbecause you can gain new information or a new perspective on the text.")
    explanation.setSize(15)
    explanation.draw(word_cloud)
    continue_click.draw(word_cloud)
    word_cloud.getMouse()
    explanation.undraw()
    continue_click.undraw()
    # Prompting the user to enter an integer and a text file
    num_words_entry = Entry(Point(50,50),90)
    num_words_entry.setText("How many words would you like to display in the word cloud? Maximum 25. Delete this text first and enter integer here: ")
    num_words_entry.draw(word_cloud)
    continue_click.draw(word_cloud)
    word_cloud.getMouse()
    num_words_entry.undraw()
    entry1 = Entry(Point(50, 50), 60)
    entry1.setText("Enter the name of the file to analyze. Delete this text first and include the .txt: ")
    entry1.draw(word_cloud)
    help_text = Text(Point(50,60), "If you have no text file to input, you can use Little Red Riding Hood by typing in: story.txt")
    help_text.setSize(15)
    help_text.draw(word_cloud)
    word_cloud.getMouse()

    # Getting the text from the entry boxes
    fileName = entry1.getText()

    # Turning numWords into an integer
    # wrapping in a try..except in case a invalid integer is entered
    # in that case, default to 25
    try:
        maxCount = int(num_words_entry.getText())
    except:
        maxCount = 25
        
    # Making sure maxCount is the maximum number of words to be displayed
    if maxCount > 25:
        maxCount = 25

    # Undrawing text
    entry1.undraw()
    continue_click.undraw()
    entry1.undraw()
    continue_click.undraw()
    help_text.undraw()
    
    return fileName, maxCount, word_cloud

def textRead(text_name, maxCount):   
    # Reading the file and converting all the letters to lower case
    text = open(text_name, "r").read().lower()

    # Checking for punctuation
    for ch in '!@#$%^&*()~`{[}]|\":;?/>.<,_-+=':
        # Replacing each punctuation character with a space
        text = text.replace(ch," ")

    # Splitting the string at whitespace to form a list of words
    words = text.split()

    # Reading the file of stop words
    stop_words = open("stop_words.txt", "r").read()

    # Getting a list of the stop words
    stop_words = stop_words.split("\n")
    stop_words = list(stop_words)

    # Creating an empty list
    exclude_list = []
    # Creating an empty dictionary
    counts = {}

    # Creating a list of the stop words
    for line in stop_words:
        exclude_list.append(line.replace("\n",''))

    # For every word in the text file
    for line in words:
        for word in line.split():
            if word not in exclude_list:
                if word not in counts.keys():
                    # Adding the words and their frequencies to the dictionary
                    counts[word] = 1
                else:
                    counts[word] = counts.get(word,0) + 1

    # Creating a dictionary of the words and their frequencies and sorting by the frequencies
    # I was inspired by: https://www.geeksforgeeks.org/python-program-to-sort-the-list-according-to-the-column-using-lambda/#google_vignette

    sorted_dict = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    # Setting the maximum word count to maxCount
    small_word_list = {}
    word_count = 0
    for key, value in sorted_dict:
        if word_count < maxCount:
            small_word_list[key] = value
            word_count = word_count =+ 1
    
    return small_word_list

def checkValidPoint(word,count, x, y, pts_list):
    
    existingWord = 0
    letters = len(word)
    size = (count * 2) + 4

    # Creating a rectangle surrounding each word based on the font size and number of letters
    for word_pt in pts_list:

        pt_x = word_pt.getX()
        pt_y = word_pt.getY()
        rect_x_left = pt_x-(letters/2)
        rect_y_left = pt_y-(size/4)
        rect_x_right = pt_x+(letters/2)
        rect_y_right = pt_y+(size/4)

        word_rect = Rectangle(Point(rect_x_left,rect_y_left), Point(rect_x_right,rect_y_right))

        # Determining if the center coordinates of the word fall within the boundaries of the rectangle of any other word
        if x > rect_x_left and y > rect_y_left and x < rect_x_right and y < rect_y_right:
            existingWord = existingWord  + 1
        else:
            existingWord = existingWord  + 0

    # Returning false as long as the word coordinates are not within any other rectangle
    if existingWord > 0:
        return False
    else:
        return True

def drawWordCloud(counts, word_cloud):
    pts_list =[]
    for key in counts:

        # Setting the text size based on the word count
        size = (counts[key] * 2) + 4
            
        # Assigning values to create a random color
        r = randrange(0,256)
        g = randrange(0,256)
        b = randrange(0,256)

        # Choosing a random location for the text   
        x = randrange(5,95)
        y = randrange(0,100)

        # Drawing the words
        draw_words = Text(Point(x,y), key)
        # Getting the center coordinates of the word
        word_pt = draw_words.getAnchor()
        pt_x = word_pt.getX()
        pt_y = word_pt.getY()

        # While the center coordinates of the word fall within any other words rectangle, assigning a new random coordinate to the word 
        while (checkValidPoint(key, counts[key], pt_x, pt_y, pts_list) == False):
            x = randrange(5,95)
            y = randrange(0,100)
            draw_words = Text(Point(x,y), key)
            word_pt = draw_words.getAnchor()
            pt_x = word_pt.getX()
            pt_y = word_pt.getY()

        # Adding the words that don't overlap to the list
        pts_list.append(word_pt)
    
        # Setting the word to be a random color and size
        draw_words.setTextColor(color_rgb(r, g, b))
        draw_words.setSize(size)
        # Drawing the words to the word_cloud
        draw_words.draw(word_cloud)

main()
