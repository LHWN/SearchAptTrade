from django.db import models

# Create your models here.


class Trade(models.Model):
    aptDong = models.CharField(max_length=255),
    aptNm = models.CharField(max_length=255)

    def __str__(self):
        return self.aptNm

class AptTrade(models.Model):
    id = models.BigAutoField(primary_key=True)
    aptdong = models.CharField(db_column='APTDONG', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aptnm = models.CharField(db_column='APTNM', max_length=255, blank=True, null=True)  # Field name made lowercase.
    buildyear = models.CharField(db_column='BUILDYEAR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cdealday = models.CharField(db_column='CDEALDAY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cdealtype = models.CharField(db_column='CDEALTYPE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dealamount = models.CharField(db_column='DEALAMOUNT', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dealday = models.CharField(db_column='DEALDAY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dealmonth = models.CharField(db_column='DEALMONTH', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dealyear = models.CharField(db_column='DEALYEAR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dealinggbn = models.CharField(db_column='DEALINGGBN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    excluusear = models.CharField(db_column='EXCLUUSEAR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    floor = models.CharField(db_column='FLOOR', max_length=255, blank=True, null=True)  # Field name made lowercase.
    jibun = models.CharField(db_column='JIBUN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    landleaseholdgbn = models.CharField(db_column='LANDLEASEHOLDGBN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rgstdate = models.CharField(db_column='RGSTDATE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sggcd = models.CharField(db_column='SGGCD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    slergbn = models.CharField(db_column='SLERGBN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    umdnm = models.CharField(db_column='UMDNM', max_length=255, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'apt_trade'

    def __str__(self):
        return self.aptnm