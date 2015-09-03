# -YGSIAC-
You Got Stuck In A Cave
# This is the game project so far 

# DONE:
   * splash screen, title screen, game state machine working well
   * map loading and parsing is a bit messy, but does what it needs to (may implement something better in future)
   * entities base class set up, with common functionality inherited to all children.
   * items base class started, can "interact" with player, it's one of those should work in theory situations, been only slightyly         tested, so it probably needs some adjustment.
   * enemies base class started, some simple AI is being tested. Currently the enemy detects when player is in range, tracks players
     position, following and shooting at the player if they are close enough. Enemies will also flee if their health drops below a       certain point. The collision detection is set up, though collision response still needs implemented.   
   * a few test levels have been made up, though none of the that's set in stone.
   * a utilities module is made up with various scripts that help out around the house from time to time, good people, real good         people. 
   * geometrics.py was written to handle all the vector math involved with the " 'line of sight', 'field of view', and 'pathfinding'    type of things. theres also a quadtree implementation taken from rouguebasin, which should help with collision detection.
    
