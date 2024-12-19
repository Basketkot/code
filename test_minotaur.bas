' Test Suite for Minotaur Game
SUB Main
    CLS
    PRINT "Starting Minotaur Game Test Suite..."
    PRINT "====================================="
    
    TestInitializeGame
    TestMovePlayer
    TestCheckBoundaries
    TestCheckBarriers
    TestThrowSpear
    TestMinotaurCharge
    TestTrapdoor
    
    PRINT "====================================="
    PRINT "Test Suite Complete"
END SUB

SUB TestInitializeGame
    PRINT "Testing Initialize Game..."
    
    DIM player AS PlayerType
    DIM minotaur AS MinotaurType
    DIM barriers(9) AS BarrierType
    
    CALL InitializeGame(player, minotaur, barriers())
    
    ' Test player initialization
    IF player.level >= 1 AND player.level <= 3 THEN
        PRINT "- Player level range: PASS"
    ELSE
        PRINT "- Player level range: FAIL"
    END IF
    
    IF player.x >= -10 AND player.x <= 10 THEN
        PRINT "- Player X position: PASS"
    ELSE
        PRINT "- Player X position: FAIL"
    END IF
    
    IF player.spear = TRUE THEN
        PRINT "- Player spear: PASS"
    ELSE
        PRINT "- Player spear: FAIL"
    END IF
    
    IF UBOUND(barriers) = 9 THEN
        PRINT "- Barrier count: PASS"
    ELSE
        PRINT "- Barrier count: FAIL"
    END IF
END SUB

SUB TestMovePlayer
    PRINT "Testing Player Movement..."
    
    DIM player AS PlayerType
    player.x = 0
    player.y = 0
    player.level = 2
    
    ' Test East movement
    CALL MovePlayer(player, 1)
    IF player.x = 1 AND player.y = 0 THEN
        PRINT "- Move East: PASS"
    ELSE
        PRINT "- Move East: FAIL"
    END IF
    
    ' Reset position
    player.x = 0: player.y = 0
    
    ' Test West movement
    CALL MovePlayer(player, 2)
    IF player.x = -1 AND player.y = 0 THEN
        PRINT "- Move West: PASS"
    ELSE
        PRINT "- Move West: FAIL"
    END IF
    
    ' Test level movement
    player.level = 2
    CALL MovePlayer(player, 5) ' Up
    IF player.level = 3 THEN
        PRINT "- Move Up Level: PASS"
    ELSE
        PRINT "- Move Up Level: FAIL"
    END IF
END SUB

SUB TestCheckBoundaries
    PRINT "Testing Boundary Checks..."
    
    DIM player AS</body>