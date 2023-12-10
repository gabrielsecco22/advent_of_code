import turtle

triangulo = turtle.Turtle()

N = 9

def draw_polygon(n):
    for i in range(n):
        triangulo.forward(100)
        triangulo.left(360 // n)

draw_polygon(N)
triangulo.forward(300)
draw_polygon(N)
