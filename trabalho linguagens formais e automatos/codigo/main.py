import re

# -----------------------------
# Lexer
# -----------------------------
TOKEN_REGEX = r"\s*(?:(\d+)|(.))"

def lexer(code):
    tokens = []
    for number, other in re.findall(TOKEN_REGEX, code):
        if number:
            tokens.append(("NUM", int(number)))
        elif other in "+-*/()":
            tokens.append((other, other))
        else:
            raise SyntaxError(f"Caractere inválido: {other}")
    tokens.append(("EOF", None))
    return tokens

# -----------------------------
# Parser (GLC -> AST)
# -----------------------------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos][0]

    def eat(self, token_type):
        if self.peek() == token_type:
            val = self.tokens[self.pos][1]
            self.pos += 1
            return val
        raise SyntaxError(f"Esperado {token_type}")

    def factor(self):
        if self.peek() == "NUM":
            return ("NUM", self.eat("NUM"))
        if self.peek() == "(":
            self.eat("(")
            node = self.expr()
            self.eat(")")
            return node
        raise SyntaxError("Erro no fator")

    def term(self):
        node = self.factor()
        while self.peek() in ("*", "/"):
            op = self.eat(self.peek())
            node = ("BINOP", op, node, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.peek() in ("+", "-"):
            op = self.eat(self.peek())
            node = ("BINOP", op, node, self.term())
        return node

# -----------------------------
# Interpretador
# -----------------------------
def evaluate(node):
    if node[0] == "NUM":
        return node[1]
    _, op, left, right = node
    a = evaluate(left)
    b = evaluate(right)
    return {
        "+": a + b,
        "-": a - b,
        "*": a * b,
        "/": a / b
    }[op]

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    code = input("Digite uma expressão: ")
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.expr()
    print("AST:", ast)
    print("Resultado:", evaluate(ast))
