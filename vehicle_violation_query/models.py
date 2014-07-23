from django.db import models


class City(models.Model):

    name = models.CharField(max_length=40)
    pinyin = models.CharField(max_length=20)
    parent = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'city'


class CarInfo(models.Model):

    license_plate_num = models.CharField(max_length=6)
    engine_no = models.CharField(max_length=6)

    class Meta:
        db_table = 'car_info'


class ViolationRecord(models.Model):

    car_info = models.ForeignKey(CarInfo, db_column='car_info')
    area = models.CharField(max_length=50)
    money = models.IntegerField()
    chuli = models.CharField(max_length=10)
    fen = models.IntegerField()
    date = models.CharField(max_length=20)
    act = models.CharField(max_length=100)

    class Meta:
        db_table = 'violation_record'
