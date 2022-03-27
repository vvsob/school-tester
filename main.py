import json
from tkinter import *
from PIL import Image, ImageTk


class ScaleAnswer(Frame):
    def __answer(self):
        print(self.__scale.get())
        self.__pv.show_solution(self.__scale.get(), self.__options['value'],
                                abs(self.__scale.get() - self.__options['value']) <= self.__options['delta'])

    def __init__(self, pv, root, options, **kwargs):
        super().__init__(root, **kwargs)
        self.__pv = pv
        self.__root = root
        self.__options = options

        if 'resolution' not in options:
            options['resolution'] = 1

        if 'cursor' not in options:
            options['cursor'] = options['from']

        if 'delta' not in options:
            options['delta'] = 0

        self.__scale = Scale(self,
                             from_=options['from'],
                             to=options['to'],
                             resolution=options['resolution'],
                             orient='horizontal')
        self.__scale.set(options['cursor'])
        self.__correct = options['value']
        self.__scale.grid(row=0, column=0)

        self.__answer_button = Button(self, text='Ответить', command=self.__answer)
        self.__answer_button.grid(row=0, column=1)


class RadiobuttonAnswer(Frame):
    def __answer(self):
        print(self.__var.get())
        self.__pv.show_solution(self.__var.get(), self.__options['value'],
                                self.__var.get() == self.__options['value'])

    def __init__(self, pv, root, options, **kwargs):
        super().__init__(root, **kwargs)
        self.__pv = pv
        self.__root = root
        self.__options = options

        self.__var = StringVar()
        self.__var.set(options['choices'][0])
        self.__radiobuttons = [Radiobutton(self, text=s, variable=self.__var, value=s) for s in
                               options['choices']]
        for i, rb in enumerate(self.__radiobuttons):
            rb.grid(row=i, column=0)

        self.__answer_button = Button(self, text='Ответить', command=self.__answer)
        self.__answer_button.grid(row=0, column=1)


class EntryAnswer(Frame):
    def __answer(self):
        print(self.__var.get())
        self.__pv.show_solution(self.__var.get(), self.__options['value'],
                                self.__var.get() == self.__options['value'])

    def __init__(self, pv, root, options, **kwargs):
        super().__init__(root, **kwargs)
        self.__pv = pv
        self.__root = root
        self.__options = options

        self.__var = StringVar()
        self.__entry = Entry(self, textvariable=self.__var)
        self.__entry.grid(row=0, column=0)

        self.__answer_button = Button(self, text='Ответить', command=self.__answer)
        self.__answer_button.grid(row=0, column=1)


type_to_class = {'scale': ScaleAnswer, 'radiobutton': RadiobuttonAnswer, 'entry': EntryAnswer}


class SolutionFrame(Frame):
    def show(self, guess, answer, is_correct):
        if is_correct:
            self.solution_label.config(text=f'Правильно! Ответ: {answer}')
        else:
            self.solution_label.config(text=f'Неправильно! Ответ: {answer}')

    def __init__(self, pv, root, **kwargs):
        super().__init__(root, **kwargs)
        self.__pv = pv
        self.__root = root

        self.solution_label = Label(self)
        self.solution_label.grid(row=0, column=0)

        self.continue_button = Button(self, text='Продолжить', command=self.__pv.next_problem)
        self.continue_button.grid(row=0, column=1)


class ProblemViewer(Frame):
    def load_problem(self, index=None):
        self.__solution_frame.grid_remove()

        if index is None:
            index = self.__index
        problem = self.__problems[index]
        self.__statement_label.config(text=problem['statement'])
        print(problem['statement'])

        if 'image' in problem:
            self.__img = Image.open(problem['image'])
            self.__img.thumbnail((300, 300), Image.ANTIALIAS)
            self.__image_canvas.config(width=self.__img.width, height=self.__img.height)
            self.__photo = ImageTk.PhotoImage(self.__img)
            self.__image_canvas.create_image(0, 0, anchor='nw', image=self.__photo)
        else:
            self.__image_canvas.delete('all')
            self.__image_canvas.config(width=0, height=0)

        self.__answer_frame.destroy()
        self.__answer_frame = type_to_class[problem['answer']['type']](self,
                                                                       self.__answer_container,
                                                                       problem['answer'])
        self.__answer_frame.pack()

    def show_solution(self, guess, answer, is_correct):
        self.__solution_frame.grid()
        self.__solution_frame.show(guess, answer, is_correct)

    def next_problem(self):
        self.__index = (self.__index + 1) % len(self.__problems)
        self.load_problem()

    def __init__(self, root, problems, **kwargs):
        super().__init__(root, **kwargs)
        self.__root = root
        self.__problems = problems
        self.__index = 0

        self.__statement_label = Label(self, justify="left", wraplength=600)
        self.__statement_label.grid(row=0, column=0)

        self.__answer_container = Frame(self)
        self.__answer_container.grid(row=1, column=0)

        self.__image_canvas = Canvas(self, height=0, width=0)
        self.__image_canvas.grid(row=0, rowspan=2, column=1, sticky='n')

        self.__answer_frame = Frame(self.__answer_container)
        self.__answer_frame.pack()

        self.__solution_frame = SolutionFrame(self, self)
        self.__solution_frame.grid(row=2, column=0)

        self.load_problem()


def main():
    with open("data/problems.json", 'r', encoding='utf-8') as problems_file:
        problems = json.load(problems_file)

    tk = Tk()
    tk.geometry('1000x600')

    viewer = ProblemViewer(tk, problems['problems'])
    viewer.grid(row=0)

    tk.mainloop()


if __name__ == '__main__':
    main()
