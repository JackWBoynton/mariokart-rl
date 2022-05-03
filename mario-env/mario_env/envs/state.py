import enum
import queue
import numpy as np

@enum.unique
class PlayerType(enum.Enum):
    Human      = 0
    CPU        = 1
    Demo       = 2
    Unselected = 3

@enum.unique
class Character(enum.Enum):
    # hex(90128747)
    Mario = 0
    BabyPeach = 1
    Waluigi = 2
    Bowser = 3
    BabyDaisy = 4
    DryBones = 5
    BabyMario = 6
    Luigi = 7
    Toad = 8
    DonkeyKong = 9
    Yoshi = 10
    Wario = 11
    BabyLuigi = 12
    Toadette = 13
    KoopaTroopa = 14
    Daisy = 15
    Peach = 16
    Birdo = 17
    DiddyKong = 18
    KingBoo = 19
    BowserJr = 20
    DryBowser = 21
    FunkyKong = 22
    Rosalina = 23
    SmallMiiOutfitAM = 24
    SmallMiiOutfitAF = 25
    SmallMiiOutfitBM = 26
    SmallMiiOutfitBF = 27
    SmallMiiOutfitCM = 28
    SmallMiiOutfitCF = 29
    MediumMiiOutfitAM = 30
    MediumMiiOutfitAF = 31
    MediumMiiOutfitBM = 32
    MediumMiiOutfitBF = 33
    MediumMiiOutfitCM = 34
    MediumMiiOutfitCF = 35
    LargeMiiOutfitAM = 36
    LargeMiiOutfitAF = 37
    LargeMiiOutfitBM = 38
    LargeMiiOutfitBF = 39
    LargeMiiOutfitCM = 40
    LargeMiiOutfitCF = 41
    MediumMii = 42
    SmallMii = 43
    LargeMii = 44
    PeachBikerOutfit = 45
    DaisyBikerOutfit = 46
    RosalinaBikerOutfit = 47
    

@enum.unique
class Track(enum.Enum):
    LuigiCircuit = 0
    MooMooMeadows = 1
    MushroomGorge = 2
    ToadsFactory = 3
    MarioCircuit = 4
    CoconutMall = 5
    DKSummitDKSnowboardCross = 6
    WariosGoldMine = 7
    DaisyCircuit = 8
    KoopaCape = 9
    MapleTreeway = 10
    GrumbleVolcano = 11
    DryDryRuins = 12
    MoonviewHighway = 13
    BowsersCastle = 14
    RainbowRoad = 15
    GCNPeachBeach = 16
    DSYoshiFalls = 17
    SNESGhostValley2 = 18
    N64MarioRaceway = 19
    N64SherbetLand = 20
    GBAShyGuyBeach = 21
    DSDelfinoSquare = 22
    GCNWaluigiStadium = 23
    DSDesertHills = 24
    GBABowserCastle3 = 25
    N64DKsJungleParkway = 26
    GCNMarioCircuit = 27
    SNESMarioCircuit3 = 28
    DSPeachGardens = 29
    GCNDKMountain = 30
    N64BowsersCastle = 31
    BlockPlaza = 32
    DelfinoPier = 33
    FunkyStadium = 34
    ChainChompWheelChainChompRoulette = 35
    ThwompDesert = 36
    SNESBattleCourse4 = 37
    GBABattleCourse3 = 38
    N64Skyscraper = 39
    GCNCookieLand = 40
    DSTwilightHouse = 41
    Winningscene = 42
    Losingscene = 43

@enum.unique
class Menu(enum.Enum):
    Characters = 0
    Stages     = 1
    Game       = 2
    PostGame   = 4

@enum.unique
class Vehicles(enum.Enum):
    StandardKartS = 0
    StandardKartM = 1
    StandardKartL = 2
    BoosterSeat = 3
    ClassicDragster = 4
    Offroader = 5
    MiniBeast = 6
    WildWing = 7
    FlameFlyer = 8
    CheepCharger = 9
    SuperBlooper = 10
    PiranhaProwler = 11
    TinyTitan = 12
    Daytripper = 13
    Jetsetter = 14
    BlueFalcon = 15
    Sprinter = 16
    Honeycoupe = 17
    StandardBikeS = 18
    StandardBikeM = 19
    StandardBikeL = 20
    BulletBike = 21
    MachBike = 22
    FlameRunner = 23
    BitBike = 24
    Sugarscoot = 25
    WarioBike = 26
    Quacker = 27
    ZipZip = 28
    ShootingStar = 29
    Magikruiser = 30
    Sneakster = 31
    Spear = 32
    JetBubble = 33
    DolphinDasher = 34
    Phantom = 35

@enum.unique
class Items(enum.Enum):
    GreenShell = 0
    RedShell = 1
    Banana = 2
    FakeItemBox = 3
    Mushroom = 4
    TripleMushroom = 5
    Bobomb = 6
    BlueShell = 7
    Lightning = 8
    Star = 9
    GoldenMushroom = 10
    MegaMushroom = 11
    Blooper = 12
    POWBlock = 13
    ThunderCloud = 14
    BulletBill = 15
    TripleGreenShell = 16
    TripleRedShell = 17
    TripleBanana = 18
    UnusedBlank = 19
    UsedforNoItem = 20

@enum.unique
class ScreenID(enum.Enum):
    Emptyitseems = 0x00
    ESRBnotice = 0x01
    sixtyHzsuggestion = 0x02
    Datacorrupt = 0x03
    Cantsave = 0x04
    Systemmemorycorrupt = 0x05
    MiiDatacorrupt = 0x06
    GrandPrixPanOverlay = 0x07
    VSPanOverlay = 0x08
    BattlePanOverlay = 0x09
    MissionPanOverlay = 0x0A
    TournamentPanOverlay = 0x0B
    GrandPrixInterface = 0x0C
    TimeTrialInterface = 0x0D
    onePVSRaceInterface = 0x0E
    twoPVSRaceInterface = 0x0F
    threePVSRaceInterface = 0x10
    fourPVSRaceInterface = 0x11
    onePBattleInterface = 0x12
    twoPBattleInterface = 0x13
    threePBattleInterface = 0x14
    fourPBattleInterface = 0x15
    MissionandTournamentInterface = 0x16
    GrandPrixPauseMenu = 0x17
    VSRacePauseMenu = 0x18
    TimeTrialPauseMenu = 0x19
    BattlePauseMenu = 0x1A
    TournamentPauseMenu = 0x1B
    GhostRacePauseMenu = 0x1C
    AbandonGhostRace = 0x1D
    QuitGhostRace = 0x1E
    GhostReplayPauseMenu = 0x1F
    GrandPrixEndScreenNextRaceWatchReplayQuit = 0x20
    TimeTrialEndScreenRetryChangeCourseetc = 0x21
    VSRaceEndScreenNextRaceQuit = 0x22
    BattleEndScreenNextBattleQuit = 0x23
    BattleEndScreenNextonlytofinalresults = 0x24
    MissionEndScreenRetryChooseMissionQuitUnused = 0x25
    TournamentEndScreen = 0x26
    GhostRaceEndScreenNextQuit = 0x27
    GotoFriendRoster = 0x28
    YoubeatyourfriendsrecordSendyourghost = 0x29
    Sendtourneyrecord = 0x2A
    Checkrankings = 0x2B
    Areyousureyouwanttoquit = 0x2C
    SplitsafterTT = 0x2D
    LeaderboardafterTT = 0x2E
    GPVSscoreupdatescreen = 0x2F
    GPVSscoreoverallscreen = 0x30
    Onlineracepointupdatescreen = 0x31
    TeamVSpointoverallscreen = 0x32
    Battlepointupdatescreen = 0x33
    Battlepointoverallscreen = 0x34
    Competitionpersonalleaderboard = 0x35
    GrandPrixreplayinterface = 0x36
    GhostRaceinterface = 0x37
    GrandPrixreplaypause = 0x38
    TTImmediateReplaypause = 0x39
    SupportingpanelPresentinmanymodesinrace2ndelement = 0x3A
    Probablyawardinterfaceuntested = 0x3B
    Probablycongratsscreenuntested = 0x3C
    CreditsVSinterfaceuntested = 0x3D
    Creditslatterinterfaceuntested = 0x3E
    Congratsaftercredits = 0x3F
    WiFiRaceInterface = 0x40
    twoPWiFiRaceInterface = 0x41
    WiFiFriendRoomRaceInterface = 0x42
    WiFiFriendRoomTeamRaceInterface = 0x43
    Congratuationsatendoffriendroomuntested = 0x44
    DummySeemstoimmediatelyload0x46 = 0x45
    OnlineRaceEndNextRaceQuitFriendRoster = 0x46
    Quitonlinerace = 0x47
    EndofonlineracePleasewaittext = 0x48
    LiveVSviewinterface = 0x49
    LiveBattleviewinterfaceuntested = 0x4A
    Startgameokay = 0x4B
    Textboxwithspinner = 0x4C
    DriftExplanationMessageBox = 0x4D
    VoteRandomMessageBox = 0x4E
    Readingghostdatascreenwithtextspinner = 0x4F
    ConnectingtoNintendoWFC = 0x50
    GenerictextboxfullscreenpressA = 0x51
    TextboxwithonepromptMultipleuses = 0x52
    PostphototoWiiMessageBoard = 0x53
    Behindmainmenu = 0x54
    DummyMaybenotlowbatteryGoesto5A = 0x55
    Lowbatterynotification = 0x56
    TitleScreen = 0x57
    OpeningMovie = 0x59
    MainMenu = 0x5A
    Behindunlocks = 0x5B
    Flagbackground = 0x5C
    BehindDisconnectsOptions = 0x5D
    Topmenuoverlay = 0x5E
    BlinkingpressA = 0x5F
    SelectMii = 0x60
    Activecontrollerdisplay = 0x61
    Playercontrolleroptin = 0x62
    PairWiiRemotes = 0x63
    PlayercontrolleroptincompleteOKChange = 0x64
    LicenseSelect = 0x65
    MiiChanged = 0x66
    LicenseSettings = 0x67
    EraseLicense = 0x68
    SinglePlayerMenu = 0x69
    GrandPrixClassSelect = 0x6A
    CharacterSelect = 0x6B
    VehicleSelect = 0x6C
    DriftSelect = 0x6D
    CupSelect = 0x6E
    CourseSelectsubscreen = 0x6F
    SelectGhosta = 0x70
    SelectGhostb = 0x71
    SelectSoloTeamVS = 0x72
    SelectRaceRules = 0x73
    TeamsOverview = 0x74
    SelectBattleMode = 0x75
    SelectVehicleBattle = 0x76
    SelectBattleRules = 0x77
    SelectBattleCup = 0x78
    SelectBattleCourse = 0x79
    MissionLevelSelectUnused = 0x7A
    MissionSelectsubscreen = 0x7B
    MissionInformationPrompt = 0x7C
    DriftSelectwithoneoption = 0x7D
    MissionTutorial = 0x7E
    Presentonsingleplayermenus = 0x7F
    MultiplayerMenuVSBT = 0x80
    MultiplayerVehicleSelect = 0x81
    MultiplayerDriftSelect = 0x82
    MultiplayerTeamSelect = 0x83
    partofconnecting = 0x84
    WFCfirstplay = 0x85
    Allowdatatobesent = 0x86
    Disconnectsyou = 0x87
    Seemstodrawbehindonlineracespanel2 = 0x88
    ErrorconnectingtoWFC = 0x89
    DummySeemstoredirectto0x52 = 0x8A
    WFCMenu = 0x8B
    WFCVSBattleSelect = 0x8C
    FriendsMenu = 0x8D
    FriendsMenuMarioKartChannel = 0x8E
    GlobalSearchManagerdoesntrender = 0x8F
    Timer = 0x90
    PlayerListVRScreen = 0x91
    CourseStageVotes = 0x92
    Presentinliveview = 0x93
    Presentinonlinerace = 0x94
    Presentinonlinemenus = 0x95
    FriendRoster = 0x96
    NotFriendsYet = 0x97
    RemoveFriendCode = 0x98
    RemovingFriendCode = 0x99
    SeemstopreparetheFriendslist = 0x9A
    FriendRoomwaitingtext = 0x9B
    FriendRoomManagerdoesntrender = 0x9C
    FriendRoom = 0x9D
    FriendRoomMessages = 0x9E
    MarioKartChannel = 0xA2
    RankingsMenu = 0xA3
    ChannelGhostsScreen = 0xA4
    DummyLoads0xA6 = 0xA5
    EnterFC = 0xA6
    GhostListManagerdoesntrender = 0xA7
    MarioKartChannelghosthistogramscreen = 0xA8
    MarioKartChannelbehind0xAD = 0xAC
    MarioKartChannelwithaselectedghostchallengewatch = 0xAD
    Residesbehind0x4Floads0xB4 = 0xB3
    MarioKartChannelDownloadedGhostList = 0xB4
    MarioKartChannelEraseGhost = 0xB5
    CompetitionforWiiWheelsonly = 0xBA
    Options = 0xC0
    NintendoWiFiConnectionoptions = 0xC1
    InformationboxwithNextcanchaintoself = 0xC2
    Informationboxwith2buttonsprompt = 0xC3
    Informationboxwith3prompts = 0xC4
    Returntosystemmenutosetregion = 0xC5
    FlagRegionDisplay = 0xC6
    Largeinfoboxwithspinner = 0xC7
    LargeinfoboxwithAprompt = 0xC8
    InfoboxwithOKprompt = 0xC9
    AddMarioKartChannel = 0xCA
    AddMarioKartChannelprompt = 0xCB
    DrawsbeneathOptionsmenu = 0xCC
    OverallRecords = 0xCE
    Favourites = 0xCF
    FriendRecords = 0xD0
    WFCRecords = 0xD1
    OtherRecords = 0xD2
    LOADING = None

OUT_NP_STATE_NAMES = ["minutes", "seconds", "thirdseconds", "xpos", "ypos", "zpos", "prev_xpos", "prev_ypos", "prev_zpos", "current_lap", "max_lap", "item", "steer", "acceleration", "state_flags", "max_lap_completion", "current_lap_completion"]

OUT_NP_STATE_NAMES_MAP = {y: x for x, y in enumerate(OUT_NP_STATE_NAMES)}

@dataclass
class State:
    """Databag that is handled by StateManager."""
    def __init__(self):

        [setattr(self, x, -1) for x in OUT_NP_STATE_NAMES]

    def asnumpy(self):
        x = [getattr(self, y) for y in OUT_NP_STATE_NAMES]
        out = np.nan_to_num(np.asarray(x).astype(np.float32), nan=0.0)
        assert out.shape[0] == 17, f"{v}, {x}, {out}"
        return out

    def __str__(self):
        return str(vars(self))


@enum.unique
class CoarseState(enum.Enum):
    pass



