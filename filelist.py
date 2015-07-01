import pygtk
pygtk.require('2.0')
import gtk
import time

class ModSwapper:

    def getAll(self):
        arr = []
        def dofor(model, path, theiter, data=None):
            arr.append(model.get_value(theiter, 0))
        self.treemodel2.foreach(dofor)
        return arr

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        self.window.destroy()
        gtk.main_quit()

    def start(self, widget, event, data=None):
        data = self.getAll()
        self.window.hide()
        while gtk.events_pending():
            gtk.main_iteration(block=False)
        self.callback(data)
        del self.window
        gtk.main_quit()

    def add_items(self, widget, event, data=None):
        paths = self.tvselection.get_selected_rows()[1]
        for path in paths:
            try:
                theiter = self.treemodel.get_iter(path)
                string = self.treemodel.get_value(theiter, 0)
                self.treestore2.append(None, [string])
                self.treestore.remove(theiter)
            except:
                self.buttonR.clicked()

    def end(self, widget, event, data=None):
        gtk.main_quit()

    def remove_items(self, widget, event, data=None):
        paths = self.tvselection2.get_selected_rows()[1]
        for path in paths:
            try:
                theiter = self.treemodel2.get_iter(path)
                string = self.treemodel2.get_value(theiter, 0)
                self.treestore.append(None, [string])
                self.treestore2.remove(theiter)
            except:
                self.buttonL.clicked()

    def deselect(self, widget, event, data=None):
        paths = self.tvselection.get_selected_rows()[1]
        for path in paths:
            try:
                self.tvselection.unselect_path(path)
            except:
                print('whoops something broke')

    def deselect2(self, widget, event, data=None):
        paths = self.tvselection2.get_selected_rows()[1]
        for path in paths:
            try:
                self.tvselection2.unselect_path(path)
            except:
                print('more broken things')

    def __init__(self, title, mods, callback):
        self.callback = callback

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('delete_event', self.delete_event)
        self.window.connect('destroy', self.destroy)
        self.window.set_border_width(10)
        self.window.set_size_request(800, 500)
        self.window.set_title(title)

        self.treestore = gtk.TreeStore(str)
        for mod in mods:
            self.treestore.append(None, [mod])
        self.treestore2 = gtk.TreeStore(str)

        self.treeview = gtk.TreeView(self.treestore)
        self.treeview2 = gtk.TreeView(self.treestore2)

        self.treeview.connect('cursor_changed', self.deselect2, None)
        self.treeview2.connect('cursor_changed', self.deselect, None)

        self.cell = gtk.CellRendererText()
        self.cell2 = gtk.CellRendererText()

        self.tvcolumn = gtk.TreeViewColumn('Unloaded')
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)

        self.tvcolumn2 = gtk.TreeViewColumn('Loaded')
        self.tvcolumn2.pack_start(self.cell2, True)
        self.tvcolumn2.add_attribute(self.cell2, 'text', 0)

        self.tvselection = self.treeview.get_selection()
        self.tvselection.set_mode(gtk.SELECTION_MULTIPLE)

        self.tvselection2 = self.treeview2.get_selection()
        self.tvselection2.set_mode(gtk.SELECTION_MULTIPLE)

        self.treemodel = self.treeview.get_model()
        self.treemodel2 = self.treeview2.get_model()

        self.buttonR = gtk.Button('>')
        self.buttonR.connect('clicked', self.add_items, None)

        self.buttonL = gtk.Button('<')
        self.buttonL.connect('clicked', self.remove_items, None)

        self.exitButton = gtk.Button('Exit')
        self.startButton = gtk.Button('Start')
        self.exitButton.connect('clicked', self.end, None)
        self.startButton.connect('clicked', self.start, None)

        self.treeview.append_column(self.tvcolumn)
        self.treeview2.append_column(self.tvcolumn2)

        self.table = gtk.Table(rows=16, columns=21, homogeneous=True)
        self.table.attach(self.treeview, 0, 10, 0, 15, xpadding=5,ypadding=5)
        self.table.attach(self.treeview2, 11, 21, 0, 15, xpadding=5,ypadding=5)
        self.table.attach(self.buttonR, 10, 11, 4, 6, xpadding=5,ypadding=5)
        self.table.attach(self.buttonL, 10, 11, 8, 10, xpadding=5,ypadding=5)
        self.table.attach(self.exitButton, 17, 19, 15, 16, xpadding=5,ypadding=5)
        self.table.attach(self.startButton, 19, 21, 15, 16, xpadding=5,ypadding=5)

        self.window.add(self.table)
        self.table.show()
        self.exitButton.show()
        self.startButton.show()
        self.buttonL.show()
        self.buttonR.show()
        self.treeview.show()
        self.treeview2.show()
        self.window.show()

    def main(self):
        gtk.main()
