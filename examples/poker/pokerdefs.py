import katagames_engine as kengi


DEBUG = False
MAXFPS = 45

# always try to keep your event number low: model->view or model->ctrl comms only
MyEvTypes = kengi.event.enum_ev_types(
    'CashChanges',  # contains int "value"
    'StageChanges',
    'EndRoundRequested',
    'Victory',  # contains: amount
    'Tie',
    'Defeat'  # contains: loss
)
