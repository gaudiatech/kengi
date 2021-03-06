import katagames_engine as kengi
from UthModel import StandardCard, PokerHand, MyEvTypes, UthModel


# - aliases
pygame = kengi.pygame
ReceiverObj = kengi.event.EventReceiver
EngineEvTypes = kengi.event.EngineEvTypes

# - program constants
BACKGROUND_IMG_PATH = 'img/bg0.jpg'
CARD_SIZE_PX = (82, 120)
CHIP_SIZE_PX = (62, 62)
POS_CASH = (1192, 1007)
CARD_SLOTS_POS = {  # coords in pixel so cards/chips & BG image do match; cards img need an anchor at the middle.
    'dealer1': (905, 329),
    'dealer2': (1000, 333),

    'flop3': (980, 470),
    'flop2': (1075, 473),
    'flop1': (1173, 471),

    'turn': (846, 473),
    'river': (744, 471),

    'player1': (1125, 878),
    'player2': (1041, 880),

    'ante': (935, 757),
    'bet': (935, 850),
    'blind': (1040, 757),

    'raise1': (955, 870),
    'raise2': (961, 871),
    'raise3': (967, 872),
    'raise4': (973, 873),
    'raise5': (980, 875),
    'raise6': (986, 876)
}
PLAYER_CHIPS = {
    '2a': (825, 1000),
    '2b': (905, 1000),
    '5': (985, 1000),
    '10': (1065, 1000),
    '20': (1145, 1000)
}


class UthView(ReceiverObj):
    TEXTCOLOR = (5, 58, 7)
    BG_TEXTCOLOR = (133, 133, 133)
    ASK_SELECTION_MSG = 'SELECT ONE OPTION: '

    def __init__(self, model):
        super().__init__()
        self._assets_rdy = False

        self.bg = None
        self.card_back_img = None

        self.card_images = dict()
        self.chip_spr = dict()

        self._mod = model
        self.ft = pygame.font.Font(None, 72)
        self.small_ft = pygame.font.Font(None, 23)

        self.info_msg0 = None
        self.info_msg1 = None  # will be used to tell the player what he/she has to do!
        self.info_msg2 = None

        # draw cash amount
        self.cash_etq = self.ft.render(str(self._mod.cash)+'$ ', True, self.TEXTCOLOR, self.BG_TEXTCOLOR)

    def _load_assets(self):
        self._assets_rdy = True

        self.bg = pygame.image.load(BACKGROUND_IMG_PATH)
        self.card_back_img = pygame.image.load('img/back.png').convert_alpha()
        self.card_back_img = pygame.transform.scale(self.card_back_img, CARD_SIZE_PX)

        for card_cod in StandardCard.all_card_codes():
            y = PokerHand.adhoc_mapping(card_cod[0]).lstrip('0') + card_cod[1].upper()  # convert card code to path
            img_path = f'img/{y}.png'
            tempimg = pygame.image.load(img_path).convert_alpha()
            self.card_images[card_cod] = pygame.transform.scale(tempimg, CARD_SIZE_PX)

        for chip_val_info in ('2a', '2b', '5', '10', '20'):
            org = chip_val_info
            if chip_val_info == '2a' or chip_val_info == '2b':
                chip_val_info = '2'
            img_path = f'img/chip{chip_val_info}.png'
            tempimg = pygame.image.load(img_path).convert_alpha()
            tempimg = pygame.transform.scale(tempimg, CHIP_SIZE_PX)
            tempimg.set_colorkey((255, 0, 255))
            spr = pygame.sprite.Sprite()
            spr.image = tempimg
            spr.rect = spr.image.get_rect()
            spr.rect.center = PLAYER_CHIPS[org]
            self.chip_spr[chip_val_info] = spr

    def _update_displayed_status(self):

        if self._mod.stage == UthModel.INIT_ST_CODE:
            self.info_msg0 = self.ft.render('Press ENTER to begin', True, self.TEXTCOLOR)
            self.info_msg1 = None
            self.info_msg2 = None
            return

        msg = None
        if self._mod.stage == UthModel.DISCOV_ST_CODE:
            msg = ' CHECK, BET x3, BET x4'
        elif self._mod.stage == UthModel.FLOP_ST_CODE and (not self._mod.autoplay_flag):
            msg = ' CHECK, BET x2'
        elif self._mod.stage == UthModel.TR_ST_CODE and (not self._mod.autoplay_flag):
            msg = ' FOLD, BET x1'
        if msg:
            self.info_msg0 = self.ft.render(self.ASK_SELECTION_MSG, True, self.TEXTCOLOR)
            self.info_msg1 = self.small_ft.render(msg, True, self.TEXTCOLOR)

    #     message_table = defaultdict(
    #         default_factory=lambda: None, {
    #             UthModel.INIT_ST_CODE: 'press SPACE to play',
    #             UthModel.DISCOV_ST_CODE: 'CHECK, BET x3, BET x4',
    #             UthModel.FLOP_ST_CODE: 'CHECK, BET x2',
    #             UthModel.TR_ST_CODE: 'FOLD, BET x1'
    #         }
    #     )
    #     elif ev.type == MyEvTypes.PlayerWins:
    #     self.delta_money = ev.amount
    #     self.info_msg0 = self.ft.render('Victory', True, self.TEXTCOLOR)
    #
    # elif ev.type == MyEvTypes.PlayerLooses:
    # # TODO disp. amount lost
    # self.info_msg0 = self.ft.render('Defeat', True, self.TEXTCOLOR)

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            if not self._assets_rdy:
                self._load_assets()
            self._paint(ev.screen)

        elif ev.type == MyEvTypes.StageChanges:
            self._update_displayed_status()

        elif ev.type == MyEvTypes.CashChanges:
            # RE-draw cash value
            self.cash_etq = self.ft.render(str(ev.value) + '$ ', True, self.TEXTCOLOR, self.BG_TEXTCOLOR)

        elif ev.type == MyEvTypes.Victory:
            print('victory event received')
            result = ev.amount
            infoh_player = self._mod.player_vhand.description
            infoh_dealer = self._mod.dealer_vhand.description
            msg = f"Player: {infoh_player}; Dealer: {infoh_dealer}; Change {result}$"
            self.info_msg0 = self.ft.render('Victory!', True, self.TEXTCOLOR)
            self.info_msg1 = self.small_ft.render(msg, True, self.TEXTCOLOR)
            self.info_msg2 = self.small_ft.render('Press BACKSPACE to restart', True, self.TEXTCOLOR)

        elif ev.type == MyEvTypes.Tie:
            print('tie event received')
            self.info_msg0 = self.ft.render('Its a Tie.', True, self.TEXTCOLOR)
            infoh_player = self._mod.player_vhand.description
            infoh_dealer = self._mod.dealer_vhand.description
            self.info_msg1 = self.small_ft.render(
                f"Player: {infoh_player}; Dealer: {infoh_dealer}; Change {0}$",
                True, self.TEXTCOLOR
            )
            self.info_msg2 = self.small_ft.render('Press BACKSPACE to restart', True, self.TEXTCOLOR)

        elif ev.type == MyEvTypes.Defeat:
            print('defeat event received')
            if self._mod.folded:
                msg = 'Player folded.'
            else:
                msg = 'Defeat.'
            self.info_msg0 = self.ft.render(msg, True, self.TEXTCOLOR)
            result = ev.loss
            if self._mod.folded:
                self.info_msg1 = self.small_ft.render(f"You've lost {result}$", True, self.TEXTCOLOR)
            else:
                infoh_dealer = self._mod.dealer_vhand.description
                infoh_player = self._mod.player_vhand.description
                self.info_msg1 = self.small_ft.render(
                    f"Player: {infoh_player}; Dealer: {infoh_dealer}; You've lost {result}$", True, self.TEXTCOLOR
                )
            self.info_msg2 = self.small_ft.render('Press BACKSPACE to restart', True, self.TEXTCOLOR)

    @staticmethod
    def centerblit(refscr, surf, p):
        w, h = surf.get_size()
        refscr.blit(surf, (p[0]-w//2, p[1]-h//2))

    def _paint(self, scr):
        scr.blit(self.bg, (0, 0))

        # ---------- draw visible or hidden cards ---------
        if self._mod.stage == UthModel.INIT_ST_CODE:
            # draw hidden cards' back, at adhoc location
            for loc in ('dealer1', 'dealer2', 'player1', 'player2'):
                UthView.centerblit(scr, self.card_back_img, CARD_SLOTS_POS[loc])

        if self._mod.stage >= UthModel.DISCOV_ST_CODE:  # cards revealed
            # draw hidden cards' back, at adhoc location
            for k in range(1, 3+1):
                UthView.centerblit(scr, self.card_back_img, CARD_SLOTS_POS['flop'+str(k)])

            for loc in ('dealer1', 'dealer2'):
                UthView.centerblit(scr, self.card_back_img, CARD_SLOTS_POS[loc])
            for k, c in enumerate(self._mod.player_hand):
                slotname = 'player'+str(k+1)
                UthView.centerblit(scr, self.card_images[c.code], CARD_SLOTS_POS[slotname])

        if self._mod.stage >= UthModel.FLOP_ST_CODE:
            # draw hidden cards' back, at adhoc location
            for loc in ('turn', 'river'):
                UthView.centerblit(scr, self.card_back_img, CARD_SLOTS_POS[loc])
            for k, c in enumerate(self._mod.flop_cards):
                slotname = 'flop'+str(k+1)
                UthView.centerblit(scr, self.card_images[c.code], CARD_SLOTS_POS[slotname])

        if self._mod.stage >= UthModel.TR_ST_CODE:
            UthView.centerblit(scr, self.card_images[self. _mod.turnriver_cards[0].code], CARD_SLOTS_POS['turn'])
            UthView.centerblit(scr, self.card_images[self._mod.turnriver_cards[1].code], CARD_SLOTS_POS['river'])

        if self._mod.revealed['dealer1'] and self._mod.revealed['dealer2']:
            # show what the dealer has
            UthView.centerblit(scr, self.card_images[self._mod.dealer_hand[0].code], CARD_SLOTS_POS['dealer1'])
            UthView.centerblit(scr, self.card_images[self._mod.dealer_hand[1].code], CARD_SLOTS_POS['dealer2'])

        # -- draw amounts for ante, blind and the bet
        for info_e in self._mod.money_info:
            x, name = info_e
            lbl_surf = self.ft.render(f'{x}', True, self.TEXTCOLOR, self.BG_TEXTCOLOR)
            scr.blit(lbl_surf, CARD_SLOTS_POS[name])

        # -- draw chips & the total cash amount
        for k, v in enumerate((2, 5, 10, 20)):
            adhoc_spr = self.chip_spr[str(v)]
            if v == 2:
                adhoc_spr.rect.center = PLAYER_CHIPS['2b']
            scr.blit(adhoc_spr.image, adhoc_spr.rect.topleft)
        self.chip_spr['2'].rect.center = PLAYER_CHIPS['2a']
        scr.blit(self.chip_spr['2'].image, self.chip_spr['2'].rect.topleft)
        scr.blit(self.cash_etq, POS_CASH)

        # -- display all 3 prompt messages
        for rank, e in enumerate((self.info_msg0, self.info_msg1, self.info_msg2)):
            if e is not None:
                scr.blit(e, (24, 10+50*rank))

        kengi.flip()
