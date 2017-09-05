from __future__ import unicode_literals

import datetime
import json
import unittest

import django
from django.core.urlresolvers import reverse, NoReverseMatch
from model_mommy import mommy

from data_research.views import validate_year_month
from data_research.models import (
    CountyMortgageData,
    MSAMortgageData,
    NationalMortgageData,
    StateMortgageData)


class YearMonthValidatorTests(unittest.TestCase):
    """check the year_month validator"""
    good_pair = '2016-09'
    future_year = '2040-08'
    too_old_year = '1957-08'
    bad_month = '2015-13'
    non_integer = '201A-12'
    bad_format = '201609'

    def test_validate_year_month_good(self):
        self.assertTrue(validate_year_month(self.good_pair))

    def test_validate_year_month_future_year(self):
        self.assertFalse(validate_year_month(self.future_year))

    def test_validate_year_month_too_old(self):
        self.assertFalse(validate_year_month(self.too_old_year))

    def test_validate_year_month_bad_month(self):
        self.assertFalse(validate_year_month(self.bad_month))

    def test_validate_year_month_non_integer(self):
        self.assertFalse(validate_year_month(self.non_integer))

    def test_validate_year_month_bad_format(self):
        self.assertFalse(validate_year_month(self.bad_format))


class TimeseriesViewTests(django.test.TestCase):

    fixtures = ['mortgage_constants.json', 'mortgage_metadata.json']

    def setUp(self):
        mommy.make(
            NationalMortgageData,
            current=2500819,
            date=datetime.date(2008, 1, 1),
            fips=00000,
            id=1,
            ninety=40692,
            other=36196,
            sixty=27586,
            thirty=67668,
            total=2674899)

        mommy.make(
            StateMortgageData,
            current=250081,
            date=datetime.date(2008, 1, 1),
            fips='12',
            valid=True,
            id=1,
            ninety=4069,
            other=3619,
            sixty=2758,
            thirty=6766,
            total=26748)

        mommy.make(
            MSAMortgageData,
            current=5250,
            date=datetime.date(2008, 1, 1),
            fips='35840',
            valid=True,
            id=1,
            ninety=1406,
            other=361,
            sixty=1275,
            thirty=3676,
            total=22674)

        mommy.make(
            CountyMortgageData,
            current=250,
            date=datetime.date(2008, 1, 1),
            valid=True,
            fips='12081',
            id=1,
            ninety=406,
            other=361,
            sixty=275,
            thirty=676,
            total=2674)

    def test_metadata_request(self):
        response = self.client.get(
            reverse(
                'data_research_api_metadata',
                kwargs={'meta_name': 'sampling_dates'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            '2008-01-01',
            json.loads(response.content)
        )

    def test_metadata_request_bad_meta_name(self):
        response = self.client.get(
            reverse(
                'data_research_api_metadata',
                kwargs={'meta_name': 'xxx'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('No metadata object found.', response.content)

    def test_national_timeseries_30_89(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries_national',
                kwargs={'days_late': '30-89'}))
        self.assertEqual(response.status_code, 200)

    def test_national_timeseries_90(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries_national',
                kwargs={'days_late': '90'}))
        self.assertEqual(response.status_code, 200)

    def test_state_timeseries_30_89(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '12',
                        'days_late': '30-89'}))
        self.assertEqual(response.status_code, 200)

    def test_state_timeseries_90(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '12',
                        'days_late': '90'}))
        self.assertEqual(response.status_code, 200)

    def test_msa_timeseries_30_89(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '35840',
                        'days_late': '30-89'}))
        self.assertEqual(response.status_code, 200)

    def test_msa_timeseries_90(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '35840',
                        'days_late': '90'}))
        self.assertEqual(response.status_code, 200)

    def test_county_timeseries_30_89(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '12081',
                        'days_late': '30-89'}))
        self.assertEqual(response.status_code, 200)

    def test_county_timeseries_90(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '12081',
                        'days_late': '90'}))
        self.assertEqual(response.status_code, 200)

    def test_timeseries_bad_fips(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '99999',
                        'days_late': '90'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('FIPS code not found.', response.content)

    def test_map_data_bad_date(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'counties',
                        'days_late': '90',
                        'year_month': '0000-01'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid year-month pair', response.content)

    def test_map_data_disallowed_delinquency_digit(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'counties',
                        'days_late': '100',
                        'year_month': '2008-01'}))

    def test_map_data_disallowed_delinquency_range(self):
        response = self.client.get(reverse(
            'data_research_api_mortgage_mapdata',
            kwargs={'geo': 'counties',
                    'days_late': '38-89',
                    'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Unknown delinquency range', response.content)

    def test_timeseries_disallowed_delinquency_range(self):
        response = self.client.get(reverse(
            'data_research_api_mortgage_timeseries',
            kwargs={'fips': '12081', 'days_late': '38-89'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Unknown delinquency range', response.content)

    def test_national_timeseries_disallowed_delinquency_range(self):
        response = self.client.get(reverse(
            'data_research_api_mortgage_timeseries_national',
            kwargs={'days_late': '38-89'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Unknown delinquency range', response.content)

    def test_map_data_unknown_geo(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'parish',
                        'days_late': '90',
                        'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Unkown geographic unit', response.content)

    def test_county_map_data_30_89(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'counties',
                        'days_late': '30-89',
                        'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(
            sorted(response_data.get('data').get('12081').keys()),
            ['date', 'name', 'value'])

    def test_county_map_data_90(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'counties',
                        'days_late': '90',
                        'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(
            sorted(response_data.get('data').get('12081').keys()),
            ['date', 'name', 'value'])

    def test_msa_map_data_30_89(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'metros',
                        'days_late': '30-89',
                        'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)

    def test_msa_map_data_90(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'metros',
                        'days_late': '90',
                        'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)

    def test_state_map_data_30_89(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'states',
                        'days_late': '30-89',
                        'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)

    def test_state_map_data_90(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'states',
                        'days_late': '90',
                        'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)

    def test_national_map_data_30_89(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'national',
                        'days_late': '30-89',
                        'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)

    def test_national_map_data_90(self):
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_mapdata',
                kwargs={'geo': 'national',
                        'days_late': '90',
                        'year_month': '2008-01'}))
        self.assertEqual(response.status_code, 200)

    def test_county_timeseries_data_invalid(self):
        for county in CountyMortgageData.objects.all():
            county.valid = False
            county.save()
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '12081', 'days_late': '90'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('County is below display threshold', response.content)

    def test_msa_timeseries_data_invalid(self):
        for msa in MSAMortgageData.objects.all():
            msa.valid = False
            msa.save(aggregate=False)
        response = self.client.get(
            reverse(
                'data_research_api_mortgage_timeseries',
                kwargs={'fips': '35840', 'days_late': '90'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Metro area is below display threshold', response.content)