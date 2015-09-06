# -YGSIAC-
You Got Stuck In A Cave

# This is the game project so far

# DONE:
 I suppose I should put some information up about how to actually play the demo.
 currently requires pygame 1.9.1, and python 2.7.
 why not python 3?
 cause i'm livin' in the stoneage like a caveman, back off!
 space bar selects title menu options, which are navigated with the arrow keys, options does nothing. then once you've started the game W,A,S,D to walk. shoot and aim with the mouse, reload with R


   * splash screen, title screen, game state machine working well
   * map loading and parsing is a bit messy, but does what it needs to (may implement something better in future)
   * entities base class set up, with common functionality inherited to all children.
   * items base class started, can "interact" with player, it's one of those should work in theory situations, been only slightly         tested, so it probably needs some adjustment.
   * enemies base class started, some simple AI is being tested. Currently the enemy detects when player is in range, tracks players
     position, following and shooting at the player if they are close enough. Enemies will also flee if their health drops below a       certain point. The collision detection is set up, though collision response still needs implemented.   
   * a few test levels have been made up, though none of the that's set in stone.
   * a utilities module is made up with various scripts that help out around the house from time to time, good people, real good         people.
   * geometrics.py was written to handle all the vector math involved with the 'line of sight', 'field of view', and 'pathfinding'    type of things. there's also a quadtree implementation taken from roguebasin, which should help with collision detection.
