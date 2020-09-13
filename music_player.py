# Importing Required Modules & libraries
from tkinter import *
import pygame
import os
from os import path
from pydub import AudioSegment
import numpy as np
import simpleaudio as sa
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from IPython.display import Audio
from numpy.fft import fft, ifft
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog
import webbrowser
from tkinter import messagebox
from tkinter import simpledialog

# Defining MusicPlayer Class


class MusicPlayer:

    # Defining Constructor

    def __init__(self, root):
        self.root = root
        # Title of the window
        self.root.title("Music Player")
        # Window Geometry
        self.root.geometry("1200x200+200+200")
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()

        # adding the menu bar
        menubar = Menu(self.root)
        files = Menu(menubar, tearoff=0)
        files.add_command(label="Conversion", command=self.conversion)
        files.add_command(label="Open", command=self.open)
        files.add_command(label="SaveAs", command=self.save)
        files.add_command(label="Visualisation", command=self.visuals)
        files.add_separator()
        files.add_command(label="Exit", command=root.destroy)
        menubar.add_cascade(label="Collection", menu=files)

        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Set Volume", command=self.volume)
        editmenu.add_separator()
        editmenu.add_command(label="Exit", command=root.destroy)
        menubar.add_cascade(label="Edit", menu=editmenu)

        contactmenu = Menu(menubar, tearoff=0)
        contactmenu.add_command(label="Contact Me", command=self.contact)
        contactmenu.add_command(label="Contributions", command=self.contribute)
        menubar.add_cascade(label="Contact", menu=contactmenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help", command=self.help)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.root.config(menu=menubar)
        # Creating Track Frame for Song label & status label
        trackframe = LabelFrame(self.root, text="Song Track", font=(
            "times new roman", 15, "bold"), bg="grey", fg="gold", bd=5, relief=GROOVE)
        trackframe.place(x=0, y=0, width=800, height=100)
        # Inserting Song Track Label
        songtrack = Label(trackframe, textvariable=self.track, width=20, font=(
            "times new roman", 24, "bold"), bg="grey", fg="gold").grid(row=0, column=0, padx=10, pady=5)
        # Inserting Status Label
        trackstatus = Label(trackframe, textvariable=self.status, font=(
            "times new roman", 24, "bold"), bg="grey", fg="gold").grid(row=0, column=1, padx=10, pady=5)

        # Creating Button Frame
        buttonframe = LabelFrame(self.root, text="Control Panel", font=(
            "times new roman", 15, "bold"), bg="grey", fg="gold", bd=5, relief=GROOVE)
        buttonframe.place(x=0, y=100, width=1000, height=100)
        # Inserting Play Button
        playbtn = Button(buttonframe, text="PLAY", command=self.playsong, width=4, height=2, font=(
            "times new roman", 16, "bold"), fg="navyblue", bg="gold").grid(row=0, column=0, padx=10, pady=5)
        # Inserting Pause Button
        playbtn = Button(buttonframe, text="PAUSE", command=self.pausesong, width=5, height=2, font=(
            "times new roman", 16, "bold"), fg="navyblue", bg="gold").grid(row=0, column=1, padx=10, pady=5)
        # Inserting Unpause Button
        playbtn = Button(buttonframe, text="UNPAUSE", command=self.unpausesong, width=7, height=2, font=(
            "times new roman", 16, "bold"), fg="navyblue", bg="gold").grid(row=0, column=2, padx=10, pady=5)
        # Inserting Stop Button
        playbtn = Button(buttonframe, text="STOP", command=self.stopsong, width=4, height=2, font=(
            "times new roman", 16, "bold"), fg="navyblue", bg="gold").grid(row=0, column=3, padx=10, pady=5)
        # Inserting the exit button
        exitbtn = Button(buttonframe, text="EXIT", command=root.destroy, width=3, height=2, font=(
            'times new roman', 16, 'bold'), fg='navyblue', bg='gold').grid(row=0, column=4, padx=10, pady=5)
        # Audio Testing
        audiotest = Button(buttonframe, text="TEST\n AUDIO", command=self.test, width=5, height=2, font=(
            'times new roman', 16, 'bold'), fg='navyblue', bg='gold').grid(row=0, column=5, padx=10, pady=5)
        # Recording
        record = Button(buttonframe, text="RECORD", width=8, height=2, font=('times new roman', 16, 'bold'),
                        fg='navyblue', bg='gold', command=self.record).grid(row=0, column=6, padx=10, pady=5)
        # Rewind
        #rewind = Button(buttonframe,text=">>",width=3,height=2,font=('times new roman',16,'bold'),fg='navyblue',bg='gold',command=self.forward).grid(row=0,column=7,padx=10,pady=5)

        # Creating Playlist Frame
        songsframe = LabelFrame(self.root, text="Song Playlist", font=(
            "times new roman", 15, "bold"), bg="grey", fg="white", bd=5, relief=GROOVE)
        songsframe.place(x=800, y=0, width=600, height=200)
        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        # Inserting Playlist listbox
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectbackground="gold", selectmode=SINGLE, font=(
            "times new roman", 12, "bold"), bg="silver", fg="navyblue", bd=5, relief=GROOVE)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        # Changing Directory for fetching Songs
        os.chdir("/home/kali/Desktop/music_player/music_files")
        # Fetching Songs
        songtracks = os.listdir()
        # Inserting Songs into Playlist
        for track in songtracks:
            self.playlist.insert(END, track)

    def conversion(self):
        try:
            files = simpledialog.askstring(
                "File", "Enter the name of the file")
            save = simpledialog.askstring(
                "File", "Enter the name by which you want to save the File")
            sound = AudioSegment.from_mp3(files)
            sound.export(save, format='wav')
            messagebox.showinfo("Converted", str(sound)+".wav")
            os.chdir('/home/kali/Desktop/music_player/music_files')
            songstracks = os.listdir()
            for track in songstracks:
                self.playlist.insert(END, track)
        except:
            messagebox.showerror("Error", "Cannot Convert the file")

    def help(self):
        messagebox.showinfo(
            "Help", "For more information please refer to my github page in contributions")

    def volume(self):
        a = pygame.mixer.music.get_volume()
        messagebox.showinfo("Volume", "Your current Volume is" +
                            str(int(pygame.mixer.music.get_volume()*100)))
        pygame.mixer.music.set_volume(a)

    def visuals(self):
        os.chdir("/home/kali/Desktop/music_player/music_files")
        songs = os.listdir()
        prompt = simpledialog.askinteger(
            "input", "Enter the index of the song(First song starts from 0)")
        try:
            if len(songs) >= prompt:
                fs, data = read(songs[prompt])
                data = data[:, 0]
                plt.figure()
                plt.plot(data)
                plt.show()
        except:
            messagebox.showerror("Error", "Please enter a valid number")

    def open(self):
        try:
            root.filename = filedialog.askopenfilename(
                initialdir="/home/kali", title="Selct your track/album in .wav EXTENSION", filetypes=(("Mp 3 Music Files", "*.mp3"), ("wav Music Files", "*.wav")))
            print("Added"+" " + root.filename)
            messagebox.showinfo("Added", "Ahoy! Press the Play Button")
            os.chdir('/home/kali/Desktop/music_playeri/music_files')
            tracks = os.listdir()
            for track in tracks:
                self.playlist.insert(END, track)
        except:
            messagebox.showerror("Error", "Cannot Open the File")

    def save(self):
        try:
            files = filedialog.asksaveasfilename(title="Enter the name of your file", filetypes=(("python files", ".py"), ("Text files", ".txt"), (
                "mp3 Music Files", "*.mp3"), ("wav Music Files", "*.wav"), ("mp4 Music Files", "*.mp4")), initialdir="/home/kali")
        except:
            print("Cannot save the file")
            messagebox.showerror("Error", "Cannot Save the File")

    def contribute(self):
        webbrowser.open("https://github.com/avishmehta68710")

    def contact(self):
        messagebox.showinfo(
            "Contact", "For any queries or ideas\n Please contact me at avishmehta6870@gmail.com")

    def rewind(self):
        self.status.set('-Rewind')
        pygame.mixer.music.rewind()

    def record(self):
        fs = 44100  # Sample rate
        seconds = simpledialog.askinteger(
            "Input", "Enter the duration of recording(in seconds)")  # Duration of recording
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        write('recordings.wav', fs, myrecording)  # Save as WAV file

    def test(self):
        frequency = 440
        fs = 44100
        seconds = 2
        t = np.linspace(0, seconds, seconds*fs, False)
        note = np.sin(frequency*t*2*np.pi)
        audio = note*(2**15-1)/np.max(np.abs(note))
        audio = audio.astype(np.int16)
        play = sa.play_buffer(audio, 1, 2, fs)
        play.wait_done()

    # Defining Play Song Function
    def playsong(self):
        # Displaying Selected Song title
        self.track.set(self.playlist.get(ACTIVE))
        # Displaying Status
        self.status.set("-Playing")
        # Loading Selected Song
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        # Playing Selected Song
        pygame.mixer.music.play()

    def stopsong(self):
        # Displaying Status
        self.status.set("-Stopped")
        # Stopped Song
        pygame.mixer.music.stop()

    def pausesong(self):
        # Displaying Status
        self.status.set("-Paused")
        # Paused Song
        pygame.mixer.music.pause()

    def unpausesong(self):
        # Displaying Status
        self.status.set("-Playing")
        # Playing back Song
        pygame.mixer.music.unpause()

    def exitsong(self):
        # Display Status
        self.statu.set("-Exit")
        # Exit the song
        pygame.mixer.music.exit()


# Creating TK Container
root = Tk()

# Passing Root to MusicPlayer Class
MusicPlayer(root)
# Root Window Looping
root.mainloop()
