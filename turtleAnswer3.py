import turtle

# Recursive tree drawing function
def draw_tree(branch_length, depth, left_angle, right_angle, reduction_factor):
    if depth == 0:
        return

    turtle.forward(branch_length)
    turtle.left(left_angle)
    draw_tree(branch_length * reduction_factor, depth - 1, left_angle, right_angle, reduction_factor)
    turtle.right(left_angle + right_angle)
    draw_tree(branch_length * reduction_factor, depth - 1, left_angle, right_angle, reduction_factor)
    turtle.left(right_angle)
    turtle.backward(branch_length)

# Get user input
left_angle = float(input("Enter left branch angle (e.g., 20): "))
right_angle = float(input("Enter right branch angle (e.g., 25): "))
start_length = float(input("Enter starting branch length (e.g., 100): "))
reduction_factor = float(input("Enter branch length reduction factor (e.g., 0.7): "))
depth = int(input("Enter recursion depth (e.g., 5): "))

# Setup turtle
turtle.speed("fastest")
turtle.left(90)  # Point upwards
turtle.penup()
turtle.goto(0, -250)
turtle.pendown()

# Draw the tree
draw_tree(start_length, depth, left_angle, right_angle, reduction_factor)

# Keep the window open
turtle.done()
