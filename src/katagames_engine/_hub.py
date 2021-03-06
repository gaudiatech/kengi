"""
Keep this file separate from __init__.py!
its important, bc all sub-modules in kengi may import _hub
in order to refer to other dependencies/sub-modules
"""
from .Injector import Injector


kengi_inj = Injector({
    'ai': '._sm_shelf.ai',

    'gfx': '._sm_shelf.gfx',
    'ascii': '._sm_shelf.ascii',
    'demolib': '._sm_shelf.demolib',
    'polarbear': '._sm_shelf.polarbear',
    'console': '._sm_shelf.console',
    'core': '._sm_shelf.core',
    'gui': '._sm_shelf.gui',
    'isometric': '._sm_shelf.isometric',
    'legacy': '._sm_shelf.legacy',
    'tabletop': '._sm_shelf.tabletop',

    # nota bene: pygame is dynamically added to this dict,
    # its done elsewhere
    'tmx': '._sm_shelf.tmx',

    'rogue': '._sm_shelf.rogue',
    'terrain': '._sm_shelf.terrain',
})


def __getattr__(targ_sm_name):
    if targ_sm_name in kengi_inj:
        return kengi_inj[targ_sm_name]
    else:
        raise AttributeError(f"kengi has no attribute named {targ_sm_name}")
