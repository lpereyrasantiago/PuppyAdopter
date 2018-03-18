#! /usr/bin/python3

# Commented Script - Unnecessary unless you didn't follow the raw, prettier script. Only the look_images function have 
# some lines that wouldn't make any sense without a comment.

import os, requests, bs4, random, shelve, shutil

def get_cwd(appended_value): #The function solves the directory flaw of the script (see readme text); get's current directory and
# allows to append a value (in case an specific file of the directory is wanted (line 21, 31 and 36 are examples)).
# The appended_value must be a string; must begin with a "/" symbol (in Windows, "\\") an after contain the name of the
# file of interest. Again: see examples.
    
    cwd = os.getcwd()
    cwd = cwd + appended_value

    return cwd

def create_folder(): # Creates the folder the files will be downloaded to (and printes a cute, unnecessary message!).
    print('Comprobando pelusitas y pulguitas...')
    os.makedirs('Puppies', exist_ok=True)

def download_image(url, request_response):
    local_filename = url.split('/')[-1]
    with open(os.path.join('Puppies', local_filename), 'wb') as f:
        shutil.copyfileobj(request_response.raw, f, [False])

    return local_filename

def create_data_file(): #This function creates a "saves.dat" file on the folder only if that file wasn't created before 
# or existed already.

    if os.path.isfile(get_cwd('/saves.dat')) == False:
        page_files = shelve.open('saves')
        page_files.close()

def save_pages_in_data(saves_list): #This function creates a key value "saves" holding the "saves_list" list, where the downloaded url will be stored, all in the saves.dat file.
        if os.path.isfile(get_cwd('/saves.dat')) == True:
            page_files = shelve.open('saves')
            page_files['saves'] = saves_list
            page_files.close()

def get_random_url(web_object, web_object_number): #This function gets an url and chooses a random
#object (an image) from it.

    while True:
        try:
            random_number = random.randint(0, web_object_number)
            url_variable = web_object[random_number].get('src')
            if not '.jpg' in str(url_variable):
                continue
            elif os.path.isfile(get_cwd('/saves.dat')) == True:
                if str(url_variable) in open('saves.dat', encoding='Latin-1').read():
                    continue
            return url_variable
            break
        except IndexError:
            print('Algo salió mal: reanundando búsqueda...')
            continue

def look_images(pages_list, saves_list): #This is where the magic happens!!

    for i in pages_list:
        res = requests.get(i)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        object = soup.select('img')
        object_number = len(object)

        print("\n Se encontraron {} cachorritos potenciales...".format(int(object_number)))
        print("\n Evaluando colmillitos y patitas...") #This last two are obviously only cute messages...
        image_url = get_random_url(object, object_number)
        print("\n Se encontraron vauitos...")
        print("\n Adoptando cachorrito...")

        if str(image_url).endswith('.jpg 2x'):
            image_url = str(image_url.replace(' ', '')[:-2]) #This if statement responds to the fact that sometimes some files' format ended with
            #" 2x", and the file was broken. Now if the url ends with " 2x", that will be erased, leaving only the ".jpg".
        if not str(image_url).startswith("http"):
            image_url = "https://" + str(image_url) # If missing, adds the initial https string to the url.
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        saves_list.append(str(image_url)) #Adds the requested url to the saves_list, which is later added to the saves.dat file, to store the already downloaded url's.
        download_image(image_url, response)
        print('¡Cachorrito adoptado!')

def get_page(): #This method joins al the other methods together, apart from stating the default web sites to scrap 
# and get the images from.

    pages = ['https://pixabay.com/es/photos/puppy/',
    'https://www.petsworld.in/blog/cute-pictures-of-puppies-and-kittens-together.html',
    'https://pixabay.com/es/photos/bear%20cubs/',
    'https://pixabay.com/es/photos/?q=cute+little+animals&hp=&image_type=photo&order=popular&cat=',
    'https://pixabay.com/es/photos/?q=baby+cows&hp=&image_type=photo&order=popular&cat=',
    'https://www.boredpanda.com/cute-baby-animals/']

    alr_dow = [] #alr_dow stands for "already downloaded"; in this list, the downloaded url's will be appended (see line 62 of the look_images function).

    create_folder()
    create_data_file()
    look_images(pages, alr_dow)
    save_pages_in_data(alr_dow)

get_page()