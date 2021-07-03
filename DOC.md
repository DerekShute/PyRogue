Combat

    Instead of inheritance, polymorphism.  Monsters and Players support certain properties
    and methods:
        * melee_attack() -> level, strength, damage
        * take_damage
        * ac
        * add_hit_msg
        * add_was_hit_msg
        * add_miss_msg
        * add_was_missed_msg
        * death
        * kill
        * xp_value

    (Which may or may not use Stats behind the scenes and which may or may not make sense for someone).
    
    Player.melee_attack() is responsible for figuring out the weapon in use and the effects of rings and other considerations
    
    Likewise Monster.melee_attack()

Procedural Generation

    Item placement is ruled by two weighted probabilities: First for the type of object (potion, food, etc.) and next 
    the type within that type (potion of strength, etc.)

Actions and Sub-Menus

    The Gameloop processes InputHandlers, which fetch and process input events from the console.  Ultimately the goal is to queue Actions that
    get processed by the Player.perform() method as part of the timer queue dispatch.  It's a nested operation, so an InputHandler.dispatch_events
    may return that InputHandler or some other InputHandler for submenu or queries:
    
    So: Gameloop starts with PlayerInput, which handles the basic commands.  The basic commands go on the player queue as Actions.  There's
    also QuitAction and CancelHandler to signal cases where the player is bailing out of the game.
    
    But if the player does a two-stage command, like "use a thing", PlayerInput returns InventoryInputHandler, where InventoryInputHandler has
    PlayerInput as 'previous'.
    
    InventoryInputHandler does the inventory command ('inventory', 'use', 'drop', 'equip', etc.) and returns the DropAction or UseAction (updated), with
    PlayerInput (previous) as the next-to-run.  It can also bail out of the command by returning self.previous and no action.

    This is kind of a bork of the tcod_tutorial logic, which wraps Gameloop and InputHandler businesses all together and returns one thing that could be an Action
    and could be a state-machine-changing Event and the caller must figure that out with an isinstance().  I don't like that.
   
Map Display / Level

    Same polymorphism for Monsters, Players, and Items.  Support:
        * char -> Tuple[Pos, display-character str, color Tuple[int, int, int]]
        * set_pos
        
    Right now each has a method to add to the level
        * level.add/remove_player
        * level.add/remove_monster
        * level.add/remove_item

    Display has an InputHandler layer (InputHandler.render_layer) for menus and things