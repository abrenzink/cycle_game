import constants
from game.casting.actor import Actor
from game.shared.point import Point

class Cycle(Actor):
    """A fast motorcycle.

    The responsibility of Cycle is to move itself.

    Attributes:
    ---
        _segments (list): A list of actors that make up each cycle.
        _trailColor (Color): A color object that defines the color of a cycle trail.
        _prepare_body (method): A method that will create the cycle for each instance of Cycle.
    """
    def __init__(self, color):
        """Constructs a new cycle.

        Args:
        ---
            color (Color): The color of the cycle trail.
        """
        super().__init__()
        self._trailColor = color
        self._segments = []
        self._prepare_body()

    def get_segments(self):
        """Gets the segments for each cycle.

        Returns:
        ---
            List: The list of actors for each cycle"""
        return self._segments
        
    def move_next(self):
        """Moves the actor to its next position according to its velocity. Will move each actor
        in _segments beginning from the last segment and ending with the first segment and
        stepping by -1 to iterate through the last backwards."""
        
        # move all segments
        for segment in self._segments:
            segment.move_next()
        # update velocities
        for i in range(len(self._segments) - 1, 0, -1):
            trailing = self._segments[i]
            previous = self._segments[i - 1]
            velocity = previous.get_velocity()
            trailing.set_velocity(velocity)

    def get_head(self):
        """Gets the firs segment of a cycle"""
        return self._segments[0]

    def turn_head(self, velocity):
        """Changes the cycle direction

        Args:
        ---
            velocity (Point): A position to set the cycle position and direction which it will travel in."""
        self._segments[0].set_velocity(velocity)
    
    def _prepare_body(self):
        """Constructs a new cycle with its trail."""

        if self._trailColor == constants.GREEN:
            x = int(constants.MAX_X / 4)
        elif self._trailColor== constants.PINK: 
            x = int((constants.MAX_X / 4) * 3)
        y = int(constants.MAX_Y / 2)

        for i in range(constants.SNAKE_LENGTH):
            position = Point(x - i * constants.CELL_SIZE, y)
            velocity = Point(1 * constants.CELL_SIZE, 0)
            text = "8" if i == 0 else "#"

            color = self._trailColor
            
            segment = Actor()
            segment.set_position(position)
            segment.set_velocity(velocity)
            segment.set_text(text)
            segment.set_color(color)
            self._segments.append(segment)

    def set_trail_color(self, color):
        """Defines the color of the cycle trail."""

        self._trailColor = color

    def grow_trail(self, number_of_segments):
        """Receives the number of trail segments and adds 1 more segment.

        Args:
        ---
            number_of_segments (int): the number of trail segments."""
        for i in range(number_of_segments):
            trail = self._segments[-1]
            velocity = trail.get_velocity()
            offset = velocity.reverse()
            position = trail.get_position().add(offset)
            
            segment = Actor()
            segment.set_position(position)
            segment.set_velocity(velocity)
            segment.set_text("#")
            segment.set_color(self._trailColor)
            self._segments.append(segment)