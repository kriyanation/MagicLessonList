import shutil
import tkinter as tk
import traceback
from threading import Thread
from tkinter import ttk, messagebox

import requests

import data_capture_lessons
import sharelesson


class MagicLessonList(tk.Toplevel):
    def __init__(self,parent,*args, **kwargs):
        super().__init__(parent,*args, **kwargs)

        s = ttk.Style(self)
        s.configure('TScrollbar', background="gray22", foreground="white")
        s.map('TScrollbar', background=[('active', '!disabled', 'gray22'), ('pressed', "white")],
              foreground=[('pressed', "white"), ('active', "gray22")])
        s.configure('Firebrick.TButton', background='steel blue', foreground='white', font=('helvetica', 12, 'bold'))

        s.map('Firebrick.TButton', background=[('active', '!disabled', 'dark turquoise'), ('pressed', 'white')],
              foreground=[('pressed', 'white'), ('active', 'white')])
        self.configure(background='gray20')
        self.l_canvas = tk.Canvas(self, background='gray20',highlightthickness=0)
        self.l_canvas.grid(row=0, column=0, columnspan=5)
        self.lesson_frame = tk.Frame(self.l_canvas, width=870,
                                    height=300,
                                    background='gray20')
        self.scrollbar = ttk.Scrollbar(self, style='TScrollbar')
        self.l_canvas.config(yscrollcommand=self.scrollbar.set)
        self.l_canvas.create_window((0, 0), window=self.lesson_frame, anchor='nw')
        self.lesson_frame.bind("<Configure>", self.l_function)
        self.scrollbar.config(command=self.l_canvas.yview)
        self.scrollbar.grid(row=0, column=5, sticky="nsew")
        self.lesson_view_label = ttk.Label(self, text="Lessons View",
                                      font=("Comic Sans", 14, 'bold'), background="gray22", foreground="white")
        self.scroll_frame = ttk.Frame(self)
        self.data_display()

    def data_display(self):
        self.headerlesson_id_label = ttk.Label(self.lesson_frame, text="ID", font=('helvetica', 16),
                                               background='gray20',
                                               foreground='aquamarine')
        self.headerlessonlabel = ttk.Label(self.lesson_frame, text="Lesson Name", font=('helvetica', 16),
                                           background='gray20',
                                           foreground='aquamarine')
        self.headerfactlabel = ttk.Label(self.lesson_frame, text="Lesson Terms", font=('helvetica', 16),
                                         background='gray20', foreground='aquamarine')
        self.headerstepslabel = ttk.Label(self.lesson_frame, text="Lesson Skills\n(first step)", font=('helvetica', 16),
                                          background='gray20', foreground='aquamarine')
        self.headersteps_numberlabel = ttk.Label(self.lesson_frame, text="Skill Steps", font=('helvetica', 16),
                                                 background='gray20', foreground='aquamarine')
        self.headersteps_sharelabel = ttk.Label(self.lesson_frame, text="Share Lesson", font=('helvetica', 16),
                                                background='gray20', foreground='aquamarine')
        self.headersteps_accesslabel = ttk.Label(self.lesson_frame, text="Share Access", font=('helvetica', 16),
                                                 background='gray20', foreground='aquamarine')
        self.headersteps_deletelabel = ttk.Label(self.lesson_frame, text="Delete Lesson", font=('helvetica', 16),
                                                 background='gray20', foreground='aquamarine')

        self.headerlesson_id_label.grid(row=0, column=0, padx=20, pady=10, sticky=tk.W)
        self.headerlessonlabel.grid(row=0, column=1, padx=20, pady=10, sticky=tk.W)
        self.headerfactlabel.grid(row=0, column=2, padx=20, pady=10, sticky=tk.W)
        self.headerstepslabel.grid(row=0, column=3, padx=20, pady=10, sticky=tk.W)
        self.headersteps_numberlabel.grid(row=0, column=4, padx=20, pady=10, sticky=tk.W)
        self.headersteps_sharelabel.grid(row=0, column=5, padx=20, pady=10, sticky=tk.W)
        self.headersteps_accesslabel.grid(row=0, column=6, padx=20, pady=10, sticky=tk.W)
        self.headersteps_deletelabel.grid(row=0, column=7, padx=20, pady=10, sticky=tk.W)

        self.import_button = ttk.Button(self, text="Import a Lesson", width=20,
                                        command=self.import_lesson,
                                        style="Firebrick.TButton")
        self.import_button.grid(row=1, column=0, columnspan=8, pady=20)

        row_index = 1
        self.share_image = tk.PhotoImage(file="../images/share.png")
        self.delete_image = tk.PhotoImage(file="../images/trash.png")
        self.lesson_list = data_capture_lessons.get_Lessons()
        for element in self.lesson_list:
            bgcolor = "gray20"
            self.dataidlabel = ttk.Label(self.lesson_frame, text=element[0], font=('helvetica', 12),
                                         foreground='white', wraplength=200, background=bgcolor)
            self.datanamelabel = ttk.Label(self.lesson_frame, text=element[1], font=('helvetica', 12),
                                           foreground='white', wraplength=200, background=bgcolor)
            self.datafactlabel = ttk.Label(self.lesson_frame, text=element[2] + '\n' + element[3] + '\n' + element[4],
                                           font=('helvetica', 12),
                                           foreground='white', wraplength=300, background=bgcolor)
            self.datasteplabel = ttk.Label(self.lesson_frame,
                                           text=element[5],
                                           font=('helvetica', 12),
                                           foreground='white', wraplength=200, background=bgcolor)
            self.datastepnumbers = ttk.Label(self.lesson_frame,
                                             text=str(element[6]),
                                             font=('helvetica', 12),
                                             foreground='white', wraplength=200, background=bgcolor)
            lesson_id = element[0]
            self.share_button = ttk.Button(self.lesson_frame, text="", image=self.share_image,
                                           style="dash.TButton", width=5,
                                           command=lambda c=lesson_id: self.launch_share(c))
            self.delete_button = ttk.Button(self.lesson_frame, text="", image=self.delete_image,
                                           style="dash.TButton", width=5,
                                           command=lambda c=lesson_id: self.delete_lesson(c))
            text_access = self.get_access_text(lesson_id)
            self.access_label = ttk.Label(self.lesson_frame,
                                          text=text_access,
                                          font=('helvetica', 12),
                                          foreground='white', wraplength=200, background=bgcolor)

            self.dataidlabel.grid(row=row_index, pady=20, column=0, padx=20, sticky=tk.W)
            self.datanamelabel.grid(row=row_index, pady=20, column=1, padx=20, sticky=tk.W)
            self.datafactlabel.grid(row=row_index, pady=20, column=2, padx=20, sticky=tk.W)
            self.datasteplabel.grid(row=row_index, pady=20, column=3, padx=20, sticky=tk.W)
            self.datastepnumbers.grid(row=row_index, pady=20, column=4, padx=20, sticky=tk.W)
            self.share_button.grid(row=row_index, pady=20, column=5, padx=20, sticky=tk.W)
            self.access_label.grid(row=row_index, pady=20, column=6, padx=20, sticky=tk.W)
            self.delete_button.grid(row=row_index, pady=20, column=7, padx=20, sticky=tk.W)
            row_index += 1

    def get_access_text(self,lesson_id):
        if data_capture_lessons.is_shared(lesson_id) == 1:
            class_id, User = data_capture_lessons.get_user_classid()
            return ("Shared Access:\nLesson ID = "+str(lesson_id)+"\nClass ID = "+str(class_id)+"\nUser = "+str(User))
        else:
            return ""

    def import_lesson(self):
        self.import_screen = tk.Toplevel(self)
        self.import_screen.title("Import Lesson")
        self.import_screen.geometry("350x250")
        self.import_screen.configure(background="grey20")
        user = tk.StringVar()
        classid = tk.StringVar()
        lessonid = tk.StringVar()

        user_label = tk.Label(self.import_screen, text="Teacher ID", font=("Comic Sans", 12, 'bold'),
                                  background="gray22", foreground="white")
        user_label.pack()
        # Set username entry
        # The Entry widget is a standard Tkinter widget used to enter or display a single line of text.
        user_entry = tk.Entry(self.import_screen, textvariable=user)
        user_entry.pack()

        # Set password label
        class_label = tk.Label(self.import_screen, text="Class ID", font=("Comic Sans", 12, 'bold'),
                                  background="gray22", foreground="white")
        class_label.pack()

        # Set password entry
        class_entry = tk.Entry(self.import_screen, textvariable=classid)
        class_entry.pack()
        lesson_label = tk.Label(self.import_screen, text="Lesson ID", font=("Comic Sans", 12, 'bold'),
                               background="gray22", foreground="white")
        lesson_label.pack()

        # Set password entry
        lesson_entry = tk.Entry(self.import_screen, textvariable=lessonid)
        lesson_entry.pack()

        self.importstatusvar = tk.StringVar()
        status_lbl = tk.Label(self.import_screen, textvariable=self.importstatusvar, font=("Comic Sans", 8, 'bold'),
                              background="gray20", foreground="aquamarine")
        status_lbl.pack()
        # Set register button
        ttk.Button(self.import_screen, text="Start Import", width=10,
                   command=lambda: self.get_lesson(user.get(), classid.get(), lessonid.get()),
                   style="Firebrick.TButton").pack()
    def get_lesson(self,user,classid,lessonid):

        status = sharelesson.import_new_lesson(user,classid,lessonid,self)
        if status == 'error':
            self.importstatusvar.set("Access information could be wrong, please try again")
        else:
            self.import_screen.destroy()
            for widget in self.lesson_frame.winfo_children():
                widget.destroy()
            self.data_display()
    def l_function(self,event):
       self.l_canvas.configure(scrollregion=self.l_canvas.bbox("all"),width=1450,height=750)

    def delete_lesson(self,lesson_id):
        try:
            delete_data = data_capture_lessons.delete_lesson(lesson_id)
            if delete_data == 0:
                shutil.rmtree("../Lessons/Lesson" + str(lesson_id), True)

        except:
            traceback.print_exc()
            print(" Error Deleting Lessons")
            return 1
        for widget in self.lesson_frame.winfo_children():
            widget.destroy()
        self.data_display()

    def launch_share(self,lesson_id):

        self.login_screen = tk.Toplevel(self)
        self.login_screen.title("Login")
        self.login_screen.geometry("350x250")
        self.login_screen.configure(background="grey20")
        username = tk.StringVar()
        password = tk.StringVar()
       # Set username label
        username_lable = tk.Label(self.login_screen, text="Username * ",font=("Comic Sans", 12, 'bold'), background="gray22", foreground="white")
        username_lable.pack()
       # Set username entry
        # The Entry widget is a standard Tkinter widget used to enter or display a single line of text.
        username_entry = tk.Entry(self.login_screen, textvariable=username)
        username_entry.pack()

        # Set password label
        password_lable = tk.Label(self.login_screen, text="Password * ",font=("Comic Sans", 12, 'bold'), background="gray22", foreground="white")
        password_lable.pack()

        # Set password entry
        password_entry = tk.Entry(self.login_screen, textvariable=password, show='*')
        password_entry.pack()
        self.statusvar = tk.StringVar()
        status_lbl = tk.Label(self.login_screen, textvariable=self.statusvar,font=("Comic Sans", 8, 'bold'), background="gray20", foreground="aquamarine")
        status_lbl.pack()
        # Set register button
        ttk.Button(self.login_screen, text="Login", width=10, command = lambda: self.get_token(username.get(),password.get(),lesson_id) ,style="Firebrick.TButton").pack()


    def get_token(self,user,pwd,lesson_id):
        self.logintoken = sharelesson.get_token(user, pwd)
        if self.logintoken=="error":
            self.statusvar.set("Login Failed. Please try again or contact support")
        else:
            messagebox.showinfo("Lesson Share","Sharing Triggered.\n The lesson list will refresh once sharing is complete \nwith the updated access details.")
            self.login_screen.destroy()
            self.post_lesson(self.logintoken,lesson_id)
            for widget in self.lesson_frame.winfo_children():
                widget.destroy()
            self.data_display()


    def post_lesson(self,token,lesson_id):
        data = sharelesson.prepare_lesson_share(lesson_id)
        sharelesson.post_lesson(data,token,lesson_id)






# if __name__== "__main__":
#     dashboard_app = tk.Tk()
#     dashboard_app.configure(background="gray20")
#     dashboard_app.title("Learning Room Lesson List")
#     dashboard_app.geometry("1200x800")
#     frame = MagicLessonList(dashboard_app)
#     dashboard_app.rowconfigure(0,weight=1)
#     dashboard_app.columnconfigure(0, weight=1)
#     frame.grid(row=0,column=0)
#     dashboard_app.mainloop()