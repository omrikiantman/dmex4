# Main
from Tkinter import Tk
from gui import Gui


def main():
    root = Tk()
    my_gui = Gui(root, 'K Means Clustering')
    root.mainloop()


if __name__ == '__main__':
    main()
