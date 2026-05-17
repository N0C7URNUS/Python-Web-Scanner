#  >-Imports-<
import os   #   Imports the os library for interaction with the operating system.
import requests   #   Imports the requests library for web interaction.
from bs4 import BeautifulSoup   #   Imports BeautifulSoup module from bs4 library for html handling.
from urllib.parse import urljoin, urlparse,urlsplit   #   Imports a number of functions urllib.parse library for URL parsing and handling.
from pathlib import Path   #   Imports Path module from pathlib library for path parsing and handling.
from collections import deque   #   Imports deque function from collections library for queue creation.
from typing import Iterable   #   Imports Iterable function from typing library for the link extracting function creation.

#  >-Main Variables-<
User_URL = input("""[Request]: Please enter the domain name
Example: example.com or example.co.il etc...
Your URL:  [Enter here]  """).strip()   #   Takes an input from the user of a domain name and cleans it form accidental spaces/newlines
Base_URL = f"http://{User_URL}/"   #   Converts the user's input to a URL
Final_URL = ""   #   Being set by Detect_www() as the final URL
Max_Links = 2500   #   Maximum amount of links allowed in a list
Max_Queue = 5000   #   Maximum amount of links allowed in the queue
Download_Num = 0   #   Changes the name of file to prevent duplicates error while downloading

#  >--Directories names--<
Main_dir = f"{User_URL}"   #   Sets the name of the main directory that will be created of the downloads
Docs_dir = f"{User_URL}-Docs"   #   Sets the name of the Docs directory that will be created of the downloads
Images_dir = f"{User_URL}-Images"   #   Sets the name of the Images directory that will be created of the downloads
Audio_dir = f"{User_URL}-Audio"   #   Sets the name of the Audio directory that will be created of the downloads
Videos_dir = f"{User_URL}-Videos"   #   Sets the name of the Videos directory that will be created of the downloads
Archives_dir = f"{User_URL}-Archives"   #   Sets the name of the Archives directory that will be created of the downloads
Code_dir = f"{User_URL}-Code"   #   Sets the name of the main Code that will be created of the downloads

#  >--Directories's Paths--<
Home_path = os.path.expanduser("~")   #   Gets the user's home directory path
Main_dir_path = os.path.join(Home_path, "Documents", User_URL)   #   Creates the path of the main directory that will be created
Docs_dir_path = os.path.join(Main_dir_path, Docs_dir)   #   Creates the path of the Docs directory that will be created
Images_dir_path = os.path.join(Main_dir_path, Images_dir)   #   Creates the path of the Images directory that will be created
Audio_dir_path = os.path.join(Main_dir_path, Audio_dir)   #   Creates the path of the Audio directory that will be created
Videos_dir_path = os.path.join(Main_dir_path, Videos_dir)   #   Creates the path of the Videos directory that will be created
Archives_dir_path = os.path.join(Main_dir_path, Archives_dir)   #   Creates the path of the Archives directory that will be created
Code_dir_path = os.path.join(Main_dir_path, Code_dir)   #   Creates the path of the Code directory that will be created

#  >--Defined Suffixes Tuples--<
Docs_Suf = (".txt", ".md", ".doc", ".docx", ".odt", ".rtf", ".pdf", ".csv", ".tsv", ".xlsx", ".ods", ".pptx", ".odp", ".ppt", ".xls")   #   Defines the Docs suffixes to look for
Images_Suf = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".svg", ".webp", ".ico")   #   Defines the Images suffixes to look for
Audio_Suf = (".mp3", ".wav", ".ogg", ".m4a", ".flac")   #   Defines the Audio suffixes to look for
Videos_Suf = (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpg", ".mpeg")   #   Defines the Videos suffixes to look for
Archives_Suf = (".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz", ".tar.bz2", ".tar.xz")   #   Defines the Archives suffixes to look for
Code_Suf  = (".js", ".css", ".json", ".xml", ".yml", ".yaml")   #   Defines the Code suffixes to look for

#  >--Links Lists--<
Links_Queue = deque(set())   #   A deque as the links queue - to remove links for the start easily
Visited = set()   #   A set a list for all links that has been visited to prevent visiting them again thus creating an infinite loop
External_links = set()   #   A set that collects all external links - links that don't have the original domain name. Those links won't be visited, but documented
Docs_links = set()   #   A set that collects all documents links for later download
Images_links = set()   #   A set that collects all images  links for later download
Audio_links = set()   #   A set that collects all Audio links - Those links won't be downloaded, but documented
Videos_links = set()   #   A set that collects all video links - Those links won't be downloaded, but documented
Archives_links = set()   #   A set that collects all archives links for later download
Code_links = set()   #   A set that collects all code related links - Those links won't be downloaded, but documented
Failed_Downloads = set()   #   A set that collects all links that the code failed to download - Those links would be documented

#  >-Functions-<
def Do_Nothing():   #   A function that do nothing and meant to be a fill in
    pass   #   Acts as placeholder

def Detect_www(URL: str):   #   detect if the website requires a www in the URL   #(URL:str) tells the function to expect a string
    global Final_URL   #   Allows the function to overwrite an existing variable
    print("[Notice]: Checking for www requirement\n")   #   Informs the user
    try:   #   tries to execute the following code
        www_check = session.get(URL, allow_redirects=True, timeout=(10, 45))   #   Sends a request for a given URL and if it gets a redirect response it allows an automatic redirection
        www_check.raise_for_status()   #   Automatically treats any non-2xx response as an error
    except:   #   if wasn't able to execute the code, then
        print(f"[Error | Connection]: Could not reach {URL}")   #   Informs the user
        Final_URL = URL   #   Sets the given URL as the final URL for the website
        return   #   Exits the function is case of an error
    Final_URL = www_check.url.rstrip("/") + "/"   #   Sets the final URL for the website and cleans from extra "/"
    print(f"[Notice]: The final URL is: {Final_URL}\n")   #   Informs the user

def Domain_Filter(URL: str) -> bool:  # Filters links found to internal and external by comparing domain names  #(URL:str) tells the function to expect a string   # -> bool tells the function to output a bool value
    Base_netloc = urlparse(Final_URL).netloc   #Defines the base domain name
    Temp_netloc = urlparse(URL).netloc   #Defines the current URL's domain name
    return Base_netloc == Temp_netloc   # Returns True of False

def Add_to_Set(list: set, item: str):   #   Adds an item to a list (set)   #   (list: set, item: str): Tell the function to expect a set for the list and string for the item
    if len(list) < Max_Links:   #   Blocks adding an item if the list is in maximum capacity
        list.add(item)   #   Adds the item to the list
    else:
        print(f"[Error | Capacity]: The list - {list} is in maximum capacity\nThe item - {item} hasn't been added to {list}\n")   #   Informs the user the item hasn't been added due to full capacity of the list

def Add_to_Deque(list: deque, item: str):   #   Adds an item to the queue (deque)   #   (list: set, item: str): Tell the function to expect a deque for the list and string for the item
    if len(list) < Max_Queue:   #   Blocks adding an item if the queue is in maximum capacity
        list.append(item)   #   Adds the item to the queue
    else:
        print(f"[Error | Capacity]: Queue at maximum capacity; not enqueuing {item}\n") #   Informs the user the item hasn't been added due to full capacity of the queue

def Classifier(URL: str):   #   Classifies each link found - first by suffix then by known and unknown
    Suffix = Path(urlparse(URL).path).suffix.lower()   #   Set a variable that equals to the new URL's suffix. Path() = treats a string as a path. urlparse(URL).path = extracts the path part of the URL. .suffix = return only the file's suffix (extension). .lower = sets the final string value to low characters.
    if Suffix in Docs_Suf:   #   if the URL's suffix exists in the predefined docs suffixes
        if URL not in Docs_links:   #   if the URL isn't already in the docs links list
            Add_to_Set(Docs_links, URL)   #   then add the URL to the docs links list
            print(f"[Notice]: \n{URL} \nHas been added to Docs_links\n")   #   and finally, inform the user
    elif Suffix in Images_Suf:   #   if the URL's suffix exists in the predefined images suffixes
        if URL not in Images_links:   #   if the URL isn't already in the images links list
            Add_to_Set(Images_links, URL)   #   then add the URL to the images links list
            print(f"[Notice]: \n{URL} \nHas been added to Images_links\n")   #   and finally, inform the user
    elif Suffix in Audio_Suf:   #   if the URL's suffix exists in the predefined audio suffixes
        if URL not in Audio_links:   #   if the URL isn't already in the audio links list
            Add_to_Set(Audio_links, URL)   #   then add the URL to the audio links list
            print(f"[Notice]: \n{URL} \nHas been added to Audio_links\n")   #   and finally, inform the user
    elif Suffix in Videos_Suf:   #   if the URL's suffix exists in the predefined video suffixes
        if URL not in Videos_links:   #   if the URL isn't already in the video links list
            Add_to_Set(Videos_links, URL)   #   then add the URL to the video links list
            print(f"[Notice]: \n{URL} \nHas been added to Videos_links\n")   #   and finally, inform the user
    elif Suffix in Archives_Suf:   #   if the URL's suffix exists in the predefined archives suffixes
        if URL not in Archives_links:   #   if the URL isn't already in the archives links list
            Add_to_Set(Archives_links, URL)   #   then add the URL to the archives links list
            print(f"[Notice]: \n{URL} \nHas been added to Archives_links\n")   #   and finally, inform the user
    elif Suffix in Code_Suf:   #   if the URL's suffix exists in the predefined codes suffixes
        if URL not in Code_links:   #   if the URL isn't already in the codes links list
            Add_to_Set(Code_links, URL)   #   then add the URL to the codes links list
            print(f"[Notice]: \n{URL} \nHas been added to Code_links\n")   #   and finally, inform the user
    else:   #   if none of the above happened then
        if Suffix not in (Docs_links, Images_links, Audio_Suf, Videos_Suf, Archives_links, Code_Suf):   #   if the URL's suffix isn't in any of the predefined suffixes lists
            if URL in Visited:   #   if the URL in the visited list
                Do_Nothing()   #   do nothing
            elif URL in Links_Queue:   #   if the URL in the links queue list
                Do_Nothing()   #   do nothing
            else:   #   if none of the above happened then
                Add_to_Deque(Links_Queue, URL)   #   Add the link to the links queue
                print(f"[Notice]: \n{URL}\nHas been added to Links_Queue\n")   #   and finally, inform the user

def File_Name_Cleaner(Name: str) -> str:   #Cleans the name of file from illegal characters   #(URL:str) tells the function to expect a string   # -> str: tells the function to output a string value as a kind of failsafe
    global Download_Num   #   Allows the function to overwrite an existing variable
    Download_Num += 1   #   Changes the value of Download_Num to prevent duplicates
    Result_Characters = []   #   Collects the legal characters
    for c in Name:   #   Loops over each character in the given name
        if c not in '<>:"/\\|?*':   #   Keeps only legal characters and remove illegal ones
            Result_Characters.append(c)   #   Append the current character to Result_Characters list

    Cleaned_Name = "".join(Result_Characters).strip()   #   Joins the characters into a string and cleans it form accidental spaces/newlines
    return Cleaned_Name or f"Download{Download_Num}"   #   Returns a value equals either to the clean name or an alternative name

def Downloader(list: set, dir_path: str, session: requests.Session):   #   Downloading the files. #list: set - tells the function to expect a set # dir_path: str - tells the function to expect a string #session: requests.Session tells the function to expect a certain variable
    for link in list:   #   for each link in a given list
        try:   #   tries to execute the following code
            Page = session.get(link, stream=True, timeout=(5, 30))   #   try to connect to the link #stream=True - reads the links content in chunks instead of everything at once #timeout=(5, 30) - sets timeouts (maximum time to establish a TCP connection, maximum time to wait for a server response (per chunk of data because stream=True)
            if Page.status_code != 200:   #   if the page's status code isn't equal to 200 (OK)
                Add_to_Set(Failed_Downloads, link)   #   add the URL to the failed downloads file
                print(f"[Error | Connection]: Couldn't get to \n{link}\n Download attempt failed\n")   #   Informs the user
                continue   #   skips the rest of the function
            else:   #   if the page's status code does equal to 200 (OK)
                try:   #   tries to execute the following code
                    File_Name = os.path.basename(urlsplit(link).path)   #   Extract the name of the file #os.path - the module #.basename - extracts the last part from a given path string #urlsplit(link) - splits it into its components #.path returns only the path portion of the URL
                    File_Name = File_Name_Cleaner(File_Name)   #   Takes the extracted name and cleans it from illegal characters using the predefined File_Name_Cleaner() function
                    File_Path = os.path.join(dir_path, File_Name)   #   Joins the file name with the relevant path #os.path - the module #.join - join given parts into a valid path string
                    New_File = open(File_Path, "wb")   #   Creates the new file in the relevant location and opens it with permissions for writing binary to enable any kind for contant
                    for chunk in Page.iter_content(chunk_size=1024 * 32):   #   for each chunk in the content of page #Page - the response #.iter_content - iterate over the response data in pieces (relevant since stream=True) #(chunk_size=1024 * 32) - define the size of each chunk of data
                        if chunk:   #   if chunk contains data it equals to True and the condition is met,  if chunk doesn't contain data it equals to False and the condition isn't met
                            New_File.write(chunk)   #   writes the chunk of data into the file
                    New_File.close()   #   at the end of the loop, close the file
                    print(f"[Notice]: Downloaded {link} \nto {dir_path} \nas {File_Name}\n")   #   Informs the user
                except:   #   if wasn't able to execute the code, then
                    Add_to_Set(Failed_Downloads, link)   #   Add the link to the Failed downloads list
                    print(f"[Error]: Failed to download\n {link}\n")   #   Informs the user
        except:   #   if wasn't able to execute the code, then
            Add_to_Set(Failed_Downloads,link)   #   Add the link to the Failed downloads list
            print(f"[Error]: Failed to download\n {link}\n")   #   Informs the user


def Extract_Links(html_content: BeautifulSoup, Final_URL: str) -> Iterable[str]:   #   link extractor #html_content: BeautifulSoup - tells the function to expect a parsed html content #Final_URL: str - tell the function to expect a string # tell the function to produces an iterable of strings (to output multiple strings but one by one)
    Tags_and_Values = (("a", "href"), ("link", "href"), ("img", "src"), ("script", "src"), ("video", "src"), ("audio", "src"), ("source", "src"))   #   Creates a tuple of pairs to search for
    for Tag, Value in Tags_and_Values:   #   for each tag and value in the tuple above
        for tag in html_content.find_all(Tag):   #   for each tag found by find_all function used on the html content
            Link = tag.get(Value)   # get the value of the tag
            if not Link or not Link.startswith(("http", "/")):   #   if the tag didn’t have the relevant value and the link doesn’t look like a proper URL or relative path
                continue   #   skips the rest of the function
            Abs_url = urljoin(Final_URL, Link)   #   uses urljoin to properly combine the original URL with the found link
            yield Abs_url   #   return/output one URL at a time

def Links_File(List: set, Path: str, Name: str):   #   Creates a file with the links from the given list #List: set - tell the function to expect a set#Path: str - tell the function to expect a string #Name: str - tell the function to expect a string
    File_Name = os.path.join(Path,Name)   #   Joins the file name with the relevant path #os.path - the module #.join - join given parts into a valid path string
    File = open(File_Name, "a", encoding="utf-8")   #
    print(f"[Notice]: Created {Name} file")   #   Informs the user
    File.write(f">-----{Name}-----<\n")   #   adds a title inside the file
    try:   #   tries to execute the following code
        if len(List) == 0:   # if the length of the list equals to 0
            File.write("Empty list")  #   write in the file "Empty list"
        else:   #   if the length of the list doesn't equal to 0
            for link in List:   #   for every link in the list
                File.write(link)   #   write the link in the file
                File.write("\n")   #   write in file "\n" - go down a row
    except:   #   if wasn't able to execute the code, then
        print("[Error]: Couldn't edit file")   #   Informs the user
    File.close()   #   close the file
    print("[Notice]: Finished editing file; File closed")   #   Informs the user

#   >-The Crawler-<
#   >--Web Interaction--<
session = requests.Session()   #   sets a session request
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"})   #   Updates the session request User-Agent Header
Detect_www(Base_URL)   #   Check for www requirement and define the value of Final_URL (var) as the final URL for the website
Website = session.get(Final_URL, timeout=(5, 45))   #   sends a conaction request to the Final URL, sets a variable as its response and defines a timeouts (maximum time to establish a TCP connection, maximum time to wait for a server response (per chunk of data because stream=True)
if Website.status_code == 200:   #   if the page's status code equals to 200 (OK)
    print(f"[Notice]: Reached\n {Final_URL}\n")   #   Informs the user
else:   #   if the page's status code isn't equal to 200 (OK)
    print(f"[Error | Connection]: Couldn't reach\n {Final_URL}\n")   #   Informs the user

#   >---Website Parsing---<
html_content = Website.text   #   Defines a variable and sets its value as the website's html content
Content = BeautifulSoup(html_content,"html.parser")   #   uses beautifulsoup to "call" fot a html "parsing engine"

#   >---First Links Extraction---<
for Abs_URL in Extract_Links(Content, Final_URL):   #   for every absolute URL extracted by Extract_Links
    #   >-----Check if the link is internal or external-----<
    if not Domain_Filter(Abs_URL):   # If domain name is different (external)
        Add_to_Set(External_links, Abs_URL)   # Adds to External_links list
    elif Domain_Filter(Abs_URL):   # If domain name is the same (internal)
        Classifier(Abs_URL)   # Classify the URL to the correct list
Visited.add(Final_URL)   #   adds Final_URL (the original domain) to the visited list


while Links_Queue:   # While there are links in Links_Queue, run
    Temp_URL = Links_Queue.popleft()   #Removes the first link in Links_Queue
    if Temp_URL in Visited: # If the link already been visited, continue to the next one
        continue   #   skips the rest of the code and "restart" the loop
    Visited.add(Temp_URL) # Adds the current URL to Visited
    print(f"[Notice]: Attempting the next URL in queue") #    Informs the user
    try:   #   tries to execute the following code
        Temp_Website = session.get(Temp_URL, timeout=(5, 45))   #
        if Temp_Website.status_code != 200:   #   if the page's status code isn't equal to 200 (OK)
            print(f"[Error | Connection]: Couldn't reach\n {Temp_URL}\nContinued to the next one")   #   Informs the user
            continue   #   skips the rest of the code and "restart" the loop
        else:   #   if the page's status code equals to 200 (OK)
            print(f"[Notice]: Attempt was successful; Reached\n {Temp_URL}")   #   Informs the user

        Temp_html_content = Temp_Website.text   #   Define a variable and sets it value to be the current URL's content
        Temp_content = BeautifulSoup(Temp_html_content, "html.parser")   #   uses beautifulsoup to "call" fot a html "parsing engine"

        for Abs_URL in Extract_Links(Temp_content, Temp_URL):   #   for every absolute URL extracted by Extract_Links
            #   >-----Check if the link is internal or external-----<
            if not Domain_Filter(Abs_URL):  # If domain name is different (external)
                Add_to_Set(External_links, Abs_URL)  # Adds to External_links list
            elif Domain_Filter(Abs_URL):  # If domain name is the same (internal)
                Classifier(Abs_URL)  # Classify the URL to the correct list
        print(f"[Notice]: Finished; Moving on\n")   #   Informs the user


    except:   #   if wasn't able to execute the code, then
        print("[Error]: ")   #   Informs the user

#   >--Downloading the Content--<
#  >--Directory Creation--<
for path in [Main_dir_path, Docs_dir_path, Images_dir_path, Audio_dir_path, Videos_dir_path, Archives_dir_path, Code_dir_path]:   #   for evey predefined path in the list
    os.makedirs(path, exist_ok=True)   #   create a new directory #exit_ok=True - if there is already a directory it's ok and don't create a new one
    print(f"[Notice]: {path} has been created")   #   Informs the user

print("\n[Notice]: Starting to download\n")   #   Informs the user
print("\n[Notice]: Downloading docs\n")   #   Informs the user
Downloader(Docs_links, Docs_dir_path, session)   #   Uses the Downloader function from above to download the content of a given list, into a given path, and uses the same session conaction
print("\n[Notice]: Finished downloading docs\n")   #   Informs the user
print("\n[Notice]: Downloading images\n")   #   Informs the user
Downloader(Images_links, Images_dir_path, session)   #   Uses the Downloader function from above to download the content of a given list, into a given path, and uses the same session conaction
print("\n[Notice]: Finished downloading images\n")   #   Informs the user
print("\n[Notice]: Downloading archives\n")   #   Informs the user
Downloader(Archives_links, Archives_dir_path, session)   #   Uses the Downloader function from above to download the content of a given list, into a given path, and uses the same session conaction
print("\n[Notice]: Finished downloading archives\n")   #   Informs the user
print("\n[Notice]: Downloading codes\n")   #   Informs the user
Links_File(Code_links, Code_dir_path, "Code_Links_File.txt")   #   Creates a file containing all the links from a given list, into a path, with a given name
print("\n[Notice]: Finished downloading codes\n")   #   Informs the user
print("\n[Notice]: Downloading audio\n")   #   Informs the user
Links_File(Audio_links,Audio_dir_path,"Audio_Links_File.txt")   #   Creates a file containing all the links from a given list, into a path, with a given name
print("\n[Notice]: Finished downloading audio\n")   #   Informs the user
print("\n[Notice]: Downloading videos\n")   #   Informs the user
Links_File(Videos_links,Videos_dir_path,"Video_Links_File.txt")   #   Creates a file containing all the links from a given list, into a path, with a given name
print("\n[Notice]: Finished downloading videos\n")   #   Informs the user
print("\n[Notice]: Downloading External_links\n")   #   Informs the user
Links_File(External_links,Main_dir_path,"External_Links_File.txt")   #   Creates a file containing all the links from a given list, into a path, with a given name
print("\n[Notice]: Finished downloading External_links\n")   #   Informs the user
print("\n[Notice]: Downloading Failed_Downloads\n")   #   Informs the user
Links_File(Failed_Downloads,Main_dir_path,"Failed_Downloads_Links_File.txt")   #   Creates a file containing all the links from a given list, into a path, with a given name
print("\n[Notice]: Finished downloading Failed_Downloads\n")   #   Informs the user

print("\n-----PROGRAM FINISHED-----\n")   #      Informs the user



















