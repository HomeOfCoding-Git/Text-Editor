# iNote
# Text Editor (version 0.1)
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser

# App Window
app = Tk()
app_title = 'iNote'
win_size = '680x640+0-33'

# Page Defaults
bg_color = '#fff'
fg_color = '#296296'
title_font = 'arial, bold', 14
text_font = 'arial', 12
status_bar_font = 'arial', 8
# Select Text Color (mouse grab)
sel_fg_color = '#ff0000'
sel_bg_color = '#ddd'

# Globals
# (open_status_name is get_file)
# (filepath) with (filename.ext)..
global open_status_name
open_status_name = False
# Cut / Copy / Paste
global selected
selected = False

# _____________________________________
# Functions

# New File
def new_file():

    # Clear Text Area
    textarea.delete('1.0', END)
    # Update App Title
    app.title(f'{app_title}: New File')
    # Update Status bar
    status_bar.config(text=f'{app_title}: New File')

    global open_status_name
    open_status_name = False


# Open File
def open_file():

    # Clear Text Area
    textarea.delete('1.0', END)

    # Grab Filename
    get_file = filedialog.askopenfilename(\
        # Create a path to where you would like your notes to be saved to.
        # Example path: initialdir='C:/change/to/where/you/prefer'
        initialdir='C:/Users/You/Desktop/iNotes', \
        title=f'{app_title}: Open File', \
        filetypes=(('Text Files', '*.txt'), \
        ('HTML Files', '*.html'), \
        ('Python Files', '*.py'), \
        ('All Files', '*.*')))

    if get_file:
        global open_status_name
        open_status_name = get_file
        
        # Update Status bar
        name = get_file
        status_bar.config(text=f'{app_title}: {name}')
        # Remove the ugly file path..
        # Just show the file name in the window title
        name = name.replace('C:/Users/You/Desktop/iNotes/', '')
        app.title(f'{app_title}: {name}')

        # Open File
        with open(get_file) as f_read:
            show_file = f_read.read()


        textarea.insert(END, show_file)


# Save File
def save_file():
    global open_status_name
    
    if open_status_name:

        # Write to File
        with open(open_status_name, 'w') as f_write:
            f_write.write(textarea.get(1.0, END))


        status_bar['text'] = f'{app_title} Saved: {open_status_name}'
    else:
        save_as_file()


# Save As File
def save_as_file():

    # Save As Filename
    get_file = filedialog.asksaveasfilename(\
        defaultextension='.*', \
        initialdir='C:/Users/You/Desktop/iNotes', \
        title=f'{app_title}: Save File', \
        
        filetypes=(('Text Files', '*.txt'), \
                 ('HTML Files', '*.html'), \
                 ('Python Files', '*.py'), \
                 ('All Files', '*.*')))
    
    if get_file:
        # Update Status bar
        name = get_file
        status_bar.config(text=f'{app_title}: {name}')
        # Remove the ugly file path..
        # Just show the file name in the window title
        name = name.replace('C:/Users/You/Desktop/iNotes/', '')
        app.title(f'{app_title}: {name}')

        # Save File
        with open(get_file, 'w') as f_write:
            f_write.write(textarea.get(1.0, END))


# Cut Text
def cut_text(e):
    global selected

    # Check if keyboard shortcut used
    if e:
        selected = app.clipboard_get()
    else:
        if textarea.selection_get():
            # Grab selected text from textarea
            selected = textarea.selection_get()
            # Delete selected text from textarea
            textarea.delete('sel.first', 'sel.last')
            # Clear Clipboard
            app.clipboard_clear()
            app.clipboard_append(selected)


# Copy Text
def copy_text(e):
    global selected

    # Check if keyboard shortcut used
    if e:
        selected = app.clipboard_get()

    if textarea.selection_get():
        # Grab selected text from textarea
        selected = textarea.selection_get()
        # Clear Clipboard
        app.clipboard_clear()
        app.clipboard_append(selected)


# Paste Text
def paste_text(e):
    global selected

    # Check if keyboard shortcut used
    if e:
        selected = app.clipboard_get()
    else:
        if selected:
            position = textarea.index(INSERT)
            textarea.insert(position, selected)


# Bold Button
def bold_button():

    # Create Bold Font
    bold_font = font.Font(textarea, textarea.cget('font'))
    bold_font.configure(weight='bold')

    # Configure a tag
    textarea.tag_configure('bold', font=bold_font)

    # Define Current Tags
    current_tags = textarea.tag_names('sel.first')

    # Check if tag is set
    if 'bold' in current_tags:
        textarea.tag_remove('bold', 'sel.first', 'sel.last')
    else:
        textarea.tag_add('bold', 'sel.first', 'sel.last')


# Italics Button
def italics_button():

    # Create Italic Font
    italics_font = font.Font(textarea, textarea.cget('font'))
    italics_font.configure(slant='italic')

    # Configure a tag
    textarea.tag_configure('italic', font=italics_font)

    # Define Current Tags
    current_tags = textarea.tag_names('sel.first')

    # Check if tag is set
    if 'italic' in current_tags:
        textarea.tag_remove('italic', 'sel.first', 'sel.last')
    else:
        textarea.tag_add('italic', 'sel.first', 'sel.last')


# Text Color Button
def text_color():

    # Choose New Text Color
    new_color = colorchooser.askcolor()[1]

    if new_color:
        status_bar['text'] = new_color

        # Create Colored Font
        color_font = font.Font(textarea, textarea.cget('font'))

        # Configure Tag
        textarea.tag_configure('colored', font=color_font, foreground=new_color)

        # Define Current Tags
        current_tags = textarea.tag_names('sel.first')

        # Check if tag is set
        if 'colored' in current_tags:
            textarea.tag_remove('colored', 'sel.first', 'sel.last')
        else:
            textarea.tag_add('colored', 'sel.first', 'sel.last')


# Choose Background Color
def back_color(e):

    # Choose New Background Color
    new_color = colorchooser.askcolor()[1]

    # # Check if keyboard shortcut used
    if e:
        textarea.config(bg=new_color)

    if new_color:
        textarea.config(bg=new_color)


# All Text Color
def all_text_color():

    # Choose New Background Color
    new_color = colorchooser.askcolor()[1]

    if new_color:
        textarea.config(fg=new_color)

    


# _____________________________________
# Header Frame
header_frame = Frame(app, bg=fg_color)
header_frame.pack(fill='x', ipady=20)

# _____________________________________
# Header Label (App Title)
header_label = Label(header_frame, text=app_title, \
                     bg=fg_color, fg=bg_color, font=title_font)
header_label.pack(side='left', padx=(20, 0))

# _____________________________________
# Toolbar Frame
toolbar_frame = Frame(app, bg=fg_color)
toolbar_frame.pack(fill='x')

# _____________________________________
# Text Area Frame
textarea_frame = Frame(app, bg=bg_color)
textarea_frame.pack(fill='x', ipady=20)

# _____________________________________
# Text Area Scrollbar
y_scroll = Scrollbar(textarea_frame)
y_scroll.pack(side='right', fill='y')

# _____________________________________
# Text Widget
textarea = Text(textarea_frame, bg=bg_color, fg=fg_color, font=text_font, \
                wrap=WORD, border=0, selectforeground=sel_fg_color, \
                selectbackground=sel_bg_color, undo=True, \
                yscrollcommand=y_scroll.set)
textarea.focus()
textarea.pack(fill='both', padx=20, pady=20, expand=True)

# _____________________________________
# Configure Scrollbar
y_scroll.config(command=textarea.yview)

# _____________________________________
# Toolbar Buttons

# Undo Button
undo_btn = Button(toolbar_frame, text='Undo', bg=bg_color, fg=fg_color, \
                  width=9, relief='flat', command=textarea.edit_undo)
undo_btn.pack(side='left', padx=(20, 0))

# Redo Button
redo_btn = Button(toolbar_frame, text='Redo', bg=bg_color, fg=fg_color, \
                  width=9, relief='flat', command=textarea.edit_redo)
redo_btn.pack(side='left', padx=2)

# Bold Button
bold_btn = Button(toolbar_frame, text='Bold', bg=bg_color, fg=fg_color, \
                  width=9, relief='flat', command=bold_button)
bold_btn.pack(side='left')

# Italics Button
italics_btn = Button(toolbar_frame, text='Italics', bg=bg_color, fg=fg_color, \
                  width=9, relief='flat', command=italics_button)
italics_btn.pack(side='left', padx=(2, 0))

# Text Color Button
color_btn = Button(toolbar_frame, text='Text Colour', bg=bg_color, fg=fg_color, \
                  width=9, relief='flat', command=text_color)
color_btn.pack(side='left', padx=2)

# _____________________________________
# Create Menu
app_menu = Menu(app)
app.config(menu = app_menu)

# _____________________________________
# Add File Menu
file_menu = Menu(app_menu, tearoff=False)
file_menu.configure(bg=fg_color, fg=bg_color)
# Display File Menu
app_menu.add_cascade(label='File', menu=file_menu)
# Dropdown Menu's (for: File Menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_separator()
file_menu.add_command(label='Save', command=save_file)
file_menu.add_command(label='Save As..', command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=quit)

# _____________________________________
# Add Edit Menu
edit_menu = Menu(app_menu, tearoff=False)
edit_menu.configure(bg=fg_color, fg=bg_color)
# Display Edit Menu
app_menu.add_cascade(label='Edit', menu=edit_menu)
# Dropdown Menu's (for: Edit Menu)
edit_menu.add_command(label='Undo', command=textarea.edit_undo, accelerator='Ctrl + z')
edit_menu.add_command(label='Redo', command=textarea.edit_redo, accelerator='Ctrl + y')
edit_menu.add_separator()
edit_menu.add_command(label='Cut', command=lambda: cut_text(False), accelerator='Ctrl + x')
edit_menu.add_command(label='Copy', command=lambda: copy_text(False), accelerator='Ctrl + c')
edit_menu.add_separator()
edit_menu.add_command(label='Paste', command=lambda: paste_text(False), accelerator='Ctrl + v')

# _____________________________________
# Add Color Menu
color_menu = Menu(app_menu, tearoff=False)
color_menu.configure(bg=fg_color, fg=bg_color)
# Display Color Menu
app_menu.add_cascade(label='Colours', menu=color_menu)
# Dropdown Menu's (for: Color Menu)
color_menu.add_command(label='Selected Text', command=text_color)
color_menu.add_command(label='All Text', command=all_text_color)
color_menu.add_command(label='Background', command=lambda: back_color(False), accelerator='Ctrl + b')

# _____________________________________
# Footer Frame
footer_frame = Frame(app, bg=fg_color)
footer_frame.pack(side='bottom', fill='x')

# _____________________________________
# Status Bar
status_bar = Label(footer_frame, text='Ready..', \
                   bg=fg_color, fg=bg_color, font=status_bar_font, anchor='w')
status_bar.pack(fill='x', padx=(15, 0), ipady=5)

# _____________________________________
# Edit Menu Key Bindings
app.bind('<Control-Key-x>', cut_text)
app.bind('<Control-Key-c>', copy_text)
app.bind('<Control-Key-v>', paste_text)

# _____________________________________
# Color Menu Key Bindings
app.bind('<Control-Key-b>', back_color)

# _____________________________________
# Root Defaults
if __name__ == '__main__':

    app.title(app_title)
    app.geometry(win_size)
    app.configure(bg=bg_color)
    app.mainloop()
