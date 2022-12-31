import tkinter as tk
from pygame import mixer
from math import sin, cos, radians

# Global variables.
project_font = 'Calculator'
font_color = '#12FF15'
background_color = 'black'
counter_seconds = 1500  # Starting time setting of timer().
work_passed = 0  # Counts seconds of work time passed.
break_passed = 0  # Counts seconds of breaks passed.
flow = 0  # 0 means no timer function instance is running.
work_check = True  # Checks if timer runs with work or break time.
radius = 68  # Length of Progress Gauge pointer.
# Variables needed to access them from main() outer level and pointer_update() inner level.
circle = None
pointer = None
# List of sound names.
alarm_sounds = ['Breaking Glass',
                'Calm String',
                'Dramatic Riser',
                'Epic Intro',
                'Flute',
                'Game Alarm',
                'Reggae Loop',
                'Sfx Glitch',
                'Shotgun',
                'Wtf Alert', ]
# Text for About frame.
about = '''This app facilitates the use of Pomodoro time management technique. It helps keep focus and balance between work and \
rest. Setting and achieving a daily time goals is much easier now. Work and Break buttons reset timer with adjusted time \
settings. Also they stop sound playback while it is running. Progress Gauge and Goal Completion updates every minute. \
Sound test is possible only when Timer is not running.'''


def main():
    # Starting tkinter, settings for main window.
    root = tk.Tk()
    root.resizable(False, False)
    root.title('Pomodoro Timer')
    root.iconbitmap('icon1.ico')
    root.geometry('600x600+300+300')

    # Setting main window background.
    bg = tk.PhotoImage(file='bkground.png')  # image size 600x600
    canvas = tk.Canvas(root, borderwidth=0)
    canvas.pack(fill='both', expand=True)
    canvas.create_image(0, 0, image=bg, anchor='nw')
    canvas.create_text(300, 43, text='POMODORO TIMER', font=(project_font, 45, 'bold'), fill=background_color)

    # Creating Session Work Time frame with two spinboxes for user input.
    # Hours spinbox
    hours_input = tk. IntVar()
    hours_input.set(0)
    goal_frame = tk.LabelFrame(root, fg=font_color, bg=background_color)
    canvas.create_window(300, 440, height=40, width=240, anchor='n', window=goal_frame)
    canvas.create_text(300, 420, text='Session work time goal', font=(project_font, 20, 'bold'), fill=font_color)
    hours_spin = tk.Spinbox(goal_frame, textvariable=hours_input, font=(project_font, 16, 'bold'), width=2, from_=0, to=12,
                            bg=background_color, fg=font_color, validate='all', wrap=True)
    hours_spin.grid(column=1, row=1, padx=7, pady=4)
    hours_label = tk.Label(goal_frame, fg=font_color, bg=background_color, font=(project_font, 16, 'bold'), text='hours ')
    hours_label.grid(column=2, row=1, padx=0, pady=4)

    # Minutes spinbox
    minutes_input = tk.IntVar()
    minutes_input.set(25)
    minutes_spin = tk.Spinbox(goal_frame, textvariable=minutes_input, font=(project_font, 16, 'bold'), width=2, from_=0, to=60,
                              bg=background_color, fg=font_color, validate='all', wrap=True)
    minutes_spin.grid(column=3, row=1, padx=0, pady=4)
    minutes_label = tk.Label(goal_frame, fg=font_color, bg=background_color, font=(project_font, 16, 'bold'), text=' minutes')
    minutes_label.grid(column=4, row=1, padx=0, pady=4)

    # Drawing colourful arc for Progress Gauge.
    for arc_degree in range(0, 181):
        canvas.create_arc(425, 160, 565, 300, start=arc_degree, extent=2, outline=arc_color_update(arc_degree), width=15,
                          style=tk.ARC)

    # Creating Progress Gauge text and pointer.
    canvas.create_text(500, 130, text='Progress Gauge', font=(project_font, 20, 'bold'), fill=font_color)
    global circle
    circle = canvas.create_oval(488, 223, 502, 237, fill='red')
    global pointer
    pointer = canvas.create_line(495, 230, (495 - radius * cos(0)), (230 - radius * sin(0)), width=3, arrow='last',
                                 arrowshape=(radius, radius, 4), fill='red')

    # Creating Goal Completion Frame.
    progress_frame = tk.LabelFrame(root, fg=font_color, bg=background_color)
    canvas.create_window(495, 250, height=55, width=150, anchor='n', window=progress_frame)
    progress_label = tk.Label(progress_frame, fg=font_color, bg=background_color, font=(project_font, 14, 'bold'),
                              text='Goal Completion 0.0%', wraplength=160)
    progress_label.pack(padx=3, pady=3)


    # Updates pointer of Progress Gauge. Called from timer().
    def pointer_update():
        global pointer
        global circle
        canvas.delete(pointer, circle)
        goal_minutes = hours_input.get() * 60 + minutes_input.get()
        in_radian = 1.8 * radians(completion(work_passed, goal_minutes))  # scale value in radian
        circle = canvas.create_oval(488, 223, 502, 237, fill=arc_color_update(
                180-round(completion(work_passed, goal_minutes)*1.8)))
        pointer = canvas.create_line(495, 230, (495 - radius * cos(in_radian)), (230 - radius * sin(in_radian)), width=6,
                                     arrow='last', arrowshape=(radius, radius, 3),
                                     fill=arc_color_update(180-round(completion(work_passed, goal_minutes)*1.8)))


    # Updates Goal Completion frame. It's called from timer().
    def goal_update():
        goal_minutes = hours_input.get() * 60 + minutes_input.get()
        progress_label.config(text=f'Goal completion\n {((work_passed/60)/goal_minutes)*100:.1f}%')


    #  Menu for choosing sound.
    sound_click = tk.StringVar()
    sound_click.set('Calm String')
    sound_menu = tk.OptionMenu(root, sound_click, *alarm_sounds)
    canvas.create_window(30, 150, height=40, width=150, anchor='nw', window=sound_menu)
    sound_menu.config(width=12, font=(project_font, 14, 'bold'), bg=background_color, fg=font_color, borderwidth=5,
                      activebackground=background_color, activeforeground=font_color, highlightthickness=0)
    sound_menu['menu'].config(borderwidth=0, font=(project_font, 14, 'bold'), bg=background_color, fg=font_color,
                              activebackground='black', activeforeground=font_color, bd=5, relief='raised')
    sound_menu['borderwidth'] = 3
    canvas.create_text(100, 130, text='Sound Menu', font=(project_font, 20, 'bold'), fill=font_color)

    #  Slider for setting volume.
    volume_value = tk.IntVar()
    volume_value.set(100)
    volume_slider = tk.Scale(root, activebackground=background_color, troughcolor=background_color, bg=background_color,
                             fg=font_color,  border=1, highlightthickness=0, highlightbackground=background_color,
                             font=(project_font, 14, 'bold'), from_=0, to=100, orient='horizontal', variable=volume_value)
    canvas.create_window(50, 350, width=140, height=44, anchor='nw', window=volume_slider)
    canvas.create_text(120, 330, text='Volume', font=(project_font, 20, 'bold'), fill=font_color)


    # Reads chosen sound file, sets volume, plays sound.
    def play_music():
        mixer.init()
        if mixer.music.get_busy():
            mixer.quit()
        else:
            mixer.music.load(sound_click.get() + '.mp3')
            mixer.music.set_volume(volume_value.get() / 100)
            mixer.music.play()


    # Starts and stops Sound Test if timer() is not busy.
    def sound_test():
        if flow == 0:
            mixer.init()
            if mixer.music.get_busy():
                mixer.quit()
            else:
                mixer.init()
                mixer.music.load(sound_click.get() + '.mp3')
                mixer.music.set_volume(volume_value.get() / 100)
                mixer.music.play()


    # Sound test button
    test_button = tk.Button(root, activebackground=background_color, activeforeground=font_color, height=1, text='Start / Stop',
                            borderwidth=5, font=(project_font, 14, 'bold'), bg=background_color, fg=font_color, command=sound_test)
    canvas.create_window(34, 250, height=47, width=140, anchor='nw', window=test_button)
    canvas.create_text(100, 230, text='Sound Test', font=(project_font, 20, 'bold'), fill=font_color)


    # Pauses timer().
    def pause_function():
        global flow
        flow = 0


    # Pause button
    pause_button = tk.Button(root,  activebackground=background_color, activeforeground=font_color, text='Pause', borderwidth=5,
                             height=1, font=(project_font, 20, 'bold'), bg=background_color, fg=font_color, command=pause_function)
    canvas.create_window(310, 250, height=57, width=90, anchor='nw', window=pause_button)


    # Stops timer(), reads worktime as counter_seconds, sets timer() to count time as a work time.
    def work_function():
        mixer.quit()
        global flow
        global work_check
        global counter_seconds
        flow = 0
        counter_seconds = work_minutes.get() * 60
        if counter_seconds == 3600:  # There are only fields for minutes and seconds so one hour is 59m:59secs in this app.
            counter_seconds = 3599
        timer_label['text'] = timer_update(counter_seconds)
        work_check = True


    # Work button
    work_button = tk.Button(root, activebackground=background_color, activeforeground=font_color, text='Work', borderwidth=5,
                            font=(project_font, 20, 'bold'), bg=background_color, fg=font_color, command=work_function)
    canvas.create_window(200, 80, height=57, width=90, anchor='nw', window=work_button)

    # Slider for setting duration (in minutes) of a worktime.
    work_minutes = tk.IntVar()
    work_minutes.set(25)
    work_slider = tk.Scale(root, activebackground=background_color, troughcolor=background_color,  bg=background_color,
                           fg=font_color, border=1, highlightthickness=0, highlightbackground=background_color,
                           font=(project_font, 14, 'bold'), from_=15, to=60, orient='horizontal', variable=work_minutes)
    canvas.create_window(230, 350, width=140, height=44, anchor='nw', window=work_slider)
    canvas.create_text(300, 330, text='Work time', font=(project_font, 20, 'bold'), fill=font_color)

    # Slider for setting duration (in minutes) of a break.
    break_minutes = tk.IntVar()
    break_minutes.set(5)
    break_slider = tk.Scale(root, activebackground=background_color, troughcolor=background_color, bg=background_color,
                            fg=font_color, border=1, highlightthickness=0, highlightbackground=background_color,
                            font=(project_font, 14, 'bold'), from_=5, to=30, orient='horizontal', variable=break_minutes)
    canvas.create_window(410, 350, width=140, height=44, anchor='nw', window=break_slider)
    canvas.create_text(480, 330, text='Break time', font=(project_font, 20, 'bold'), fill=font_color)

    # Creating Timer label.
    timer_label = tk.Label(root, width=6, height=1, text=str(work_minutes.get()) + ':00', relief='raised', borderwidth=5,
                           font=(project_font, 50, 'bold'), bg=background_color, fg=font_color)
    canvas.create_window(200, 150, width=200, anchor='nw', window=timer_label)

    # About frame
    about_frame = tk.LabelFrame(root, labelanchor='n', font=('Calibri', 10, 'bold'), foreground=font_color, text='About',
                                bg=background_color)
    canvas.create_window(300, 485, height=110, width=580, anchor='n', window=about_frame)
    about_label = tk.Label(about_frame, text=about, justify='left', wraplength=574, borderwidth=0, font=('Calibri', 10,),
                           bg=background_color, fg=font_color)
    about_label.place(relx=.5, rely=.5, anchor='center', bordermode='outside')


    # Starts timer(). Allows only one instance of timer() running.
    def start_function():
        mixer.init()
        if not mixer.music.get_busy() and counter_seconds > 0:
            global flow
            flow += 1
            if flow == 1:
                timer()


    # Start button
    start_button = tk.Button(root, activebackground=background_color, activeforeground=font_color, height=1, text='Start',
                             borderwidth=5, font=(project_font, 20, 'bold'), bg=background_color, fg=font_color,
                             command=start_function)
    canvas.create_window(200, 250, height=57, width=90, anchor='nw', window=start_button)


    # Counts down seconds, updates time label every second. Counts seconds of worktime and breaks passed.
    # Triggers timer_update(), goal_update(), goal_update() and play_music().
    def timer():
        global flow
        mixer.init()
        if not mixer.music.get_busy() and flow > 0:
            global work_passed
            global break_passed
            global counter_seconds
            if counter_seconds >= 0:
                timer_label['text'] = timer_update(counter_seconds)
                counter_seconds -= 1
                if work_check:
                    work_passed += 1
                else:
                    break_passed += 1
                if work_passed % 60 == 0:  # Updating Progress Gauge and Goal Completion every minute.
                    goal_update()
                    pointer_update()
                root.after(985, timer)  # 15 milliseconds subtracted for timer() operation time.
            else:  # If timer reaches 0 it plays sound and resets its instance counter.
                flow = 0
                play_music()


    # Stops timer(), sets timer() to count time as a break.
    def break_function():
        mixer.quit()
        global counter_seconds
        global work_check
        global flow
        flow = 0
        counter_seconds = break_minutes.get() * 60
        timer_label['text'] = timer_update(counter_seconds)
        work_check = False


    # Break button
    break_button = tk.Button(root, activebackground=background_color, activeforeground=font_color, text='Break',
                             borderwidth=5, font=(project_font, 20, 'bold'), background=background_color, fg=font_color,
                             command=break_function)
    canvas.create_window(310, 80, height=57, width=90, anchor='nw', window=break_button)

    # Starting app window.
    root.tk.mainloop()


# Creating Progress Gauge text and drawing.
def arc_color_update(degree):
    change = int((255/180)*degree)  # Jump in colour value for each degree of arc angle.
    color_c = f'#{change:02x}{255-change:02x}00'
    return color_c


# Controls user goal % accomplishment for pointer_update().
def completion(work_passed, goal_minutes):
    if goal_minutes == 0:
        return 0
    elif goal_minutes * 60 <= work_passed:
        return 100
    else:
        return round(((work_passed/60)/goal_minutes)*100)


# It's used to read counter_seconds global value and update Timer label.
def timer_update(counter_seconds):
    minutes, seconds = divmod(counter_seconds, 60)
    return f'{minutes:02d}:{seconds:02d}'


if __name__ == "__main__":
    main()
