import web
import os
import glob

origMessage="""not possible, sorry :-)<br/>
    causes:<br/>
    - image allready deleted<br/>
    - image allready uploaded<br/>
    - image never existed<br/>
    """
def make_text(string):
    return string
def makeDeleteFile(filePaths):
    message=origMessage
    for f in filePaths:
        pathDelete=f[:len(f)-5]+".delete"
        with open(pathDelete, 'w') as doneFile:
            doneFile.write('delete')
            message= "files deleted"
    return message
    
def checkIfDoneFileExist(tokenString):
    try:
        dateString=tokenString.decode('base64')
#    filePath=os.path.join(os.getcwd(),"outgoing/"+dateString+"*.done")
        filePaths=glob.glob(os.path.join(os.getcwd(),"outgoing/"+dateString+"*.done"))
    #if glob.glob(os.path.join(os.getcwd(),"outgoing/"+dateString+"*.done")):
        if filePaths:
            print "made delete file"+str(filePaths[0])
            return filePaths
    except:
        pass
    return None

urls = ('/', 'tutorial')
render = web.template.render('webTemplates/')

app = web.application(urls, globals())

my_form = web.form.Form(
                web.form.Textbox('', class_='textfield', id='textfield'),
                )

class tutorial:
    def GET(self):
        message="not possible, sorry :-)"
        try:
            tokenString=web.input(_method='get')["stringToken"]
            tmp=checkIfDoneFileExist(tokenString)
            if tmp:
                message= makeDeleteFile(tmp)
        except:
            pass
        form = my_form()
        return render.tutorial(form, message)
        
    def POST(self):
        form = my_form()
        form.validates()
        s = form.value['textfield']
        
        tmp=checkIfDoneFileExist(s)
        if tmp:
            return makeDeleteFile(tmp)
        return origMessage

if __name__ == '__main__':
    app.run()

