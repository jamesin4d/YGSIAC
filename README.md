# YGSIAC-


This is the game project so far 
img -
    - contains all the images used, and then some, still working on the artwork
maps - 
    - contains the .json files for the test levels made up so far
source -
    
    
    
    - contains the .py source files
    --Modules:
    init.py
    badguys.py
      --functions: 
        sortenemydata - takes location (x,y), id_key, and image data
        sortbytype - probably redundant, takes the return from sortenemydata and 
                        makes an instance of an Enemy()
      --classes:
      TurretBullet()
        - non working bullet prototype sprite
      Turret()
        - non working turret prototype
      Walker()
        - the only functional enemy in the game so far
      
    engine.py
      --classes:
      Engine()
        - a finite state machine
      State()
        - state parent class
    
    entities.py--contains the same sort methods as badguys.py
    this is more a module to contain inanimate objects
    
    entityKing.py
    ALL HAIL THE MASTER
    game_states.py
    --classes:
    Logo()
    --splash screen state
    StartScreen()
    --start menu, it's not made clear yet, but press space over
      the selection you want, <quit> and <start> both work
    Game() 
    -- the main game controller
    Gameover()
    -- you have been killed to death screen
    RealitySimulator()
    -- now just close your eyes...
    
    main_game.py
    -- initializes the display/caption
    -- initializes the Engine()
    
    mapper.py
    --classes:
      Mapper()
      (the parser formally known as Parapa)
      handles the parsing of .json data 
      creating all game 'objects'
    
    player.py
    --classes:
    player()
    
    utilities.py
    this module is mostly used as a "testing grounds" currently
    though a few of the functions there are used.
    
    
