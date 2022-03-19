from django.test import SimpleTestCase
from django.urls import reverse, resolve
from profiles.views import ResearcherListApiView, ResearcherDetailApiView
from profiles.views import ParticipantListApiView, ParticipantDetailApiView


class TestParticipantUrls(SimpleTestCase):

    def test_list_participant_urls_is_resolved(self):
        url = reverse('participants')
        self.assertEquals(
            resolve(url).func.__name__, 
            ParticipantListApiView.as_view().__name__
        )
    
    def test_detail_participant_urls_is_resolved(self):
        url = reverse('participant', args=['1'])
        self.assertEquals(
            resolve(url).func.__name__, 
            ParticipantDetailApiView.as_view().__name__
        )
 

class TestResearcherUrls(SimpleTestCase):

    def test_list_researcher_urls_is_resolved(self):
        url = reverse('researchers')
        self.assertEquals(
            resolve(url).func.__name__, 
            ResearcherListApiView.as_view().__name__
        )
    
    def test_detail_researcher_urls_is_resolved(self):
        url = reverse('researcher', args=['1'])
        self.assertEquals(
            resolve(url).func.__name__, 
            ResearcherDetailApiView.as_view().__name__
        )
 