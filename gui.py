# GUI class
from Tkinter import Label, Button, Entry, W, E, StringVar, PhotoImage, Image
import tkFileDialog
import tkMessageBox
from pre_process import PreProcess
from build_cluster import BuildCluster
from traceback import print_exc
from sys import stdout
import matplotlib.pyplot as plt
from PIL import Image
import plotly.plotly as py


class Gui:
    def __init__(self, master, head_title):
        self.master = master
        self.head_title = head_title
        master.title(head_title)

        # params definition
        self.n_clusters = 4
        self.n_init = 10
        self.file_path = 'C:/'
        self.is_pre_processed = False
        self.processor = None
        self.cluster = None

        # Tkinter gui

        self.file_path_text = StringVar(value=self.file_path)
        self.file_path_label = Label(master, text='Data path:')
        self.file_path_entry = Entry(master, textvariable=self.file_path_text, width=50)
        self.browse_button = Button(master, text='Browse', command=self.browse)

        self.n_clusters_text = StringVar(value=self.n_clusters)
        self.n_clusters_label = Label(master, text='Num of clusters k:')
        self.n_clusters_entry = Entry(master, textvariable=self.n_clusters_text)

        self.n_init_text = StringVar(value=self.n_init)
        self.n_init_label = Label(master, text='Num of runs:')
        self.n_init_entry = Entry(master, textvariable=self.n_init_text)

        self.pre_process_button = Button(master, text='Pre-process', command=self.pre_process)
        self.build_model_button = Button(master, text='Cluster', command=self.build_model)

        self.scatter_label = Label(self.master)
        self.horopleth_label = Label(master)
        # LAYOUT

        self.file_path_label.grid(row=0, column=0, sticky=W)
        self.file_path_entry.grid(row=0, column=1, columnspan=2)
        self.browse_button.grid(row=0, column=2, sticky=E)

        self.n_clusters_label.grid(row=1, column=0, sticky=W)
        self.n_clusters_entry.grid(row=1, column=1, columnspan=2, sticky=W+E)

        self.n_init_label.grid(row=2, column=0, sticky=W)
        self.n_init_entry.grid(row=2, column=1, columnspan=2, sticky=W+E)

        self.pre_process_button.grid(row=3, column=1, sticky=W)
        self.build_model_button.grid(row=4, column=1, sticky=W)

        self.scatter_label.grid(row=5, column=0, sticky=W)
        self.horopleth_label.grid(row=5, column=1, sticky=E)

    def browse(self):
        # browse method for choosing the data file
        path = tkFileDialog.askopenfilename()
        if path is None or path == '':
            return

        self.file_path = path
        self.file_path_text.set(self.file_path)

    def pre_process(self):
        # pre process the data to fit into the algorithm
        if self.processor is not None:
            # if we already ran this, ask the user if he wants to run it again
            result = tkMessageBox.askquestion(
                message="pre-processing has already been made.\nare you sure you want to run it again?'",
                icon='warning', title=self.head_title)
            if result != 'yes':
                return
        self.processor = None
        self.is_pre_processed = False
        try:
            # verify the file can be pre-processed
            self.file_path = self.file_path_text.get()
            processor = PreProcess(self.file_path)
            if processor.verifications() is False:
                tkMessageBox.showerror(title=self.head_title, message=processor.error_message)
                return

            # process the data
            processor.pre_process()
            tkMessageBox.showinfo(title=self.head_title, message='Preprocessing completed successfully')
            self.processor = processor
            self.is_pre_processed = True
        except Exception as err:
            template = "An exception of type {0} occurred. Arguments:{1}"
            message = template.format(type(err).__name__, err)
            print_exc(err, file=stdout)
            tkMessageBox.showerror(title=self.head_title, message=message)

    def build_model(self):
        # build the kmeans model
        if not self.is_pre_processed:
            tkMessageBox.showerror(title=self.head_title, message="pre processing is not validated yet")
            return

        if self.cluster is not None:
            # if we already ran the clustering, verify if we really want to run it again
            result = tkMessageBox.askquestion(
                message="clustering has already been made.\nare you sure you want to run it again?",
                icon='warning', title=self.head_title)
            if result != 'yes':
                return
        self.cluster = None
        try:
            # create the kmeans model
            self.n_clusters = self.n_clusters_text.get()
            self.n_init = self.n_init_text.get()
            model = BuildCluster(self.n_clusters, self.n_init, self.processor.df)
            if model.verifications() is False:
                tkMessageBox.showerror(title=self.head_title, message=model.error_message)
                return

            model.build_cluster()
            self.cluster = model
            # draw the graphs in the gui
            self.draw_graphs()
            tkMessageBox.showinfo(title=self.head_title, message='Clustering Finished successfully!')
        except Exception as err:
            template = "An exception of type {0} occurred. Arguments:{1}"
            message = template.format(type(err).__name__, err)
            print_exc(err, file=stdout)
            tkMessageBox.showerror(title=self.head_title, message=message)

    def draw_graphs(self):
        # draw scatter graph using matPlotLib and plotly
        self.draw_scatter()
        self.draw_horopleth()

    def draw_scatter(self):
        # Draw a scatter plot of Generosity vs social support
        df = self.cluster.df
        fig_path = 'scatter.png'
        plt.scatter(x=df['Generosity'], y=df['Social support'], c=df['cluster'], alpha=0.5)
        plt.xlabel('Generosity')
        plt.ylabel('Social support')
        plt.title("Scatter of Generosity vs Social Support, colored by clusters")
        plt.savefig(fig_path)
        # convert from png to gif
        convert_png_to_gif(fig_path)
        # display in GUI
        photo = PhotoImage(file=fig_path.replace('png', 'gif'))
        self.scatter_label.configure(image=photo, width='400px', height='400px')
        self.scatter_label.image = photo

    def draw_horopleth(self):
        # Draw a horopleth of the country clusters
        df = self.cluster.df
        py.sign_in('omrikipiki', 'VcDvTak2bEIiyOfiaxMj')
        data = [dict(
            type='choropleth',
            locations=df['country'],
            z=df['cluster'],
            text=df['country'],
            locationmode='country names',
            colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"], [0.5, "rgb(70, 100, 245)"],
                        [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"], [1, "rgb(220, 220, 220)"]],
            autocolorscale=False,
            reversescale=True,
            marker=dict(
                line=dict(
                    color='rgb(180,180,180)',
                    width=0.5
                )),
            colorbar=dict(
                # autotick=False,
                title='Cluster Group'),
        )]

        layout = dict(
            title='K-Means Clustering Visualization',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection=dict(
                    type='Mercator'
                )
            )
        )
        fig = dict(data=data, layout=layout)

        py.iplot(fig, validate=False, filename='d3-world-map')

        fig_path = 'choromap.png'
        py.image.save_as(fig, filename=fig_path)
        # convert to gif
        convert_png_to_gif(fig_path)
        # put in GUI
        photo = PhotoImage(file=fig_path.replace('png', 'gif'))
        self.horopleth_label.configure(image=photo, width='600px', height='600px')
        self.horopleth_label.image = photo


def convert_png_to_gif(fig_path):
    # convert png images saved on disk to gif images
    im = Image.open(fig_path)
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
    im.save(fig_path.replace('.png', '.gif'))
