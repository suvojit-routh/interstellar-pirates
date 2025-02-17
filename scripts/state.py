from enum import Enum,auto

class State(Enum):
	START_BGM = auto()
	MENU = auto()
	SHOP = auto()
	EVENT = auto()
	JOURNEY = auto()
	SETTINGS = auto()
	DISPLAY = auto()
	QUIT = auto()
	GACHA = auto()
	GACHA_ROLL = auto()
	GACHA_RESULT = auto()
	MODES = auto()
	CAMPAIGN = auto()
	SELECTION = auto()
	SELECTION_MENU = auto()
	SHIPS_INV = auto()
	UPGRADE_INV = auto()
	EXHAUST = auto()
	THRUSTER = auto()
	CANNON = auto()
	ITEMS_INV = auto()
	ITEMS_INV2 = auto()
	CRAFTING = auto()
	PAUSE = auto()
	TAB_MENU = auto()
	PLANETERY_OPTION = auto()
	PLANETERY_ENTER = auto()
	PLANETERY_LOADING = auto()
	PLANETERY_EXIT = auto()
	LOADING = auto()
	ALIVE = auto()
	DEAD = auto()
	SPACESTATION_ENTER =auto()
	SPACESTATION = auto()
	SPACESTATION_EXIT = auto()
	WARPING = auto()
	LOBBY = auto()

state = State.START_BGM

