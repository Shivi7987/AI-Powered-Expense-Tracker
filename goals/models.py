# # 


# from django.db import models
# from django.contrib.auth.models import User

# class Goal(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     amount_to_save = models.DecimalField(max_digits=10, decimal_places=2)
#     current_saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     is_achieved = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name

#     @property
#     def calculate_progress(self):
#         if self.amount_to_save == 0:
#             return {"saved_percentage": 0}
#         percentage = (self.current_saved_amount / self.amount_to_save) * 100
#         return {"saved_percentage": round(percentage, 2)}

# from django.db import models
# from django.contrib.auth.models import User

# class Goal(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     amount_to_save = models.DecimalField(max_digits=10, decimal_places=2)
#     current_saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     is_achieved = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name

#     @property
#     def progress_percentage(self):
#         if self.amount_to_save == 0:
#             return 0
#         return round((self.current_saved_amount / self.amount_to_save) * 100, 2)

from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    amount_to_save = models.DecimalField(max_digits=10, decimal_places=2)
    current_saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_achieved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def calculate_progress(self):
        if self.amount_to_save == 0:
            return {"saved_percentage": 0}

        percentage = (self.current_saved_amount / self.amount_to_save) * 100
        return {"saved_percentage": round(percentage, 2)}