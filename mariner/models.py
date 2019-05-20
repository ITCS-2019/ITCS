from django.db import models

from django.contrib import admin

#from datetime import datetime
#from django.utils import timezone

#//////////////////////////////////////////////////////////
# class SailorManager(models.Model):
#     def all_with_prefetch_certificates(self):
#         qs = self.get_queryset()
#         return qs.prefetch_related('certificated')



class Sailor(models.Model):
    M = 0
    W = 1
    ISU = 2
    ANU = 3
    SEX = (
        (M, 'Чоловік'),
        (W, 'Жінка')
    )
    first_name_en = models.CharField(max_length=140, blank=True)
    last_name_en = models.CharField(max_length=140, blank=True)
    last_name_ukr = models.CharField(max_length=140)
    first_name_ukr = models.CharField(max_length=140)
    second_name_ukr = models.CharField(max_length=140, blank=True)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)
    inn = models.CharField(max_length=100, null=True, blank=True)
    sex = models.IntegerField(choices=SEX, null=True, default=M)
    # objects = SailorManager()
    class Meta:
        ordering = ('last_name_ukr', 'first_name_ukr')
    def __str__(self):
        return u"%s %s" % (self.last_name_ukr, self.first_name_ukr)


class SailorAdmin(admin.ModelAdmin):
    list_display = ('last_name_ukr', 'first_name_ukr',)
    search_fields = ('last_name_ukr',)

admin.site.register(Sailor, SailorAdmin)

#//////////////////////////////////////////////////////////
class RangeNumber(models.Model):
    number = models.IntegerField(null=True, blank=True)
    organisation_id = models.IntegerField(null=True, blank=True)
    organisation_name = models.CharField(max_length=200, null=True, blank=True)
    direction_id = models.IntegerField(null=True, blank=True)
    direction_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return u"%s / %s / %s" % (self.number, self.direction_name, self.organisation_name)
#//////////////////////////////////////////////////////////
LEVELS = (
        ('---', '---',),
        ('Отримання', 'Отримання'),
        ('Підтвердження', 'Підтвердження')
)

ALLOWS = (
        ('---', '---',),
        ('Управлiння', 'Управлiння'),
        ('Експлуатація', 'Експлуатація')
)

class TrainigDirections(models.Model):
    ACT = 0
    NACT = 1
    DIRECTSTATUS = (
        (ACT, 'Активний'),
        (NACT, 'Не Активний')
    )

    price_id = models.IntegerField(null=True, blank=True)
    direction_title = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=LEVELS, default='---')
    
    allow_functions = models.CharField(max_length=20, choices=ALLOWS, default='---')
    price = models.IntegerField(null=True, blank=True)

    status = models.IntegerField(choices=DIRECTSTATUS, null=True, default=ACT)

    range_numbers = models.ManyToManyField(to='RangeNumber', related_name='ranged', blank=True)
    
    def __str__(self):
        return u"%s / %s / %s /" % (self.direction_title, self.get_allow_functions_display(), self.get_level_display())
        #return u"%s" % (self.direction_title)


class TrainigDirectionsDocAdmin(admin.ModelAdmin):
    list_display = ('price_id', 'direction_title', 'price',)
    search_fields = ('direction_title',)

admin.site.register(TrainigDirections, TrainigDirectionsDocAdmin)

#//////////////////////////////////////////////////////////
class TrainigOrganisation(models.Model):
    organisation_id = models.CharField(max_length=140, blank=True)
    organisation_name = models.CharField(max_length=140, blank=True)
    orgnisation_email = models.CharField(max_length=140, blank=True)
    activated = models.DateField(null=True, blank=True)
    active_till = models.DateField(null=True, blank=True)
    directions = models.ManyToManyField(to='TrainigDirections', related_name='directioned', blank=True)

    def get_certInReview(self):
        return self.trained.filter(status__startswith=1)
    def get_issuedCerts(self):
        return self.trained.filter(status__startswith=2)
    
    def __str__(self):
        return u"%s" % (self.organisation_name)

class TrainigOrganisationAdmin(admin.ModelAdmin):
    list_display = ('organisation_name', 'orgnisation_email',)
    search_fields = ('organisation_name',)
    filter_horizontal = ('directions',)

admin.site.register(TrainigOrganisation, TrainigOrganisationAdmin)        
#//////////////////////////////////////////////////////////
class Certificate(models.Model):
    DRF = 0
    IRV = 1
    ISU = 2
    ANU = 3
    STATUSES = (
        (DRF, 'Чернетка'),
        (IRV, 'Обробка'),
    	(ISU, 'Видан'),
    	(ANU, 'Анульований')
    )
    # NTZ_STATUSES = (
    #     (DRF, 'Чернетка'),
    #     (IRV, 'Обробка')
    # )
    WTL = 0
    TER = 1
    VALID = (
    	(WTL, 'Безстроковий'),
    	(TER, 'Терміновий'),
    )

    certf_number = models.CharField(max_length=40, null=True, blank=True)
    form_number = models.CharField(max_length=40, null=True, blank=True)
    ntz_number = models.CharField(max_length=40, null=True, blank=True)

    first_name_en = models.CharField(max_length=140, blank=True)
    last_name_en = models.CharField(max_length=140, blank=True)
    last_name_ukr = models.CharField(max_length=140)
    first_name_ukr = models.CharField(max_length=140)
    second_name_ukr = models.CharField(max_length=140, blank=True)
    born = models.DateField()
    inn = models.CharField(max_length=100, null=True, blank=True)
    sailor = models.ForeignKey(to='Sailor', null=True, on_delete=models.SET_NULL, related_name='certificated', blank=True)
    
    trainigOrganisation = models.ForeignKey(to='TrainigOrganisation', null=True, on_delete=models.SET_NULL, related_name='trained', blank=True)
    
    date_of_issue = models.DateField(null=True, blank=True)
    valid_date = models.DateField(null=True, blank=True)
    valid_type = models.IntegerField(choices=VALID, null=True, default=WTL)

    direction_level = models.CharField(max_length=20, choices=LEVELS, default='Отримання')
    direction_allow_functions = models.CharField(max_length=20, choices=ALLOWS, default='---')
    training_direction = models.ForeignKey(to='TrainigDirections', null=True, on_delete=models.SET_NULL, related_name='directed', blank=True)

    status = models.IntegerField(choices=STATUSES, null=True, default=DRF)


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('form_number', 'last_name_ukr', 'trainigOrganisation',)
    search_fields = ('form_number',)

admin.site.register(Certificate, CertificateAdmin)
