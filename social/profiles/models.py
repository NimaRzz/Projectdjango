from django.db import models
from accounts.models import User

class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='frelation', blank=True, null=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trelation', blank=True, null=True)
    relation = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} followed  {self.to_user}  at date {self.created}'
    
    def followers(self):
        return self.from_user
    
    def followers_id(self):
        return self.from_user.id
    
    def followings(self):
        return self.to_user
    
    def followings_id(self):
        return self.to_user.id