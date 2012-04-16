import datetime

from django.contrib.auth.models import User
from django.db import models

from markdown import markdown

class Category(models.Model):
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text='Suggested value automatically generated from title. Must be unique.')
    description = models.TextField()
    
    def live_idea_set(self):
        from alva.models import Idea
        return self.idea_set.filter(status=Idea.LIVE_STATUS)
    
    class Meta: 
        ordering = ['title']
        verbose_name_plural="Categories"
    
    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('alva_category_detail', (), { 'slug': self.slug })
        

class LiveIdeaManager(models.Manager):
    def get_query_set(self):
        return super(LiveIdeaManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Idea(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Public'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Private'),
    )
    
    #core fields
    title = models.CharField(max_length=250, help_text="Maximum 250 characters.")
#    excerpt = models.TextField(blank=True, help_text="A short summary of the entry. Optional.")
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    
    #fields to store generated HTML
#    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank = True)
    
    #metadata
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
#    featured = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, help_text="Suggested value automatically generated from title. Must be unique.")
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS, help_text="Only entries with live status will be publicly displayed.")
    
    #Categorization
    categories = models.ManyToManyField(Category)
#    tag = TagField(help_text="Separate tags with spaces.")
    
    #For the filtering of live entries
    objects = models.Manager()
    live = LiveIdeaManager()
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = "Ideas"
    
    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            self.excerpt_html = markdown(self.excerpt)
        super(Idea, self).save(force_insert, force_update)

#have to fix thisTODO
    @models.permalink
    def get_absolute_url(self):
        #return "/weblog/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)
        return ('coltrane_entry_detail', (), { 'year': self.pub_date.strftime("%Y"), 'month': self.pub_date.strftime("%b").lower(), 'day': self.pub_date.strftime("%d"), 'slug': self.slug })
    
    #get_absolute_url = models.permalink(get_absolute_url)


#TODO
from akismet import Akismet
from django.conf import settings            
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_will_be_posted
from django.contrib.sites.models import Site
from django.core.mail import mail_managers
from django.utils.encoding import smart_str

class IdeaModerator(CommentModerator):
    auto_moderate_field = 'pub_date'
    moderate_after = 30
    email_notification = True
    
    def moderate(self, comment, content_object, request):
        already_moderated = super(IdeaModerator, self).moderate(comment, content_object)
        if already_moderated:
            return True
        akismet_api = Akismet(key=settings.AKISMET_API_KEY, blog_url="http:/%s/" % Site.objects.get_current().domain)
        if akismet_api.verify_key():
            akismet_data = { 'comment_type': 'comment', 'referrer': request.META['HTTP_REFERER'], 'user_ip': comment.ip_address, 'user-agent': request.META['HTTP_USER_AGENT']}
            return akismet_api.comment_check(smart_str(comment.comment), akismet_data, build_data=True)
        return False
    
moderator.register(Entry, EntryModerator)