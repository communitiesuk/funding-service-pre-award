from flask_babel import gettext
from wtforms import RadioField, StringField, TextAreaField
from wtforms.validators import Email, InputRequired

from pre_award.apply.forms.base import ApplicationFlaskForm, PrepopulatedForm


class DefaultSectionFeedbackForm(ApplicationFlaskForm):
    experience = RadioField()
    more_detail = TextAreaField()

    def __init__(self, *args, **kwargs):
        super(DefaultSectionFeedbackForm, self).__init__(*args, **kwargs)
        self.experience.label.text = gettext("How easy did you find it to complete this section?")
        self.experience.choices = [
            ("very easy", gettext("Very easy")),
            ("easy", gettext("Easy")),
            (
                "neither easy or difficult",
                gettext("Neither easy nor difficult"),
            ),
            ("difficult", gettext("Difficult")),
            ("very difficult", gettext("Very difficult")),
        ]
        self.more_detail.label.text = gettext("Explain why you chose this score (optional)")
        self.experience.validators = [InputRequired(message=gettext("Select a score"))]

    @property
    def as_dict(self):
        return {
            "application_id": self.application_id.data,
            "experience": self.experience.data,
            "more_detail": self.more_detail.data,
        }


class EndOfApplicationPage1Form(PrepopulatedForm):
    overall_application_experience = RadioField()

    def __init__(self, *args, **kwargs):
        super(EndOfApplicationPage1Form, self).__init__(*args, **kwargs)
        self.overall_application_experience.label.text = gettext(
            "How was your overall experience of using this service?"
        )
        self.overall_application_experience.choices = [
            ("very good", gettext("Very good")),
            ("good", gettext("Good")),
            ("average", gettext("Average")),
            ("poor", gettext("Poor")),
            ("very poor", gettext("Very poor")),
        ]
        self.overall_application_experience.validators = [InputRequired(message=gettext("Select a score"))]


class EndOfApplicationPage2Form(PrepopulatedForm):
    service_improvement = TextAreaField()

    def __init__(self, *args, **kwargs):
        super(EndOfApplicationPage2Form, self).__init__(*args, **kwargs)
        self.service_improvement.label.text = gettext("How could we improve this service?")


class EndOfApplicationPage3Form(PrepopulatedForm):
    time_spent = RadioField()

    def __init__(self, *args, **kwargs):
        super(EndOfApplicationPage3Form, self).__init__(*args, **kwargs)
        self.time_spent.label.text = gettext(
            "On average, how much time did you and your team spend completing the form (including collating and "
            "providing information)?"
        )
        self.time_spent.choices = [
            ("up_to_3_hours", gettext("Up to 3 hours")),
            ("4_to_6_hours", gettext("4 to 6 hours")),
            ("7_to_9_hours", gettext("7 to 9 hours")),
            ("10_to_12_hours", gettext("10 to 12 hours")),
            ("more_than_12_hours", gettext("More than 12 hours")),
        ]
        self.time_spent.validators = [InputRequired(message=gettext("Select an option"))]


class EndOfApplicationPage4Form(PrepopulatedForm):
    research_participation = RadioField()
    research_email = StringField()
    research_organisation = StringField()

    def __init__(self, *args, **kwargs):
        super(EndOfApplicationPage4Form, self).__init__(*args, **kwargs)
        self.research_participation.label.text = gettext(
            "Would you like to participate in our research to help improve the service?"
        )
        self.research_participation.choices = [
            ("yes", gettext("Yes")),
            ("no", gettext("No")),
        ]
        self.research_participation.validators = [InputRequired(message=gettext("Select an option"))]
        self.research_email.label.text = gettext("What is your email address?")
        self.research_organisation.label.text = gettext("What organisation do you work for?")

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        valid = True

        if self.research_participation.data == "yes":
            if not self.research_email.data:
                self.research_email.errors.append(gettext("Enter your email address"))
                valid = False
            else:
                try:
                    Email()(None, self.research_email)
                except Exception:
                    self.research_email.errors.append(gettext("Enter a valid email address"))
                    valid = False

            if not self.research_organisation.data:
                self.research_organisation.errors.append(gettext("Enter your organisation name"))
                valid = False

        return valid


END_OF_APPLICATION_FEEDBACK_SURVEY_PAGE_NUMBER_MAP = {
    "1": (
        EndOfApplicationPage1Form,
        "apply/end_of_application_feedback_page_1.html",
    ),
    "2": (
        EndOfApplicationPage2Form,
        "apply/end_of_application_feedback_page_2.html",
    ),
    "3": (
        EndOfApplicationPage3Form,
        "apply/end_of_application_feedback_page_3.html",
    ),
    "4": (
        EndOfApplicationPage4Form,
        "apply/end_of_application_feedback_page_4.html",
    ),
}
