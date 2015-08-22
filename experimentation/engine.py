# Created by a human
# when:
#8/22/2015
#6:26 AM
#
#
#--------------------------------------------------------------------
import pygame
import sys

class Engine(object):
    #a generic state mach
    def __init__(self):
        self.current_state = State()
        self.states = []

    def run(self):
        self.states = [self.current_state]

        while self.states:
            self.current_state = self.states.pop()
            if self.current_state.paused:
                self.current_state.unpause()

            next, paused = self.current_state.mainloop()
            if self.current_state.kill_prev and self.states:
                self.states.pop()

            if paused:  #paused states are kept
                self.states.append(self.current_state)

            if next:
                self.states.append(next)

#generic parent class for a state
class State(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.clock = pygame.time.Clock()
        self.paused = False
        self.kill_prev = False
        self.screen = pygame.display.get_surface()

    def reinit(self):
        pass

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False
        self.done = False
        self.next = None

    def main_start(self):
        pass

    def mainloop(self):
        self.main_start()
        while not self.done:
            self.check_events()
            self.check_collisions()
            self.update_screen()
            self.tick()
            pygame.event.pump()
        return self.next, self.paused

    def check_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.quit()

    def check_collisions(self):
        pass

    def update_screen(self):
        pass

    def tick(self):
        self.clock.tick(30)

    def quit(self):
        self.done = True
        self.screen.fill((0,0,0))
        return self.next, self.paused

    def close_game(self):
        sys.exit(0)


# ------------------------------------------------------------
# subclassing Engine() to use as an AI state machine
# -----------------------------------------------------------
class NPC(Engine):
    def __init__(self):
        Engine.__init__(self)
        self.current_state = NPCState()
        self.states = []


# entity state object to be used with AI engine
class NPCState(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.clock = pygame.time.Clock()
        self.paused = False
        self.kill_prev = False

    def reinit(self):
        pass

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False
        self.done = False
        self.next = None

    def main_start(self):
        pass

    def main_loop(self):
        self.main_start()
        while not self.done:
            self.check_surroundings()
            self.update()
            self.tick()
        return self.next, self.paused

    def check_surroundings(self):
        pass

    def update(self):
        pass

    def tick(self):
        self.clock.tick(30)

    def quit(self):
        self.done = True
        return self.next, self.paused
