# zim-auto-linker
Hello! This is a plugin I wrote to automatically link to specified pages.

## How it works
Throughout this document, I will be using the example of a notebook created to organized the elements of a story. We will be working specifically with the characters.

So, imagine you have a page, Characters. On this page, you have a list of all the story's characters, let's say "Bob", "Sandy", and "Michael".
You have them listed on the page like this:
~~~
+Bob    
+Sandy     
+Michael 
~~~

Zim automatically links them, of course. In the source, it looks like this:
```
[[+Bob]]
[[+Sandy]]
[[+Michael]]
```
The plugin takes the source file and parses it for the right format and extracts the names. Then, every time you end a word (via spaces, tabs, new lines, etc.), it first "cleans" the word, getting rid of any puncuation, then sends it through the list of names to see if there are any matches. If there is one, it will replace the word with the link (preserving your punctuation, don't worry).

#### Example time!
A sentence like this: "Bob, Michael, and Sandy went to the store."
will get turned into this (bold is link): "__Bob__, __Michael__, and __Sandy__ went to the store."

In the source, it looks like:
~~~
"[[Characters:Bob|Bob]], [[Characters:Michael|Michael]], and [[Characters:Sandy|Sandy]] went to the store."
~~~
Cool, right?
Of course, it doesn't just magically start working. You have to set it up. (:() Let's get into how to do that.

## Setup

So let's say the notebook is named Story, and it's set up like this.
```
> Planning
> > Characters
> > > Bob
> > > Michael
> > > Sandy
> > Plot
> Writing
> > CHapter One
> > Snippets
```
In the plugin file, there is a function called link_collector. Find it. This is where you'll be doing most if not all of your customization.
```
def link_collector(self, notebook): #you'll probably just want to read the github page for this
  linklist = {}
  if notebook == "Notebook": #change this to your notebook name
    f = open("") #path to the parent page text file (use slashes, not colons)
    for line in f.read().splitlines():
      if line[:3] == '[[+' and line[-2:] == ']]': #I'm assuming you just have a list of pages linked like [[+Name]]. If not, correct it.
      linklist[line[3:-2]] = "" + line[3:-2] #the path where the pages that will be linked to are (colons this time)
		return linklist
```

---

The first line you need to change is this:
```
if notebook == "Notebook": #change this to your notebook name
```
Pretty simple. There we go:
```
if notebook == "Story": #change this to your notebook name
```

---

Next line gets a little more complicated.
```
f = open("") #path to the parent page text file (use slashes, not colons)
```
So, it's looking for the actual filepath, like the one you would navigate to with a file manager. Luckily, it follows the same folder structure as the notebook index. 
```
f = open("Notebooks/Story/Planning/Characters.txt") #path to the parent page text file (use slashes, not colons)
```
(make sure the first folder is Notebooks, and it ends with a .txt file)

---

This line is similar to the last one.
```
linklist[line[3:-2]] = "" + line[3:-2] #the path where the pages that will be linked to are (colons this time)
```
It's going to be used to tell zim where to link to.
```
linklist[line[3:-2]] = "Planning:Characters:" + line[3:-2] #the path where the pages that will be linked to are (colons this time)
```
It just adds the page name to the end, so make sure it ends in a colon.

---

Our finished product:
```
def link_collector(self, notebook): #you'll probably just want to read the github page for this
  linklist = {}
  if notebook == "Story": #change this to your notebook name
    f = open("") #path to the parent page text file (use slashes, not colons)
    for line in f.read().splitlines():
      if line[:3] == '[[+' and line[-2:] == ']]': #I'm assuming you just have a list of pages linked like [[+Name]]. If not, correct it.
        linklist[line[3:-2]] = "Planning:Characters:" + line[3:-2] #the path where the pages that will be linked to are (colons this time)
  return linklist
```

It should work now! Go ahead and test it out! If you have multiple notebooks you want it to work in, or multiple pages you want to read from, continue reading.

### Multiples
This is pretty simple. If you want to add another notebook, simply copy the ```if notebook == "Notebook":``` statement and everything in it, then paste it below and change the "if" to an "elif". Example:
```
def link_collector(self, notebook): #you'll probably just want to read the github page for this
  linklist = {}
    
  if notebook == "Notebook": #change this to your notebook name
    f = open("") #path to the parent page text file (use slashes, not colons)
    for line in f.read().splitlines():
      if line[:3] == '[[+' and line[-2:] == ']]': #I'm assuming you just have a list of pages linked like [[+Name]]. If not, correct it.
        linklist[line[3:-2]] = "" + line[3:-2] #the path where the pages that will be linked to are (colons this time)
          
  elif notebook == "Notebook": #change this to your notebook name
    f = open("") #path to the parent page text file (use slashes, not colons)
    for line in f.read().splitlines():
      if line[:3] == '[[+' and line[-2:] == ']]': #I'm assuming you just have a list of pages linked like [[+Name]]. If not, correct it.
        linklist[line[3:-2]] = "" + line[3:-2] #the path where the pages that will be linked to are (colons this time)
          
  return linklist
```
If you then wanted to add another page to one of them, do the same thing with the ```f = open("")``` and the for loop. Like this:
```
def link_collector(self, notebook): #you'll probably just want to read the github page for this
  linklist = {}
    
  if notebook == "Notebook": #change this to your notebook name
    
    f = open("") #path to the parent page text file (use slashes, not colons)
    for line in f.read().splitlines():
      if line[:3] == '[[+' and line[-2:] == ']]': #I'm assuming you just have a list of pages linked like [[+Name]]. If not, correct it.
        linklist[line[3:-2]] = "" + line[3:-2] #the path where the pages that will be linked to are (colons this time)
          
    f = open("") #path to the parent page text file (use slashes, not colons)
    for line in f.read().splitlines():
      if line[:3] == '[[+' and line[-2:] == ']]': #I'm assuming you just have a list of pages linked like [[+Name]]. If not, correct it.
        linklist[line[3:-2]] = "" + line[3:-2] #the path where the pages that will be linked to are (colons this time)
          
  elif notebook == "Notebook": #change this to your notebook name
    f = open("") #path to the parent page text file (use slashes, not colons)
    for line in f.read().splitlines():
    if line[:3] == '[[+' and line[-2:] == ']]': #I'm assuming you just have a list of pages linked like [[+Name]]. If not, correct it.
      linklist[line[3:-2]] = "" + line[3:-2] #the path where the pages that will be linked to are (colons this time)
          
  return linklist
```

### Restriction
Let's say you have a page you don't want it to link from. (like Characters, for example. That could get messy very quickly and would break the plugin.) Go to the on_end_of_word function and change it from this:
```
def on_end_of_word(self, textview, start, end, word, char, editmode): #If you don't want it to work on certain pages, this is where you do that.
  buffer = textview.get_buffer() 
	links = self.link_collector(buffer.notebook.name)
	clean_word, prefix, suffix = clean(word)
	if clean_word in links.keys():
		buffer.delete(start, buffer.get_insert_iter())
		buffer.insert_at_cursor(prefix)
		buffer.insert_link_at_cursor(clean_word, links[clean_word])
		buffer.insert_at_cursor(suffix + ' ')
		buffer.set_modified(True)
		textview.stop_emission('end_of_word')
```
to this:
```
def on_end_of_word(self, textview, start, end, word, char, editmode): #If you don't want it to work on certain pages, this is where you do that.
  buffer = textview.get_buffer() 
  if not(buffer.page.basename == "Characters"):
    links = self.link_collector(buffer.notebook.name)
    clean_word, prefix, suffix = clean(word)
    if clean_word in links.keys():
      buffer.delete(start, buffer.get_insert_iter())
      buffer.insert_at_cursor(prefix)
      buffer.insert_link_at_cursor(clean_word, links[clean_word])
      buffer.insert_at_cursor(suffix + ' ')
      buffer.set_modified(True)
      textview.stop_emission('end_of_word')
```
Use "name" if you have multiple pages with the same name and want to specify which one. Otherwise, "basename" is fine. (basename of Characters is "Characters", but name is "Planning:Characters")
