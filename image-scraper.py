# Import the function for downloading web pages
from urllib import urlopen

# Import the regular expression function
from re import findall

# Import the Tkinter functions
from Tkinter import *


# Import a constructor for converting byte data to character strings 
from StringIO import StringIO

# Import the Python Imaging Library module (comment this line out
# if you do not intend to use PIL in your solution)
from PIL import Image, ImageTk



##### DEVELOP YOUR SOLUTION HERE #####
url = 'http://www.wired.com/category/business/feed/' # Put your web page address here

#-----
# Open the gallery URL
picture_source = urlopen(url)

#-----
# Extract the web page's content as a string
html_code = picture_source.read()

#----
# Close the connection to the web server
picture_source.close()


#----
# A Regular expression that searches for the specified img tags
# in the RSS feed.
img_urls = findall('img src="([^"]*.jpg[^"]*)"[^>]*>', html_code)

#----
# This replaces all the new lines and tabs with nothing
# This is important as when the description is seen
# it will not contain something like:
# "Microsoft&#8217;s Windows 10 Vision Isn&#8217;t \n\tas Simple as It Seems"
new_html = html_code.replace('\n','')
new_html = new_html.replace('\t','')
new_html = new_html.replace('&#8217;','\'')
new_html = new_html.replace('&#8216;','\'')
new_html = new_html.replace('â€”','-')


#----
# This regular expression searches the HTML for a phrase involving
# the <item> tag which specifies where an image is, and then the <title>
# tag to grab the title of the post.
# This will arrange all the descriptions in a list.
descriptions = findall('<item><title>(.*?)</title>', new_html)

dates = findall('<pubDate>(.*?)</pubDate>', new_html)

position = 0
#print len(descriptions)
for image in img_urls:
    
    print image

    if position < len(descriptions):
        print descriptions[position]
        print dates[position]
        if position <=20:
            position += 1
            
    elif position >=21 :
        print "This image has no description"
    print



root = Tk()
root.geometry("900x450")
# This variable is used to keep track of the position in the
# img_urls list and descriptions list.
pos = 0

####################
# Button Functions #
####################

# Next img function
def next_img():
    global pos

    #Position of the list +1 so receive the next image
    pos +=1
    # So the user can loop through the lists and be returned to
    # the begining when they reach the final image.
    if pos >=10:
        pos = 0

    # The image that will be used, as determined by the position
    url = img_urls[pos]

    # Encoding the image so it can be displayed
    image = urlopen(url).read()
    data = StringIO(image)
    displayable_image = Image.open(data)

    resized_img = displayable_image.resize(img_size, Image.ANTIALIAS)
    
    final_img = ImageTk.PhotoImage(resized_img)
    
    # Changing the despcription text and updating the image
    # label to display the next image/description
    pub_date["text"] = dates[pos]
    image_description["text"] = text=str(pos+1) + "/" + str(len(img_urls)) +": " + descriptions[pos]
    display_image.configure(image = final_img)
    display_image.image = final_img

# The previous image function  
def prev_image():
    global pos
    # Position of the list is now -1 to view the previous image
    pos -=1
    # So the user can loop through the lists and be returned to
    # the begining when they reach the final image.
    if pos < 0:
        pos = 9
        
    # The image that will be used, as determined by the position
    url = img_urls[pos]

    # Encoding the image so it can be displayed
    image = urlopen(url).read()
    data = StringIO(image)
    displayable_image = Image.open(data)
    resized_img = displayable_image.resize(img_size, Image.ANTIALIAS)
    final_img = ImageTk.PhotoImage(resized_img)
    
    # Changing the despcription text and updating the image
    # label to display the next image/description
    pub_date["text"] = dates[pos]
    image_description["text"] = text=str(pos+1) + "/" + str(len(img_urls)) +": " + descriptions[pos]
    display_image.configure(image = final_img)
    display_image.image = final_img

##################
# Image Encoding #
##################


# Open the first image to display to the user on open
url = img_urls[pos]
#Read the Image
image = urlopen(url).read()

#Unencode the image using StrinIO
#this enables Tkinter to display the image.
data = StringIO(image)

#This uses the PIL package to read the data as an image
displayable_image = Image.open(data)

# This keeps the image ratio, but moves the buttons around the screen
# Makes the gui hard to use and isn't a good user experience
'''max_size = 600
img_size = min(max_size/displayable_image.size[0], max_size/displayable_img.size[1])
resized_img = displayable_image.resize((int(displayable_image.size[0] * img_size), int(displayable_image.size[1] * img_size)), Image.ANTIALIAS)'''


# this solution doesn't keep the ratio, but works for 8 or 9 out of 10 times
# This stops buttons moving around the screen, so the use can use the GUI properly
img_size = (500, 300)

resized_img = displayable_image.resize(img_size, Image.ANTIALIAS)

# Set frame title
frame_name = "Wired News"
root.title(frame_name)

# convert PIL image to Tkinter PhotoImage so it can be displayed
final_img = ImageTk.PhotoImage(resized_img)



###########
# Widgets #
###########

# Display a title
heading = Label(root, text="Wired Business News", font=("Myriad Pro", 24))
heading.grid(row=0, column = 0)

pub_date = Label(root, text = dates[pos], font=("Arial", 12))
pub_date.grid(row=1, column = 0)
# display the image in a label widget
display_image = Label(root, image=final_img, bg='blue')
display_image.grid(row=2)

# display the relevant description for the image being displayed
image_description = Label(root, width = 100, text=str(pos+1) + "/" + str(len(img_urls)) +": " + descriptions[pos], font=("Arial", 12))
image_description.grid(row=3, column = 0)

# The next button so users can see more photos
next_btn = Button(root, text="Next", command = next_img, width = 20, height=1)
next_btn.grid(row=4, column = 0, padx=(200,10))

# The back button so users can see previous photos
back_btn = Button(root, text="Previous", command = prev_image, width = 20, height=1)
back_btn.grid(row=4, column = 0, padx=(10, 200))


root.mainloop() 



#
#--------------------------------------------------------------------#
