#!/usr/bin/python2

from pprint import pprint

from modhandler import ModLoader
from crosscompat import SLASH
from filelist import getMods
from cleanup import clean
from runner import runGame

import pygtk
pygtk.require('2.0')
import gtk

class ModToggler:

    def listbox(self, columnTitle):
        retObj = {}

        retObj['treestore'] = gtk.TreeStore(str)

        retObj['treeview'] = gtk.TreeView(retObj['treestore'])
        retObj['treeview'].set_reorderable(False)

        retObj['cell'] = gtk.CellRendererText()

        retObj['tvcolumn'] = gtk.TreeViewColumn(columnTitle)
        retObj['tvcolumn'].pack_start(retObj['cell'], True)
        retObj['tvcolumn'].add_attribute(retObj['cell'], 'text', 0)

        retObj['tvselection'] = retObj['treeview'].get_selection()
        retObj['tvselection'].set_mode(gtk.SELECTION_MULTIPLE)

        retObj['treemodel'] = retObj['treeview'].get_model()

        retObj['treeview'].append_column(retObj['tvcolumn'])

        return retObj


    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        self.window.destroy()
        gtk.main_quit()

    def start(self, widget, data):
        arr = []
        def dofor(model, path, theiter, data=None):
            arr.append(self.data[model.get_value(theiter, 0)])
        data['treemodel'].foreach(dofor)
        self.window.hide()
        while gtk.events_pending():
            gtk.main_iteration(block=False)
        ModLoader(arr).prepMods().load()
        runGame()
        clean()
        gtk.main_quit()

    def exit(self, widget, data=None):
        gtk.main_quit()

    def deselect(self, widget, data):
        selected, deselected = data
        paths = deselected['tvselection'].get_selected_rows()[1]
        for path in paths:
            try:
                deselected['tvselection'].unselect_path(path)
            except:
                print('o dam')

    def move_items(self, widget, data):
        fromlist, tolist = data
        paths = fromlist['tvselection'].get_selected_rows()[1]
        for path in paths:
            try:
                theiter = fromlist['treemodel'].get_iter(path)
                string = fromlist['treemodel'].get_value(theiter, 0)
                tolist['treestore'].append(None, [string])
                fromlist['treestore'].remove(theiter)
            except:
                self.buttons['rightButton'].clicked()

    def move_up(self, widget, data):
        tvselection = data['tvselection']
        treemodel = data['treemodel']
        treestore = data['treestore']

        paths = tvselection.get_selected_rows()[1]
        fstrpath = treemodel.get_string_from_iter(treemodel.get_iter(paths[0]))
        try:
            previter = treemodel.get_iter_from_string(str(int(fstrpath)-1))
            for path in paths:
                treestore.move_before(treemodel.get_iter(path), previter)
        except:
            print('i mean oh well i guess')

    def move_down(self, widget, data):
        tvselection = data['tvselection']
        treemodel = data['treemodel']
        treestore = data['treestore']

        paths = tvselection.get_selected_rows()[1]
        lstrpath = treemodel.get_string_from_iter(treemodel.get_iter(paths[-1]))
        try:
            nextiter = treemodel.get_iter_from_string(str(int(lstrpath)+1))
            for path in reversed(paths):
                treestore.move_after(treemodel.get_iter(path), nextiter)
        except:
            print('i mean oh well i guess')


    def load_data(self, arr):
        self.data = {}
        for archive in arr:
            self.data['.'.join(archive.split(SLASH)[-1].split('.')[:-1]).replace('_',' ')] = archive
        self.update(self.listbox1)

    def update(self, listbox):
        for name, path in self.data.items():
            listbox['treestore'].append(None, [name])

    def __init__(self, title):
        self.data = {}

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect('delete_event', self.delete_event, None)
        self.window.connect('destroy', self.destroy, None)
        self.window.set_border_width(10)
        self.window.set_size_request(800, 500)
        self.window.set_title(title)

        self.listbox1 = self.listbox('Unloaded')
        self.listbox2 = self.listbox('Loaded')
        self.listbox1['treeview'].connect('cursor_changed', self.deselect, (self.listbox1, self.listbox2))
        self.listbox2['treeview'].connect('cursor_changed', self.deselect, (self.listbox2, self.listbox1))

        self.buttons = {
            'rightButton': gtk.Button('>'),
            'leftButton': gtk.Button('<'),
            'upButton': gtk.Button('^'),
            'downButton': gtk.Button('v'),
            'startButton': gtk.Button('Start'),
            'exitButton': gtk.Button('Exit')
        }

        self.label = gtk.Label('Mods load from the top-down, so the last in the list get precedence.')

        self.buttons['rightButton'].connect('clicked', self.move_items, (self.listbox1, self.listbox2))
        self.buttons['leftButton'].connect('clicked', self.move_items, (self.listbox2, self.listbox1))

        self.buttons['upButton'].connect('clicked', self.move_up, self.listbox2)
        self.buttons['downButton'].connect('clicked', self.move_down, self.listbox2)

        self.buttons['startButton'].connect('clicked', self.start, self.listbox2)
        self.buttons['exitButton'].connect('clicked', self.exit, None)

        self.table = gtk.Table(rows=16, columns=22, homogeneous=True)
        self.table.attach(self.listbox1['treeview'],    0, 10,  1, 15, xpadding=5, ypadding=5)
        self.table.attach(self.listbox2['treeview'],   11, 21,  1, 15, xpadding=5, ypadding=5)
        self.table.attach(self.buttons['rightButton'], 10, 11,  5,  7, xpadding=5, ypadding=5)
        self.table.attach(self.buttons['leftButton'],  10, 11,  8, 10, xpadding=5, ypadding=5)
        self.table.attach(self.buttons['exitButton'],  17, 19, 15, 16, xpadding=5, ypadding=5)
        self.table.attach(self.buttons['startButton'], 19, 21, 15, 16, xpadding=5, ypadding=5)
        self.table.attach(self.buttons['upButton'],    21, 22,  1,  3, xpadding=5, ypadding=5)
        self.table.attach(self.buttons['downButton'],  21, 22,  3,  5, xpadding=5, ypadding=5)
        self.table.attach(self.label,                   0, 21,  0,  1, xpadding=5, ypadding=5)

        show = [
            self.table,
            self.listbox1['treeview'],
            self.listbox2['treeview'],
            self.label
        ]

        for name, button in self.buttons.items():
            show.append(button)

        self.window.add(self.table)
        self.window.show()
        for elem in show:
            elem.show()


    def main(self):
        gtk.main()

if __name__ == '__main__':
    toggler = ModToggler('Asterne\'s Modloader')
    toggler.load_data(getMods())
    toggler.main()
