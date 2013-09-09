# PyRSS Reader v0.0.1
# https://github.com/rayeshman/PyRSS-Reader
# See Licence

from gi.repository import Gtk,WebKit
import feedparser,socket

class MyWindow(Gtk.Window):

    def __init__(self):

        # Socket Settings #
        timeout = 120
        socket.setdefaulttimeout(timeout)
        
        # An empty window #
        Gtk.Window.__init__(self, title="PyRSS Reader")
        self.set_size_request(1000, 700)

        ##### Some objects #

        ### Boxes
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.hbox = Gtk.Box()
        
        ## List Store
        self.liststore = Gtk.ListStore(str, str, str, str) 
        self.treeview = Gtk.TreeView(self.liststore)
        self.txtrenderer = Gtk.CellRendererText()
        self.column1 = Gtk.TreeViewColumn('Feed summary', self.txtrenderer,text=1)
        self.treeview.append_column(self.column1)
        self.treeview.connect("row-activated", self.tree_doubleclick)
        
        ## WebKit Object
        self.webview = WebKit.WebView()
        self.webview.load_html_string('<center><h1>PyRRS Reader</h1><h6><a href=\"https://github.com/rayeshman/PyRSS-Reader\">v0.0.1</a></h6></center><br>',"file:///")

        ## Scrolled Windows
        scrolledwindow = Gtk.ScrolledWindow(hexpand = True, vexpand = True)
        scrolledwindow2 = Gtk.ScrolledWindow(hexpand = True , vexpand = True)
        
        # Paned
        self.panes=Gtk.HPaned()
        self.panes.pack1(scrolledwindow2,  True, True)
        self.panes.pack2(scrolledwindow,  True,  True)
        
        ## Import Entry
        self.entry = Gtk.Entry(text='')
        
        ## Import Button
        self.button = Gtk.Button("Import")
        self.button.connect("clicked", self.on_button_clicked)

        ## RTL CheckButton
        self.checkbutton = Gtk.CheckButton(label="Force RTL?")
        self.checkbutton.connect("clicked", self.on_checkbutton_clicked)
        
        ## Spinner
        self.spinner = Gtk.Spinner()
        
        ##### /Some objects #
        
        # Put things on the window! #
        ## V Box
        self.add(self.vbox)
        self.vbox.pack_start(self.panes, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
        
        ## Hbox
        self.hbox.pack_start(self.entry, True, True, 0)
        self.hbox.pack_start(self.button, False,False, 0)
        self.hbox.pack_start(self.checkbutton, False, False, 0)
        self.hbox.pack_start(self.spinner, False, False, 0)

        #Scrolled Window
        scrolledwindow.add(self.webview)
        scrolledwindow2.add(self.treeview)
        
        # /Put things on the window! #

    def fill_treeview(self):
        self.liststore.clear()
        self.ident = feedparser.parse(self.feed_url)
        for i in range(len(self.ident.entries)):
            #get the date/timer
            time=self.ident.entries[i].updated
            title=self.ident.entries[i].title
            summary=self.ident.entries[i].summary
            link=self.ident.entries[i].link
            self.liststore.append([time, title, summary, link])

    def tree_doubleclick(self, tree,  path,  column):
        self.title = self.liststore[path[0]][1]
        self.content = self.liststore[path[0]][2]
        self.url = self.liststore[path[0]][3]
        if self.checkbutton.get_active():
            self.webview.load_html_string("<body dir=\"rtl\">" + "<strong>عنوان:"+self.title + "</strong><br/>" + self.content +"<br/>آدرس: " +"<a href=\""+ self.url + "\">" + self.title + "</a>","file:///")
        else :
            self.webview.load_html_string("<strong>Title:"+self.title + "</strong><br/>" + self.content +"<br/>URL: " + "<a href=\""+ self.url + "\">" + self.title + "</a>","file:///")
    
    def on_button_clicked(self,a):
        self.feed_url = self.entry.get_text()
        if self.feed_url.find("://") == -1:
            self.feed_url = "http://" + self.feed_url
            self.entry.set_text(self.feed_url)
        self.fill_treeview()


    def on_checkbutton_clicked(self,a):
        if self.checkbutton.get_active():
            self.webview.load_html_string("<body dir=\"rtl\">" + "<strong>عنوان:"+self.title + "</strong><br/>" + self.content +"<br/>آدرس: " +"<a href=\""+ self.url + "\">" + self.title + "</a>","file:///")
        else :
            self.webview.load_html_string("<strong>Title:"+self.title + "</strong><br/>" + self.content +"<br/>URL: " + "<a href=\""+ self.url + "\">" + self.title + "</a>","file:///")

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()