import constants

from game.casting.cast import Cast
from game.casting.score import Score
from game.casting.cycle import Cycle
from game.scripting.script import Script
from game.scripting.control_first_cycle_action import ControlFirstCycleAction
from game.scripting.control_second_cycle_action import ControlSecondCycleAction
from game.scripting.move_actors_action import MoveActorsAction
from game.scripting.handle_collisions_action import HandleCollisionsAction
from game.scripting.draw_actors_action import DrawActorsAction
from game.directing.director import Director
from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService
from game.shared.point import Point


def main():
    
    # create the cast
    cast = Cast()
    cycle1 = Cycle(constants.GREEN)
    cycle2 = Cycle(constants.PINK)
    cast.add_actor("cycles", cycle1)
    cast.add_actor("cycles", cycle2)

    score1 = Score(1)
    score2 = Score(2)
    score1.set_position(Point(constants.MAX_X - 850, 0))
    score2.set_position(Point(constants.MAX_X - 200, 0))
    cast.add_actor("scores", score1)
    cast.add_actor("scores", score2)
   
    # start the game
    keyboard_service = KeyboardService()
    video_service = VideoService()

    script = Script()
    script.add_action("input", ControlFirstCycleAction(keyboard_service))
    script.add_action("input", ControlSecondCycleAction(keyboard_service))
    script.add_action("update", MoveActorsAction())
    script.add_action("update", HandleCollisionsAction())
    script.add_action("output", DrawActorsAction(video_service))
    
    director = Director(video_service)
    director.start_game(cast, script)


if __name__ == "__main__":
    main()