import datetime

from django.utils import timezone
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.urls import reverse
from django.core import mail

from .models import Team, UserPlayer, Point, Trade
from . import views
from .views import PlayersView, place_trade, TradesView
from .forms import UserPlayerForm, TeamForm, PointForm
from django.contrib.auth.models import User
from leagues.models import League
import pdb

class TeamModelTests(TestCase):
    def setUp(self):
        user = User(username='jr.merryman', password='rabble')
        user.save()
        self.user = user
        league = League(name='league', owner=user, created_date=timezone.now(), signup_code="ehh")
        league.save()
        league.participants.add(user)
        league.save()
        self.league = league

    def test_was_created_recently(self):
        time = timezone.now() + datetime.timedelta(days = 30)
        team = Team(created_date=time, id=1, team_owner=self.user, league=self.league)
        team.save()

        self.assertIs(team.was_created_recently(), False)

    def test_team_has_players(self):
        team = Team(created_date=timezone.now(), id=1, team_owner=self.user, league=self.league)
        team.save()
        player = UserPlayer(player_team=team, id=1, league=self.league)
        player.save()

        self.assertIs(team.players_present(), True)

    def test_team_has_no_players(self):
        team = Team(created_date=timezone.now(), id=1, team_owner=self.user, league=self.league)
        team.save()

        self.assertIs(team.players_present(), False)

    def test_filter_points(self):
        team = Team(created_date=timezone.now(), id=1, team_owner=self.user, league=self.league)
        team.save()
        player = UserPlayer(player_team=team, id=1, points_scored=1, league=self.league)
        player.save()

        self.assertIs(team.filter_team_points(), 1)

    def test_get_player_set(self):
        team = Team(created_date=timezone.now(), id=1, team_owner=self.user, league=self.league)
        team.save()
        player = UserPlayer(player_team=team, id=1, league=self.league)
        player.save()

        self.assertEqual(team.get_player_set().count(), 1)
        self.assertEqual(team.get_player_set().first(), player)

class PointModelTests(TestCase):
    def setUp(self):
        user = User(username='jr.merryman', password='rabble')
        user.save()
        self.user = user
        league = League(name='league', owner=user, created_date=timezone.now(), signup_code="ehh")
        league.save()
        league.participants.add(user)
        league.save()
        self.league = league
        team = Team(created_date=timezone.now(), id=1, team_owner=self.user, league=self.league)
        player = UserPlayer(player_team=team, id=1, league=self.league)
        self.team = team
        self.player = player

    def test_str(self):
        new_point = Point(player=self.player, point=1, note='meow', point_owner=self.user, team=self.team)
        new_point.save()

        self.assertEqual(str(new_point), '1')

class TradeModelTests(TestCase):
    
    def setUp(self):
        #first user
        first_user = User.objects.create(username='jab')
        first_user.set_password('1234')
        first_user.email = 'test_email@gmail.com'
        first_user.save()

        #second user
        second_user = User.objects.create(username='jabroni')
        second_user.set_password('1234')
        second_user.email = 'test_email2@gmail.com'
        second_user.save()
        
        #set up league
        league = League(name='league', owner=first_user, created_date=timezone.now(), signup_code="ehh")
        league.save()
        league.participants.add(first_user)
        league.participants.add(second_user)
        league.save()
        self.league = league
        
        #first team with players
        first_team = Team(team_name='jabs', team_owner_id=first_user.id, created_date=timezone.now(), league=self.league)
        first_team.save()
        first_player = UserPlayer(player_team=first_team, player_first_name='joe', player_last_name='momma', league=league)
        first_player.save()

        #second team with players
        second_team = Team(team_name='jabronis', team_owner_id=second_user.id, created_date=timezone.now(), league=self.league)
        second_team.save()
        second_player = UserPlayer(player_team=second_team, player_first_name='joseph', player_last_name='momma', league=league)
        second_player.save()

        #make the trade sucka!
        new_trade = Trade(proposing_team=first_team,
                          receiving_team=second_team,
                          created_date=timezone.now())
        new_trade.save()
        new_trade.proposing_team_players.add(first_player)
        new_trade.receiving_team_players.add(second_player)
        new_trade.save()
        self.trade = new_trade

    def test_update_outcome_accept(self):
        self.trade.update_outcome('accept')

        self.assertEqual(self.trade.outcome, "Accepted")
        self.assertIs(self.trade.is_completed, True)

    def test_update_outcome_decline(self):
        self.trade.update_outcome('decline')
        
        self.assertEqual(self.trade.outcome, "Declined")
        self.assertIs(self.trade.is_completed, True)

class CloudRoniViewsTests(TestCase):
    
    def setUp(self):
        user = User.objects.create(username='jab')
        user.set_password('1234')
        user.email = 'test_email@gmail.com'
        user.save()
        self.new_user = user
        self.login_user()
        self.team_index = self.client.get('/cloud_roni/')
        league = League(name='league', owner=user, created_date=timezone.now(), signup_code="ehh")
        league.save()
        league.participants.add(user)
        league.save()
        self.league = league

    def login_user(self):
        self.client.login(username='jab',password='1234')

    def set_up_team_with_players(self, is_second_team_needed = False):
        team = Team(team_name='jabs', team_owner_id=1, created_date=timezone.now(), league=self.league)
        team.save()
        self.team = team
        player = UserPlayer(player_team=team, player_first_name='joe', player_last_name='momma', league=self.league)
        player.save()
        self.player = player
        
        if(is_second_team_needed):
            user = User.objects.create(username='jabroni')
            user.set_password('1234')
            user.email = 'test_email2@gmail.com'
            user.save()
            self.second_user = user
            second_team = Team(team_name='jabronis', team_owner_id=user.id, created_date=timezone.now(), league=self.league)
            second_team.save()
            self.second_team = second_team
            player = UserPlayer(player_team=second_team, player_first_name='joseph', player_last_name='momma', league=self.league)
            player.save()
            self.second_player = player

    def create_players_in_db(self):
        num_arr = ["1","2","3","4"]
        
        for nums in num_arr:
            player = UserPlayer(player_first_name='joe', player_last_name='momma' + nums, player_team=self.team, league=self.league)
            player.save()

    def test_place_trade_loads(self):
        self.set_up_team_with_players(True)
        load_page = self.client.get('/cloud_roni/' + str(self.second_user.id) + '/trade/')

        self.assertIn('Propose Trade', load_page.content)

    def test_submit_place_trade(self):
        self.set_up_team_with_players(True)
        data = {'requesting_team_ids[]': self.player.id,
                'receiving_team_ids[]': self.second_player.id
                }
        response = self.client.post('/cloud_roni/' + str(self.second_user.id) + '/trade/', data)

        self.assertEqual(Trade.objects.count(), 1)
        self.assertIn(self.player, Trade.objects.last().proposing_team_players.all())
        self.assertIn(self.second_player, Trade.objects.last().receiving_team_players.all())

    def test_trade_index_view_loads(self):
        self.login_user()
        self.set_up_team_with_players()

        request = RequestFactory().get('/trades')
        request.user = self.new_user
        view = TradesView.as_view()
        response = view(request)

        self.assertIn("My Trades", response.rendered_content)

    def test_trade_completed_accepted(self):
        self.login_user()
        self.set_up_team_with_players(True)

        #creates a trade
        new_trade = Trade(proposing_team=self.team,
                          receiving_team=self.second_team,
                          created_date=timezone.now())
        new_trade.save()
        new_trade.proposing_team_players.add(self.player)
        new_trade.receiving_team_players.add(self.second_player)
        new_trade.save()

        data = {'trade_id': new_trade.id,
                'outcome': 'accept'}

        response = self.client.post('/cloud_roni/complete_trade/', data)

        self.assertIn("Accepted", response.content)

    def test_trade_completed_declined(self):
        self.login_user()
        self.set_up_team_with_players(True)

        #creates a trade
        new_trade = Trade(proposing_team=self.team,
                          receiving_team=self.second_team,
                          created_date=timezone.now())
        new_trade.save()
        new_trade.proposing_team_players.add(self.player)
        new_trade.receiving_team_players.add(self.second_player)
        new_trade.save()

        data = {'trade_id': new_trade.id,
                'outcome': 'decline'}

        response = self.client.post('/cloud_roni/complete_trade/', data)

        self.assertIn("Declined", response.content)

    def test_search_players_with_valid_search(self):
        name_to_search = "joe"
        request = RequestFactory().get('/cloud_roni/players')
        team = Team(team_name='jabs', team_owner_id=1, created_date=timezone.now(), league=self.league)
        team.save()
        self.team = team
        view = PlayersView.as_view()
        self.create_players_in_db()
        request.user = self.new_user
        response = view(request, q=name_to_search)

        self.assertEqual(response.context_data['players_list'].count(), 4)

    def test_search_players_invalid_search(self):
        name_to_search = "joseph"
        request = RequestFactory().get('/cloud_roni/players')
        view = PlayersView.as_view()
        request.user = self.new_user
        response = view(request, q=name_to_search)

        self.assertEqual(response.context_data['players_list'].count(), 0)
    
    def test_root_url_resolves_to_teams(self):
        found = resolve('/cloud_roni/')

        self.assertEqual(found.url_name, 'index')

    def test_teams_page_has_correct_info_with_no_teams(self):
        content = self.team_index.content

        self.assertIn('These are not the teams you are looking for...', content)

    def test_teams_page_has_correct_info_with_teams(self):
        Team(team_name='jabs', team_owner_id=1, created_date=timezone.now(), league=self.league).save()
        reload_home_page = self.client.get('/cloud_roni/')

        self.assertIn('<a href="/cloud_roni/1/team/">1. jabs</a>', reload_home_page.content)

    def test_teams_page(self):
        team = Team(team_name='jabs', team_owner_id=1, created_date=timezone.now(), league=self.league)
        team.save()
        UserPlayer(player_team=team, player_first_name='joe', player_last_name='momma', league=self.league).save()
        team_page_request = self.client.get("/cloud_roni/" + str(team.id) + "/team/")

        self.assertIn('joe momma', team_page_request.content)

    def test_detailed_player_view(self):
        self.set_up_team_with_players()
        player_page_request = self.client.get("/cloud_roni/" + str(self.player.player_team.id) + "/players/" + str(self.player.id) + "/")

        self.assertIn('joe momma', player_page_request.content)


    def test_add_point_view_with_error(self):
        self.set_up_team_with_players()
        response = self.client.post("/cloud_roni/" + str(self.player.id) + "/add_point/", {'player_id': self.player.id})

        self.assertTrue('Note is required' in response.content)

    def test_add_point_view_without_error(self):
        point_count = Point.objects.count()
        self.set_up_team_with_players()
        response = self.client.post("/cloud_roni/" + str(self.player.id) + "/add_point/", {'note': "I am a note", 'point': Point.ONE})

        self.assertEqual(Point.objects.count(), point_count + 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_create_player_view(self):
        self.set_up_team_with_players()
        player_count = UserPlayer.objects.count()
        self.team.league.drafted = True
        self.team.league.save()
        response = self.client.post('/cloud_roni/' + str(self.team.id) + '/create_player/',
            {
                'usage': UserPlayer.HEAVY_USE,
                'player_first_name': 'Jarrod',
                'player_last_name': 'Marryweather',
            })

        self.assertEqual(UserPlayer.objects.count(), player_count + 1)
        self.assertRedirects(response, expected_url=reverse('cloud_roni:team', args=(self.team.id,)))

    def test_create_player_view_with_error(self):
        self.set_up_team_with_players()
        self.team.league.drafted = True
        self.team.league.save()
        response = self.client.post('/cloud_roni/' + str(self.team.id) + '/create_player/')

        self.assertTrue('Form is invalid!' in response.content)

    def test_create_player_view_without_league_draft(self):
        self.set_up_team_with_players()
        response = self.client.post('/cloud_roni/' + str(self.team.id) + '/create_player/')

        self.assertTrue('Your league has not drafted yet!' in response.content)

    def test_create_team_view(self):
        response = self.client.post('/cloud_roni/create_team/', {'team_name': 'Jabrones', 'team_owner': str(self.new_user.id)})

        self.assertEqual(Team.objects.count(), 1)
        self.assertRedirects(response, expected_url=reverse('cloud_roni:index'))

    def test_create_team_view_with_error(self):
        response = self.client.post('/cloud_roni/create_team/')

        self.assertTrue('Invalid Information!' in response.content)

    def test_update_player_view(self):
        self.login_user()
        self.set_up_team_with_players()
        response = self.client.get('/cloud_roni/' + str(self.player.id) + '/update_player/')

        self.assertTrue('joe' in response.content)
        self.assertTrue('momma' in response.content)
        self.assertTrue('Not Using' in response.content)

    def test_delete_player_view(self):
        self.set_up_team_with_players()
        player_count = UserPlayer.objects.count()
        response = self.client.post('/cloud_roni/' + str(self.player.id) + '/delete_player/')

        self.assertEqual(UserPlayer.objects.count(), player_count - 1)
        self.assertRedirects(response, expected_url=reverse('cloud_roni:team', args=(self.team.id,)))

class PointFormTests(TestCase):

    def setUp(self):
        user = User.objects.create(username='jab')
        user.set_password('1234')
        user.save()
        self.new_user = user
        self.login_user()
        self.team_index = self.client.get('/cloud_roni/')
        league = League(name='league', owner=user, created_date=timezone.now(), signup_code="ehh")
        league.save()
        league.participants.add(user)
        league.save()
        self.league = league

    def login_user(self):
        self.client.login(username='jab',password='1234')

    def set_up_team_with_players(self):
        team = Team(team_name='jabs', team_owner_id=1, created_date=timezone.now(), league=self.league)
        team.save()
        self.team = team
        player = UserPlayer(player_team=team, player_first_name='joe', player_last_name='momma', league=self.league)
        player.save()
        self.player = player

    def test_add_point_form(self):
        self.set_up_team_with_players()
        self.login_user()
        form = PointForm({
            'point': Point.ONE,
            'note': 'Hey, I am a note',
        })

        self.assertTrue(form.is_valid())

        submitted_point = form.save(commit=False)
        submitted_point.player = self.player
        submitted_point.point_owner = self.new_user
        submitted_point.save()

        self.assertEqual(submitted_point.player, self.player)
        self.assertEqual(submitted_point.point, Point.ONE)
        self.assertEqual(submitted_point.note, "Hey, I am a note")
        self.assertEqual(submitted_point.point_owner, self.new_user)