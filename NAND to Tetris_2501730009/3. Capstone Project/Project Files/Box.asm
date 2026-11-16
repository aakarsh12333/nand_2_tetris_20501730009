// Box for K=9: row 9, 20 rows tall, 2 words (32 px) wide
(LOOP)
    @KBD
    D=M
    @PRESSED
    D;JNE
    @color
    M=0            // no key -> white
    @PAINT
    0;JMP
(PRESSED)
    @color
    M=-1           // key -> black
(PAINT)
    @SCREEN
    D=A
    @288           // 32 * K = 32 * 9
    D=D+A
    @addr
    M=D            // addr = 16672 = start of row 9
    @20
    D=A
    @rows
    M=D            // 20 rows
(ROWLOOP)
    @2             // (K mod 4) + 1 = 2 words
    D=A
    @cols
    M=D
    @addr
    D=M
    @p
    M=D
(COLLOOP)
    @color
    D=M
    @p
    A=M
    M=D
    @p
    M=M+1
    @cols
    M=M-1
    D=M
    @COLLOOP
    D;JGT
    @32
    D=A
    @addr
    M=M+D          // next row = +32 words
    @rows
    M=M-1
    D=M
    @ROWLOOP
    D;JGT
    @LOOP
    0;JMP