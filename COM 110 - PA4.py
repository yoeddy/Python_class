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
    
    text1,word_cloud = drawGraphics()
    counts = textRead(text1)
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

    # Drawing a message
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
    entry1 = Entry(Point(50, 50), 60)
    entry1.setText("Enter the name of the file to analyze. Delete this text first and include the .txt: ")
    entry1.draw(word_cloud)
    continue_click.draw(word_cloud)
    help_text = Text(Point(50,60), "If you have no text file to input, you can use Little Red Riding Hood by typing in: story.txt")
    help_text.setSize(15)
    help_text.draw(word_cloud)
    word_cloud.getMouse()
    text1 = entry1.getText()
    entry1.undraw()
    continue_click.undraw()
    help_text.undraw()
    return text1, word_cloud

# I need to make it so the user can choose how many words they want to display and if they dont choose it displays the top 25.
#enter the number of words they want to display, if not 25

def byfreq(pair):
    return pair[1]

def textRead(text_name):   
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

    # Creating a list of the words and their frequencies

    sorted_dict = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    # set maximum word count to 25
    small_word_list = {}
    word_count = 0
    for key, value in sorted_dict:
        if word_count < 25:
            small_word_list[key] = value
            word_count = word_count + 1

    print(small_word_list)    

    
    
    return small_word_list

def checkValidPoint(word,count, x, y, pts_list):
    existingWord = 0
    letters = len(word)
    size = (count * 2) + 4


    for word_pt in pts_list:

        pt_x = word_pt.getX()
        pt_y = word_pt.getY()
        rect_x_left = pt_x-(letters/2)
        rect_y_left = pt_y-(size/4)
        rect_x_right = pt_x+(letters/2)
        rect_y_right = pt_y+(size/4)
            
        word_rect = Rectangle(Point(rect_x_left,rect_y_left), Point(rect_x_right,rect_y_right))
        if x > rect_x_left and y > rect_y_left and x < rect_x_right and y < rect_y_right:
            existingWord = existingWord  + 1
        else:
            existingWord = existingWord  + 0


    if existingWord > 0:
        return False
    else:
        return True

def drawWordCloud(counts, word_cloud):
    pts_list =[]
    for key in counts:

        # set text size based on word count
        size = (counts[key] * 2) + 4
            
        # set a random color
        r = randrange(0,256)
        g = randrange(0,256)
        b = randrange(0,256)

        # choose a random location for the text   
        x = randrange(5,95)
        y = randrange(0,100)
        
        draw_words = Text(Point(x,y), key)
        word_pt = draw_words.getAnchor()
        pt_x = word_pt.getX()
        pt_y = word_pt.getY()
        while (checkValidPoint(key, counts[key], pt_x, pt_y, pts_list) == False):
            print(" ")
            print(x,y)
            x = randrange(5,95)
            y = randrange(0,100)
            draw_words = Text(Point(x,y), key)
            word_pt = draw_words.getAnchor()
            pt_x = word_pt.getX()
            pt_y = word_pt.getY()
        pts_list.append(word_pt)
    

        draw_words.setTextColor(color_rgb(r, g, b))
        draw_words.setSize(size)
        draw_words.draw(word_cloud)



main()
