from as9.util.screen_img import ScreenImg

img_back_button = ScreenImg('back-button')
img_chat_close = ScreenImg('chat-close')
img_chat_open = ScreenImg('chat-open')
img_close_button = ScreenImg('close-button')
img_daily_events = ScreenImg('daily-events', threshold=0.7)
img_exit_game = ScreenImg('exit-game')
img_free_button = ScreenImg('free-button')
img_free_pack = ScreenImg('free-pack', threshold=0.9)
img_gray_next_button = ScreenImg('grey-next-button')
# High threshold because we don't want to click when it's already highlighted white.
img_legend_pass = ScreenImg('legend-pass', threshold=0.95)
img_next_button = ScreenImg('next-button')
img_open_free_pack = ScreenImg('open-free-pack')
# Low because the required tickets changes.
img_play0_button = ScreenImg('play0-button', threshold=0.7)
img_play_button = ScreenImg('play-button')
img_race_button = ScreenImg('race-button')
img_refill_tickets = ScreenImg('refill-tickets')
img_skip_button = ScreenImg('skip-button')
img_td_off = ScreenImg('td-off')
img_td_on = ScreenImg('td-on')
