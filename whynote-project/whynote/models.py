from django.db import models


class Note(models.Model):
    note_title = models.CharField('the title of a note',
                                  max_length = 200)
    note_text = models.TextField()
    public_date = models.DateTimeField('The publication date')

    def __str__(self):
        return self.note_title
    
class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete = models.CASCADE)
    author_name = models.CharField('The author\'s name', max_length = 70)
    comment_text = models.CharField('The text of a comment', max_length = 200)

    def __str__(self):
        return self.author_name

class Tabsettings(models.Model):
    textcolor = models.CharField('Text color', max_length = 20)
    bgcolor = models.CharField('Background color', max_length = 20)
    textstyle = models.CharField('Text style', max_length = 20)
    fontfamily = models.CharField('Font family', max_length = 50)
    fontsize = models.IntegerField('Font size', max_length = 10)
