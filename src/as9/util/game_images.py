from as9.util.needle_img import NeedleImg

img_back_button = NeedleImg('back-button')
img_chat_close = NeedleImg('chat-close')
img_chat_open = NeedleImg('chat-open')
img_close_button = NeedleImg('close-button')
img_daily_events = NeedleImg('daily-events', threshold=0.7)
img_exit_game = NeedleImg('exit-game')
img_free_button = NeedleImg('free-button')
img_free_pack = NeedleImg('free-pack', threshold=0.9)
img_gray_next_button = NeedleImg('grey-next-button')
# High threshold because we don't want to click when it's already highlighted white.
img_legend_pass = NeedleImg('legend-pass', threshold=0.95)
img_next_button = NeedleImg('next-button')
img_open_free_pack = NeedleImg('open-free-pack')
# Low because the required tickets changes.
img_play0_button = NeedleImg('play0-button', threshold=0.7)
# Play a multiplayer race.
img_play_button = NeedleImg('play-button')
# Start an MP race.
img_play_race = NeedleImg('play-race-button')
img_race_button = NeedleImg('race-button')
img_refill_tickets = NeedleImg('refill-tickets')
img_skip_button = NeedleImg('skip-button')
img_td_off = NeedleImg('td-off')
img_td_on = NeedleImg('td-on')
img_legend_showcase = NeedleImg('legend-showcase')
img_snapdragon1 = NeedleImg('snapdragon1')
# Be certain since this spends resources.
img_ticket_free_refill = NeedleImg('ticket-free-refill', threshold=0.9)
img_ready_to_claim = NeedleImg('ready-to-claim')
img_quit_race = NeedleImg('quit-race')
