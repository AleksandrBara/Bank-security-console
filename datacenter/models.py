from django.db import models
from django.utils.timezone import localtime


def is_visit_long(visit, seconds=3600):
    return get_duration(visit) > seconds


def get_duration(visit):
    exit_time = visit.leaved_at
    entry_time = visit.entered_at
    timedelta = localtime(exit_time) - localtime(entry_time)
    return timedelta.total_seconds()


def format_duration(duration):
    hours = int(duration) // 3600
    minutes = (int(duration % 3600)) // 60
    formatted_duration = f'{hours}:{minutes}'
    return formatted_duration


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
