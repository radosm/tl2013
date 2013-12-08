from bcTokens import lexer
import test

def testCallback(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print tok

test.run(testCallback)
