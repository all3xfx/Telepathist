import sqlite3
import sys
from tkinter import *

db=sqlite3.connect('animal.db')

ans=''
def init_database():

    try:
        db.execute('CREATE TABLE objects(id integer primary key AUTOINCREMENT,name text);')
        db.execute('CREATE TABLE questions(id integer primary key AUTOINCREMENT,q text);')
        db.execute('CREATE TABLE data(object_id integer,question_id integer,value text);')
        db.execute('insert into objects(name) values(?)',('elephant',))
        db.execute('insert into objects(name) values(?)',('zebra',))
        db.execute('insert into objects(name) values(?)',('cheetah',))
        db.execute('insert into objects(name) values(?)',('cat',))
        db.execute('insert into objects(name) values(?)',('dog',))
        db.execute('insert into questions(q) values(?)',('Is it a carnivore',))
        db.execute('insert into questions(q) values(?)',('Does the animal has specific colour/pattern',))
        db.execute('insert into questions(q) values(?)',('Is it domesticable',))
        db.execute('insert into questions(q) values(?)',('Is it Bigger than buffallo',))
        db.execute('insert into questions(q) values(?)',('Is it a stronger than human',))
        db.execute('insert into questions(q) values(?)',('Is it called the mans best friend',))
        db.execute('insert into data values(?,?,?)',(1,1,'no'))
        db.execute('insert into data values(?,?,?)',(2,1,'no'))  
        db.execute('insert into data values(?,?,?)',(3,1,'yes'))  
        db.execute('insert into data values(?,?,?)',(4,1,'yes'))  
        db.execute('insert into data values(?,?,?)',(5,1,'yes'))
        db.execute('insert into data values(?,?,?)',(1,2,'yes'))
        db.execute('insert into data values(?,?,?)',(2,2,'yes'))  
        db.execute('insert into data values(?,?,?)',(3,2,'yes'))  
        db.execute('insert into data values(?,?,?)',(4,2,'no'))  
        db.execute('insert into data values(?,?,?)',(5,2,'no'))
        db.execute('insert into data values(?,?,?)',(1,3,'no'))
        db.execute('insert into data values(?,?,?)',(2,3,'no'))  
        db.execute('insert into data values(?,?,?)',(3,3,'no'))  
        db.execute('insert into data values(?,?,?)',(4,3,'yes'))  
        db.execute('insert into data values(?,?,?)',(5,3,'yes')) 
        db.execute('insert into data values(?,?,?)',(1,4,'yes'))
        db.execute('insert into data values(?,?,?)',(2,4,'no'))  
        db.execute('insert into data values(?,?,?)',(3,4,'no'))  
        db.execute('insert into data values(?,?,?)',(4,4,'no'))  
        db.execute('insert into data values(?,?,?)',(5,4,'no'))   
        db.execute('insert into data values(?,?,?)',(1,5,'yes'))
        db.execute('insert into data values(?,?,?)',(2,5,'no'))  
        db.execute('insert into data values(?,?,?)',(3,5,'yes'))  
        db.execute('insert into data values(?,?,?)',(4,5,'no'))  
        db.execute('insert into data values(?,?,?)',(5,5,'no'))
        db.execute('insert into data values(?,?,?)',(1,6,'no'))
        db.execute('insert into data values(?,?,?)',(2,6,'no'))  
        db.execute('insert into data values(?,?,?)',(3,6,'no'))  
        db.execute('insert into data values(?,?,?)',(4,6,'no'))  
        db.execute('insert into data values(?,?,?)',(5,6,'yes'))
                                   
        db.commit()
    except :
        pass


def entropy(objects,question):
    '''Entropy is low if for a given question, the number of yes and no
       answers is approx equal.'''
    
    
    yeses= get_num_positives(objects, question)
    
    nos= get_num_negatives(objects, question)
    
    question_entropy = 0
    
    question_entropy += yeses * 1
    question_entropy -= nos * 1
    
    
    return abs(question_entropy)



def get_num_positives(object_tuple, question_id):
    '''Returns the number of objects in the object_tuple where the value for the
       given question_id is positive.'''
       
    
    
    where = "object_id IN %s AND question_id=%d AND value='yes'" %(object_tuple, question_id)
    rows = db.execute('select count(*) from data where '+where)
    return int((tuple(rows))[0][0])
  

def get_num_negatives(object_tuple, question_id):
    '''Returns the number of objects in the object_tuple where the value for the
       given question_id is negative.'''
       

    
    where = "object_id in %s AND question_id=%d AND value='no'" %(object_tuple, question_id)
    rows = db.execute('select count(*) from data where '+where)
    return int((tuple(rows))[0][0])
   
  
def get_objects():
    '''Returns all the objects in database'''
    return db.execute('select * from objects')
    
def get_data(ans, question_id,objects):
    '''Returns the object ids which satisfy condition in the database.'''
    
    l=[]
    where = "value='"+ans+"' AND question_id="+str(question_id)
    for i in db.execute("select object_id from data where "+where):
        if i[0] in objects:
            l.append(i[0]) 
       
    return l   

def get_questions():
    '''Returns all the questions in the database'''
    
    return db.execute('select * from questions')    

def yes_count(q_id):
    '''counts the number of yes for a particular question in the data table '''
    
    return tuple(db.execute("select count(*) from data where question_id=%d AND value='yes'" %(q_id)))[0][0]
    
class diag: 
  def __init__(self, parent,quest,yesno): 
                              
    self.parent=parent 
    self.yesno=yesno
    self.parent.bind("<Return>", self.ok)
    self.parent.bind("<Escape>", self.quit)              
    self.l1=Label(self.parent, text=(quest+self.yesno))
    self.l1.pack()                      
 
    self.e1=Entry(self.parent, bd =5)
    self.e1.pack()
    self.e1.focus_set()  
    
    self.b1=Button(self.parent, borderwidth=2, text="OK", bd=5)    
    self.b1.pack(side=LEFT) 
    self.b1.bind("<ButtonPress-1>", self.ok) 
    
    self.b2=Button(self.parent, borderwidth=2, text="Quit", bd=5) 
    self.b2.pack(side = RIGHT) 
    self.b2.bind("<ButtonPress-1>", self.quit)  
 
  def ok(self, event=None): 
    global ans                          
    ans=self.e1.get()
    self.parent.destroy()
  def quit(self, event=None): 
      sys.exit(0)  
    

def main():
    global ans
    init_database()
    objects = get_objects()
    objects = [obj[0] for obj in objects]
    questions =list(get_questions()) 
    while len(objects)!=1 and  questions: 
        index=0   
        q_id=questions[0][0]
        minimum=entropy(tuple(objects), questions[0][0])
        for i,question in enumerate(questions):
            if minimum>entropy(tuple(objects), question[0]):
                q_id=question[0]
                index=i
                minimum=entropy(tuple(objects), question[0])
        root = Tk()
        diag(root,questions[index][1]," (yes/no)")
        root.mainloop() 
        objects=get_data(ans,q_id,objects)
        questions.pop(index)
    i=objects[0]
    objects = tuple(get_objects())  
    root = Tk()
    diag(root,"our guess is "+objects[i-1][1]+' is it right '," (yes/no)")
    root.mainloop()
    if ans=='no':
        root = Tk()
        diag(root,"could you please provide some details so that we can enter it in our database"," (yes/no)")
        root.mainloop()
        if ans=='yes':
            root = Tk()
            diag(root,"enter the name of the animal"," ")
            root.mainloop()
            db.execute('insert into objects(name) values(?)',(ans,))
            root = Tk()
            diag(root,"enter a question which is specific to it(which has an answer yes to it)",'')
            root.mainloop()
            db.execute('insert into questions(q) values(?)',(ans,))
            objects = tuple(get_objects())
            questions =tuple(get_questions())
            obj=objects[-1][0]
            question=questions[-1][0]
            db.execute('insert into data values(?,?,?)',(obj,question,'yes'))
            for i in objects:
                if i[0]!=objects[-1][0]:
                    db.execute('insert into data values(?,?,?)',(i[0],question,'no'))
            root = Tk()
            diag(root,"please answer a few more questions","")
            root.mainloop()
            for i in questions :
                if i[0] !=question:                   
                    if yes_count(i[0]) != 1 :
                        root = Tk()
                        diag(root,i[1]," (yes/no)")
                        root.mainloop()
                        db.execute('insert into data values(?,?,?)',(obj,i[0],ans))
                    else:    
                        db.execute('insert into data values(?,?,?)',(obj,i[0],'no'))
            db.commit()    
            

               
main() 