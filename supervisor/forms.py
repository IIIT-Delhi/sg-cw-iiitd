from django import forms
from django.utils import timezone

from studentportal.models import Category
from studentportal.models import project_stage as ps
from supervisor.models import News, Comment, TA


class AdvanceSearchForm(forms.Form):
    stage = forms.ChoiceField(choices=(
        (0, 'All'),
        (ps.TO_BE_VERIFIED, 'Awaiting acceptance',),
        (ps.ONGOING, 'Ongoing'),
        (ps.SUBMITTED, 'Submitted'),
        (ps.COMPLETED, 'Completed')),
        label="Stage of project")
    name = forms.CharField(label="Name of student", required=False)
    email = forms.EmailField(label="Email", required=False)
    roll_no = forms.IntegerField(required=False, label="Roll number")
    project_title = forms.CharField(required=False, label="Words in project title")
    NGO_name = forms.CharField(required=False, label="Name of the NGO")
    year_choices = ((x, str(x)) for x in range(2014, timezone.now().year + 1))
    proposal_year = forms.ChoiceField(choices=year_choices,
                                      label="Year of proposal of the project")
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label='All', required=False,
                                      label="Category of the project")


# time_completed_before
# time_completed_after


class NewsForm(forms.ModelForm):
    priority = forms.ChoiceField(choices=(
        (False, "Low"), (True, "High"),),
        help_text="High priority will also send a mail to \
                        all the students who are still doing their projects."
    )

    class Meta:
        model = News
        fields = ['content', 'priority']


class NewCategoryForm(forms.Form):
    name = forms.CharField(label="Name of the category", required=True)
    description = forms.CharField(label="Describe the category", required=False)


class NewNGOForm(forms.Form):
    name = forms.CharField(label="Name of the NGO")
    link = forms.CharField(label="Link for the NGO", required=False)
    details = forms.CharField(label="Something about the NGO", required=False)


class EmailProjectForm(forms.Form):
    to = forms.CharField(label="Student Email", required=True)
    body = forms.CharField(label="Body", widget=forms.Textarea, required=True)


class NewCommentForm(forms.ModelForm):
    text = forms.CharField(label="Comment: ", required=True)

    class Meta:
        model = Comment
        fields = ['text']


class ReportForm(forms.Form):
    date = forms.ChoiceField(label="Projects which were marked as complete within these past months : ",
                             choices=tuple([(x, x) for x in range(1, 13)]))
    semester = forms.ChoiceField(label="Semester:",
                                 choices=((0, "Any"),
                                 (1, "First"), (2, "Second"), (3, "Third"), (4, "Fourth"), (5, "Fifth"), (6, "Sixth"),
                                 (7, "Seventh"), (8, "Eighth"), (9, "Summer Semester 1"),
                                 (10, "Summer Semester 2"), (11, "Summer Semester 3"), (12, "Summer Semester 4")))
    batch = forms.ChoiceField(label="Batch: ",
                             choices=tuple([(0, "Any")] + [(x, x) for x in range(2016, timezone.now().year + 1)]))


class TAForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = TA

    email = forms.CharField(label="IIIT-D Email of the TA", required=True)
