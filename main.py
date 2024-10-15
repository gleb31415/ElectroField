import tkinter as tk
import math

root = tk.Tk()

screen_width, screen_height = 800, 800
canvas = tk.Canvas(root, width=screen_width, height=screen_height, background='black')

particles = []  # pos [x, y], sign
nl = 10  # number of power lines
k = 5000  # constant for Kulon's law


def add_pos_particle(event):
    global particles
    mouse_pos = event.x, event.y
    particles.append([mouse_pos, 1])
    canvas.create_oval(mouse_pos[0] - 10, mouse_pos[1] - 10, mouse_pos[0] + 10, mouse_pos[1] + 10, fill='red', tags='base')
    canvas.delete('lines')
    for i in range(len(particles) - 1):
        for j in range(i + 1, len(particles)):
            if int(math.dist(particles[i][0], particles[j][0])) < 10:
                particles.pop(j)
    main()


def add_neg_particle(event):
    global particles
    mouse_pos = event.x, event.y
    particles.append([mouse_pos, -1])
    canvas.create_oval(mouse_pos[0] - 10, mouse_pos[1] - 10, mouse_pos[0] + 10, mouse_pos[1] + 10, fill='blue', tags='base')
    canvas.delete('lines')
    for i in range(len(particles) - 1):
        for j in range(i + 1, len(particles)):
            if int(math.dist(particles[i][0], particles[j][0])) < 10:
                particles.pop(j)

    main()


def move(point):
    hs, vs = 0, 0
    for particle in particles:
        dx, dy = point[0] - particle[0][0], point[1] - particle[0][1]
        r = math.hypot(dx, dy) or 0.0001
        module = k * particle[1] / r ** 2
        hs += module * dx
        vs += module * dy
    return [hs, vs]


def sign(a):
    if a < 0:
        return -1
    return 1

def draw_traject(point, charge):
    path = []
    global particles
    mxst = 2000
    stz = 2
    for _ in range(mxst):
        dx, dy = move(point)
        if math.hypot(dx, dy) == 0:
            break
        dx, dy = dx * stz/math.hypot(dx, dy),  dy * stz/math.hypot(dx, dy)
        point[0] += dx * sign(charge)
        point[1] += dy * sign(charge)
        path.append((point[0], point[1]))

        if not (0 < point[0] < screen_width and 0 < point[1] < screen_height or
                any(math.hypot(point[0] - prt[0][0], point[1] - prt[0][1]) < 20 for prt in particles)):
             break

    if len(path) > 1:
        canvas.create_line([coord for p in path for coord in p], fill="yellow", tags="lines")
        canvas.tag_raise("base")


def main():
    global particles
    shiftangle = 2 * math.pi / nl
    for particle in particles:
        for _ in range(nl):
            px, py = int(particle[0][0] + math.cos(shiftangle * (_ + 1)) * 10), int(particle[0][1] + math.sin(shiftangle * (_ + 1)) * 10)
            draw_traject([px, py], particle[1])


canvas.bind('<Button-1>', add_pos_particle)
canvas.bind('<Button-2>', add_neg_particle)
canvas.pack()
root.mainloop()