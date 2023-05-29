from django.db import models
from datetime import datetime,date,time
from django.utils.timezone import now

class GeneralInfo(models.Model):
    """
    Model for general information about a device.
    """

    dev_id = models.IntegerField(primary_key=True)
    dev_name = models.CharField(max_length=60, verbose_name="Device Name")
    dev_ip_address = models.CharField(max_length=30, null=True, blank=True, help_text="IP address in the format '192.168.1.1'")

    class Meta:
        verbose_name = "General Info"
        verbose_name_plural = "General Infos"

    def __str__(self):
        return self.dev_name


class PerformanceMetrics(models.Model):
    """
    Model for performance metrics of a device.
    """

    dev_id = models.ForeignKey(GeneralInfo, on_delete=models.CASCADE)
    cpu_percentage_used = models.FloatField(max_length=5)
    memory_percentage_used = models.FloatField(max_length=5)
    harddisk_percentage_used = models.FloatField(max_length=5)

    class Meta:
        verbose_name = "Performance Metrics"
        verbose_name_plural = "Performance Metrics"


class AdvancedInfo(models.Model):
    """
    Model for advanced information about a device.
    """

    dev_id = models.ForeignKey(GeneralInfo, on_delete=models.CASCADE)
    dev_manufacturer = models.CharField(max_length=60, verbose_name="Device Manufacturer")
    dev_model = models.CharField(max_length=60, verbose_name="Device Model")
    dev_os = models.CharField(max_length=60, verbose_name="Device OS")
    dev_ssh_port = models.IntegerField(default=22, verbose_name="SSH Port")
    dev_snmp_port = models.IntegerField(default=161, verbose_name="SNMP Port")

    class Meta:
        verbose_name = "Advanced Info"
        verbose_name_plural = "Advanced Infos"


class StatusInfo(models.Model):
    """
    Model for status information of a device.
    """

    dev_id = models.ForeignKey(GeneralInfo, on_delete=models.CASCADE)
    dev_status = models.IntegerField(default=-1, verbose_name="Device Status")
    dev_ping_status = models.BooleanField(verbose_name="Device Ping Status")
    dev_ssh_status = models.BooleanField(verbose_name="Device SSH Status")
    dev_snmp_status = models.BooleanField(verbose_name="Device SNMP Status")

    class Meta:
        verbose_name = "Status Info"
        verbose_name_plural = "Status Infos"

class CpuHistory(models.Model):
    dev_id = models.ForeignKey(GeneralInfo, on_delete=models.CASCADE)
    cpu_percentage_used = models.FloatField(max_length=5)
    dev_date = models.DateField(default=date.today)
    dev_time = models.TimeField(default=datetime.now)

    class Meta:
        verbose_name = "CPU History"
        verbose_name_plural = "CPU History"

class MemoryHistory(models.Model):
    dev_id = models.ForeignKey(GeneralInfo, on_delete=models.CASCADE)
    memory_percentage_used = models.FloatField(max_length=5)
    dev_date = models.DateField(default=date.today)
    dev_time = models.TimeField(default=datetime.now)

    class Meta:
        verbose_name = "Memory History"
        verbose_name_plural = "Memory History"
    

