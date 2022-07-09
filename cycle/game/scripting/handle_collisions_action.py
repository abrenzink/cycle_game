import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when a cycle collides
    with its segments or the segments of the other cycle, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
        _winner (int): The number of the winner player.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._winner = 0

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)
    
    def _handle_segment_collision(self, cast):
        """Sets the game over flag if one cycle collides with one of the other cycle segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        cycles = cast.get_actors("cycles")
        head1 = cycles[0].get_segments()[0]
        head2 = cycles[1].get_segments()[0]
        trail1 = cycles[0].get_segments()[1:]
        trail2 = cycles[1].get_segments()[1:]
       
        for segment in trail1:
            if head2.get_position().equals(segment.get_position()):
                self._is_game_over = True
                self._winner = 1

        for segment in trail2:
            if head1.get_position().equals(segment.get_position()):
                self._is_game_over = True
                self._winner = 2
        
    def _handle_game_over(self, cast):
        """Shows the 'game over' message, onfroms the winner, and turns both cycles 
        white if the game is over.

        Args:
        ---
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            cycles = cast.get_actors("cycles")
            trails = []

            for cycle in cycles:
                trails.append(cycle.get_segments())
                cycle.set_trail_color(constants.WHITE)

            for segment in trails[0]:
                segment.set_color(constants.WHITE)

            for segment in trails[1]:
                segment.set_color(constants.WHITE) 

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 3)
            position = Point(x, y)

            message = Actor()
            message.set_text(f"Game Over! \n Player {self._winner} wins.")
            message.set_position(position)
            cast.add_actor("messages", message)

            scores = cast.get_actors("scores")

            if self._winner == 1:
                scores[0].add_points(1)
            elif self._winner == 2:
                scores[1].add_points(1)
