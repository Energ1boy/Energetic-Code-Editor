from tkinter import ttk,filedialog,font
from io import StringIO
import tkinter as tk
import sys
import re

#window
window = tk.Tk()
window.title("Energetic-Code")
window.geometry("800x600")

#variables
file_path = None
console_position = tk.IntVar()
console_position.set(4)
console_output = StringIO()



theme = tk.IntVar()
theme.set(1)
light_theme = {"editor_bg": "#f6f6f6","editor_fg": "#000000","console_bg": "#d0d0d0","console_fg": "#000000","mark": "#000000"}
dark_theme = {"editor_bg": "#393e46","editor_fg": "#f7f7f7","console_bg": "#393e46","console_fg": "#f7f7f7", "mark": "#f7f7f7"}
police_default = ("Segoe", 12)

# keywords =  re.compile(r'\b(?:and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b'),
keywords = ["and","as","async","assert","break","class","continue","def","del","elif","else","except","False","finally","for","from","global","if","import","in","is","lambda","None","nonlocal","not","or","pass","raise","return","True","try","while","with","yield"]

highlight_color = {
    "keywords" : "",
    "comment" : "",
    "variable" : "",
    "string" : ""
}

#functions

#file functions
def run(event=None):
    terminal_text.config(state="normal")
    terminal_text.delete(1.0,tk.END)
    code_data = editor_text.get(1.0, tk.END)
    try:
        sys.stdout = console_output
        exec(code_data)
        console_text = console_output.getvalue()
        terminal_text.insert("end", str(console_text))
        terminal_text.config(state="disable")
    except Exception as e:
        terminal_text.insert("end", f"Error: {str(e)}\n")
        terminal_text.config(state="disable")

def new_file(event=None):
    global file_path
    editor_text.delete(1.0, tk.END)
    editor_text.insert(1.0, "#write your code here")
    file_path = None
    print("new file :" +str(file_path))

def save_file(event=None):
    if file_path != None or "":
        with open(str(file_path), "w") as f:
            f.write(editor_text.get(1.0, tk.END))
    else :
        save_as()
    print("save :" +str(file_path))

def save_as(event=None):
    global file_path
    file_path = tk.filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
    print("save as :" + file_path)
    with open(str(file_path), "w") as f:
        f.write(editor_text.get(1.0, tk.END))

def open_file(event=None):
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    with open(file_path, "r") as f:
        content = f.read()
        editor_text.delete(1.0, tk.END)
        editor_text.insert(tk.END, content)
    print("save as :" +str(file_path))

#editor functions
def select_all(event=None):
    editor_text.tag_add("sel", "1.0", "end")

def add_indetations():

    print("hey")

def add_numbers_line(event=None):
    # Effacer les anciens numéros de ligne
    lines_number_canva.delete("numero_ligne")
    
    # Obtenir les coordonnées y de la première ligne affichée dans le widget de texte
    y0 = editor_text.yview()[0] * line_height
    # Obtenir les coordonnées y dtext dernière ligne affichée dans le widget de texte
    y1 = editor_text.yview()[1] * line_height
    # Nombre de lignes visibles dans le widget de texte
    first_visible_line = int(y0 // line_height) + 1
    last_visible_line = int(y1 // line_height) + 1
    
    for i in range(first_visible_line, last_visible_line + 1):  # Afficher les numéros de ligne
        print(i)
        # Calculer les coordonnées y pour chaque numéro de ligne
        y = (i - first_visible_line) * line_height
        # Afficher le numéro de ligne dans le lines_number_canva à la position (5, y)
        lines_number_canva.create_text(5, y, anchor="nw", text=str(i), tags="numero_ligne")
        
#theme
def themes_function():
    if theme.get() == 1:
        editor_text.config(bg=light_theme["editor_bg"], fg=light_theme["editor_fg"],insertbackground=light_theme["mark"])
        terminal_text.config(bg=light_theme["console_bg"], fg=light_theme["console_fg"])
    elif theme.get() ==2:
        editor_text.config(bg=dark_theme["editor_bg"], fg=dark_theme["editor_fg"],insertbackground=dark_theme["mark"])
        terminal_text.config(bg=dark_theme["console_bg"], fg=dark_theme["console_fg"])

def highlight_function(event=None):
    #suprime les tags existants
    editor_text.tag_remove("keyword", 1.0, tk.END)
    editor_text.tag_remove("string", 1.0, tk.END)
    editor_text.tag_remove("comment", 1.0, tk.END)

    code_data = editor_text.get(1.0, tk.END)

    #divides the code in lines
    lines = code_data.split("\n")

    for i, line in enumerate(lines, 1):
        for keyword in keywords:
        # searches word in the text belonging to keywords list
            for match in re.finditer(r'\b{}\b'.format(keyword), line):
               
               start_index = "{}.{}".format(i, match.start())
               end_index = "{}.{}".format(i, match.end())
               editor_text.tag_add("keyword", start_index, end_index)
    


        for string in re.finditer(r'(\'[^\']*\'|\"[^\"]*\")', line):
            first_str = f"{i}.{string.start()}" 
            last_str = f"{i}.{string.end()}"
            editor_text.tag_add("string", first_str, last_str)
        for comment in re.finditer(r'(#.*)', line):
            begin_comment = f"{i}.{comment.start()}"
            end_comment = f"{i}.end"
            editor_text.tag_add("comment", begin_comment, end_comment)
    #apply the color
    editor_text.tag_configure("keyword", foreground="orange")
    editor_text.tag_configure("string", foreground="green")
    editor_text.tag_configure("comment", foreground="gray")

#Create the top bar
menu_bar = tk.Menu()
#file
file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="New",accelerator="Ctrl+N",command=new_file)
file_menu.add_command(label="Save",accelerator="Ctrl+S",command=save_file)
file_menu.add_command(label="Save_as",accelerator="Shift+Ctrl+A",command=save_as)
file_menu.add_command(label="open",accelerator="Ctrl+O",command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Exit",accelerator=None, command=exit)
menu_bar.add_cascade(menu=file_menu, label="File")
#run
run_menu = tk.Menu(menu_bar, tearoff=False)
run_menu.add_command(label="Run",accelerator="F5",command=run)
menu_bar.add_cascade(menu=run_menu, label="Run")
#preferences
preferences_menu = tk.Menu(menu_bar, tearoff=False)
theme_menu = tk.Menu(menu_bar,tearoff=False)
console_position_menu = tk.Menu(menu_bar,tearoff=False)
theme_menu.add_radiobutton(label="Light",value=1,variable=theme,command=themes_function)
theme_menu.add_radiobutton(label="Dark",value=2,variable=theme,command=themes_function)
console_position_menu.add_radiobutton(label="Right",value=1,variable=console_position)
console_position_menu.add_radiobutton(label="Left",value=2,variable=console_position)
console_position_menu.add_radiobutton(label="Top",value=3,variable=console_position)
console_position_menu.add_radiobutton(label="Bottom",value=4,variable=console_position)
menu_bar.add_cascade(menu=preferences_menu, label="Preferences")
preferences_menu.add_cascade(menu=theme_menu,label="Themes")
preferences_menu.add_cascade(menu=console_position_menu,label="Console position")

#block text
editor_Frame = tk.Frame(window)
editor_Frame.pack(fill="both")

lines_number_canva = tk.Canvas(editor_Frame,width=30)
lines_number_canva.pack(side="left",pady=10,fill="y")

editor_text = tk.Text(editor_Frame, font=police_default)
editor_text.pack(side="left",pady=10,fill="both")


lines_number_canva.config(bg="Blue")

text_high = editor_text.winfo_height()
amount_of_lines = int(editor_text.index('end-1c').split('.')[0])
police = editor_text.cget("font")
if police:
    # Extraire la hauteur de ligne de la police
    line_height = tk.font.Font(font=police).metrics("linespace")
else:
    # Utiliser une hauteur de ligne par défaut si la police n'est pas définie
    line_height = 20  # Vous pouvez ajuster cette valeur selon votre besoin

# #terminal block
terminal_frame = tk.Frame(window)
terminal_frame.pack(expand=True,fill="both",padx=(5, 0),pady=(0,5))
terminal_label = tk.Label(terminal_frame, text="console output:")
terminal_label.pack(anchor="w")
terminal_text = tk.Text(terminal_frame,wrap="word",bg="gainsboro",state="disabled")
terminal_text.pack(fill="both")


#shortcuts
window.bind_all("<F5>", run)
window.bind_all("<Control-Key-5>", run)
window.bind_all("<Control-n>", new_file)
window.bind_all("<Control-N>", new_file)
window.bind_all("<Control-s>", save_file)
window.bind_all("<Control-S>", save_file)
window.bind_all("<Shift-Control-s>", save_as)
window.bind_all("<Shift-Control-S>", save_as)
window.bind_all("<Control-o>", open_file)
window.bind_all("<Control-O>", open_file)
window.bind_all("<Control-a>", select_all)
window.bind_all("<Control-A>", select_all)
editor_text.bind("<KeyRelease>", highlight_function)
# editor_text.bind("<<Modified>>", add_numbers_line)

# window.bind_all("<Control-slash>", comment_line)
# window.bind_all("<Control-slash>", comment_line)



#run the program
# editor_text.config(bg=light_theme["editor_bg"], fg=light_theme["editor_fg"],insertbackground=light_theme["mark"])
# terminal_text.config(bg=light_theme["console_bg"])
window.config(menu=menu_bar)
themes_function()
new_file()
window.mainloop()