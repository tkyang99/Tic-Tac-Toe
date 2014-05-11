
from django.conf.urls.defaults import patterns, include, url


from TicTacToe.views import TicTacToeView


urlpatterns = patterns('',
                       
    url(r'^tictactoe/$', TicTacToeView.as_view())
)
