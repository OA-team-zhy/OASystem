from django.db import models
import datetime
from defaultAPP.models import Admin, GeneralUser
from constants import OFFICE_STATUS, OFFICE_OPERATION



def current_year():

    return datetime.date.today().year


class Office(models.Model):
    credits = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    semesters = [
        ("Autumn", "上"),
        ("Spring", "下")
    ]
    name = models.CharField(max_length=50, verbose_name="会议室名称")
    introduction = models.CharField(max_length=250, verbose_name="介绍")
    credit = models.IntegerField(verbose_name="楼号（几号楼）")
    max_number = models.IntegerField(verbose_name="会议室最大人数")

    year = models.IntegerField(verbose_name="年份", default=current_year)
    semester = models.CharField(max_length=20, verbose_name="学期", choices=semesters)

    # 未开始选会议室， 1
    # 开始选会议室，未关闭会议室2
    # 关闭会议室， 3
    # 结束 4
    # 已打完分 5
    status = models.IntegerField(verbose_name="会议室状态", default=1)

    admin = models.ForeignKey(Admin, verbose_name="会议室使用者", on_delete=models.CASCADE)

    def get_status_text(self):
        return OFFICE_STATUS[self.status]

    def get_op_text(self):
        return OFFICE_OPERATION[self.status]

    def get_current_count(self):
        offices = GeneralUserOffice.objects.filter(office=self, with_draw=False)
        return len(offices)

    def get_schedules(self):
        schedules = Schedule.objects.filter(office=self)
        return schedules

    def __str__(self):
        return "%s (%s)" % (self.name, self.admin.name)


def weekday_choices():
    weekday_str = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    return [(i + 1, weekday_str[i]) for i in range(7)]


class Schedule(models.Model):
    weekday = models.IntegerField(choices=weekday_choices(), verbose_name="日期")
    start_time = models.TimeField(verbose_name="使用开始时间")
    end_time = models.TimeField(verbose_name="使用结束时间")
    location = models.CharField(max_length=100, verbose_name="会议室使用地点")
    remarks = models.CharField(max_length=100, verbose_name="备注", null=True, blank=True)

    start_week = models.IntegerField(verbose_name="第几周开始")
    end_week = models.IntegerField(verbose_name="第几周结束")

    intervals = [
        (1, "无间隔"),
       (2, "每隔一周用一次")
    ]
    week_interval = models.IntegerField(verbose_name="周间隔", choices=intervals, default=1)

    office = models.ForeignKey(Office, verbose_name="会议室名称", on_delete=models.CASCADE)

    def __str__(self):
        s = "第%s周-第%s周 " % (self.start_week, self.end_week)
        if self.week_interval == 2:
            s += "隔一周 "
        s += "%s %s-%s " % (self.get_weekday_display(), self.start_time.strftime("%H:%M"),
                            self.end_time.strftime("%H:%M"))
        s += "在%s" % self.location
        if self.remarks:
            s += " %s" % self.remarks
        return s


class GeneralUserOffice(models.Model):
    create_time = models.DateTimeField(auto_now=True)
    with_draw = models.BooleanField(default=False)
    with_draw_time = models.DateTimeField(default=None, null=True)

    scores = models.IntegerField(verbose_name="得分", null=True)
    comments = models.CharField(max_length=250, verbose_name="会议室评价", null=True)

    rates = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]

    rating = models.IntegerField(verbose_name="用户评分", choices=rates, null=True, help_text="5分为最满意，最低分是1分")
    assessment = models.CharField(max_length=250, verbose_name="用户评价", null=True)

    generaluser = models.ForeignKey(GeneralUser, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
