import datetime

from django.core import management, mail
from nose.tools import eq_
from test_utils import TestCase

from mock import patch

from remo.profiles.tests import UserFactory
from remo.reports.models import Report
from remo.reports.tests import ReportFactoryWithoutSignals


class FirstNotificationTest(TestCase):
    """Test sending of first notification to Reps to fill reports."""

    def test_send_notification(self):
        """Test sending of first notification to Reps to fill reports."""
        mentor = UserFactory.create(groups=['Mentor'])
        rep = UserFactory.create(groups=['Rep'], userprofile__mentor=mentor)
        ReportFactoryWithoutSignals.create(user=rep)
        management.call_command('send_first_report_notification', [], {})
        eq_(len(mail.outbox), 1)

    @patch('remo.reports.management.commands'
           '.send_third_report_notification.datetime')
    def test_dry_run(self, fake_datetime):
        """Test sending of first notification with debug activated"""
        # act like it's March 2012
        fake_date = datetime.datetime(year=2012, month=3, day=1)
        fake_datetime.today.return_value = fake_date

        management.call_command('send_first_report_notification', dry_run=True)
        eq_(len(mail.outbox), 0)


class SecondNotificationTest(TestCase):
    """Test sending of second notification to Reps to fill reports."""

    def setUp(self):
        """Iniatilize data for the tests."""
        self.mentor = UserFactory.create(groups=['Mentor'])
        self.rep = UserFactory.create(groups=['Rep'],
                                      userprofile__mentor=self.mentor)

    @patch('remo.reports.management.commands'
           '.send_second_report_notification.datetime')
    def test_send_notification_with_reports_filled(self, fake_datetime):
        """Test sending of second notification, with reports filled."""
        # act like it's March 2012
        ReportFactoryWithoutSignals.create(user=self.rep,
                                           month=datetime.date(2012, 2, 1))
        fake_date = datetime.datetime(year=2012, month=3, day=1)
        fake_datetime.today.return_value = fake_date

        management.call_command('send_second_report_notification', [], {})
        eq_(len(mail.outbox), 1)

    @patch('remo.reports.management.commands'
           '.send_second_report_notification.datetime')
    def test_send_notification_without_reports_filled(self, fake_datetime):
        """Test sending of second notification, with missing reports."""
        # act like it's March 2012
        fake_date = datetime.datetime(year=2012, month=3, day=1)
        fake_datetime.today.return_value = fake_date

        # delete existing reports
        Report.objects.all().delete()
        management.call_command('send_second_report_notification', [], {})
        eq_(len(mail.outbox), 2)

    @patch('remo.reports.management.commands'
           '.send_third_report_notification.datetime')
    def test_dry_run(self, fake_datetime):
        """Test sending of second notification with debug activated"""
        # act like it's March 2012
        fake_date = datetime.datetime(year=2012, month=3, day=1)
        fake_datetime.today.return_value = fake_date

        management.call_command('send_second_report_notification', dry_run=True)
        eq_(len(mail.outbox), 0)


class ThirdNotificationTest(TestCase):
    """Test sending of third notification to Reps to fill reports."""
    def setUp(self):
        """Iniatilize data for the tests."""
        self.mentor = UserFactory.create(groups=['Mentor'])
        self.rep = UserFactory.create(groups=['Rep'],
                                      userprofile__mentor=self.mentor)

    @patch('remo.reports.management.commands'
           '.send_third_report_notification.datetime')
    def test_send_notification_with_reports_filled(self, fake_datetime):
        """Test sending of third notification, with reports filled."""
        # act like it's March 2012
        ReportFactoryWithoutSignals.create(user=self.rep,
                                           month=datetime.date(2012, 1, 1))
        fake_date = datetime.datetime(year=2012, month=3, day=1)
        fake_datetime.today.return_value = fake_date

        management.call_command('send_third_report_notification', [], {})
        eq_(len(mail.outbox), 1)

    @patch('remo.reports.management.commands'
           '.send_third_report_notification.datetime')
    def test_send_notification_without_reports_filled(self, fake_datetime):
        """Test sending of third notification, with missing reports."""
        # act like it's March 2012
        fake_date = datetime.datetime(year=2012, month=3, day=1)
        fake_datetime.today.return_value = fake_date

        # delete existing reports
        Report.objects.all().delete()
        management.call_command('send_third_report_notification', [], {})
        eq_(len(mail.outbox), 1)

    @patch('remo.reports.management.commands'
           '.send_third_report_notification.datetime')
    def test_dry_run(self, fake_datetime):
        """Test sending of third notification with debug activated"""
        # act like it's March 2012
        fake_date = datetime.datetime(year=2012, month=3, day=1)
        fake_datetime.today.return_value = fake_date

        management.call_command('send_third_report_notification', dry_run=True)
        eq_(len(mail.outbox), 0)


class MentorNotificationTest(TestCase):
    """Test sending reports to Mentors about unfilled reports."""
    def setUp(self):
        """Iniatilize data for the tests."""
        self.mentor = UserFactory.create(groups=['Mentor'])
        self.rep = UserFactory.create(groups=['Rep'],
                                      userprofile__mentor=self.mentor)

    @patch('remo.reports.management.commands'
           '.send_mentor_report_notification.datetime')
    def test_send_notification_with_reports_filled(self, fake_datetime):
        """Test sending of mentor notification, with reports filled."""
        # act like it's March 2012
        ReportFactoryWithoutSignals.create(user=self.rep,
                                           month=datetime.date(2012, 1, 1))
        ReportFactoryWithoutSignals.create(user=self.rep,
                                           month=datetime.date(2012, 2, 1))
        fake_date = datetime.datetime(year=2012, month=3, day=1)
        fake_datetime.today.return_value = fake_date

        management.call_command('send_mentor_report_notification', [], {})
        eq_(len(mail.outbox), 0)

    @patch('remo.reports.management.commands'
           '.send_mentor_report_notification.datetime')
    def test_send_notification_without_reports_filled(self, fake_datetime):
        """Test sending of mentor notification, with reports missing."""
        # act like it's March 2012
        fake_date = datetime.datetime(year=2012, month=3, day=1)
        fake_datetime.today.return_value = fake_date

        # delete existing reports
        Report.objects.all().delete()
        management.call_command('send_mentor_report_notification', [], {})
        eq_(len(mail.outbox), 1)

    @patch('remo.reports.management.commands'
           '.send_third_report_notification.datetime')
    def test_dry_run(self, fake_datetime):
        """Test sending of mentor notification with debug activated"""
        # act like it's March 2012
        fake_date = datetime.datetime(year=2012, month=3, day=1)
        fake_datetime.today.return_value = fake_date

        management.call_command('send_mentor_report_notification', dry_run=True)
        eq_(len(mail.outbox), 0)

