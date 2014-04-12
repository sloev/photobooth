import web
import os
import glob

def make_text(string):
    return string
def makeDeleteFile(filePath):
    pathDelete=filePath[:len(filePath)-5]
    with open(pathDelete, 'w') as doneFile:
        doneFile.write('delete')
        return "files deleted"
    return "files allready uploaded, sorry :-)"
    
def checkIfDoneFileExist(tokenString):
    dateString=tokenString.decode('base64')
    filePath=os.path.join(os.getcwd(),"outgoing/"+dateString+"*.done")
    print filePath
    if glob.glob(os.path.join(os.getcwd(),"outgoing/"+dateString+"*.done")):
        print filePath
        return filePath[0]
    return None

urls = ('/', 'tutorial')
render = web.template.render('templates/')

app = web.application(urls, globals())

my_form = web.form.Form(
                web.form.Textbox('', class_='textfield', id='textfield'),
                )

class tutorial:
    def GET(self):
        form = my_form()
        return render.tutorial(form, "Your text goes here.")
        
    def POST(self):
        form = my_form()
        form.validates()
        s = form.value['textfield']
        
        tmp=checkIfDoneFileExist(s)
        if tmp:
            return makeDeleteFile(tmp)
        return "files allready uploaded, sorry :-)"

if __name__ == '__main__':
    app.run()

