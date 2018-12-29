import pygame
import pygame.gfxdraw
import imageio
import os
import numpy as np


def draw_letter_at(label, coords):
    centre_pos = np.array([coords[0] - (label.get_width() / 2), coords[1] - (label.get_height() / 2)])
    surface.blit(label, centre_pos)


def draw_distance(person_a, person_b, color):
    perp_direction = np.matmul(rotation_matrix(90), get_direction(person_a, person_b))
    dist_part1 = person_a + perp_direction * 15
    dist_part2 = dist_part1 + perp_direction * 10
    dist_part4 = person_b + perp_direction * 15
    dist_part3 = dist_part4 + perp_direction * 10
    letter_center = to_int_matrix(perp_direction * 15 + dist_part2 + ((dist_part3 - dist_part2) / 2))
    draw_letter_at(label_d_prime, letter_center)
    pygame.draw.lines(surface, color, False,
                      [dist_part1, dist_part2, dist_part3, dist_part4])


def move_guys(person_a, person_b):
    person_a = person_a + a_direction
    b_direction = get_direction(person_a, person_b)
    person_b = person_b + b_direction * speed
    return person_a, person_b, b_direction


def get_direction(person_a, person_b):
    person_diff = person_a - person_b
    b_direction = person_diff / np.linalg.norm(person_diff)
    return b_direction


def rotation_matrix(angle: int):
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    return np.array(((c, -s), (s, c)))


def draw_arrow(person, direction, color):
    arrow_length = 18
    arrow_part_lengths = 5
    arrow_point = person + (direction * arrow_length)
    arrow_part1 = arrow_point + np.matmul(rotation_matrix(140), direction) * arrow_part_lengths
    arrow_part2 = arrow_point + np.matmul(rotation_matrix(-140), direction) * arrow_part_lengths
    pygame.draw.line(surface, color, to_int_matrix(person), to_int_matrix(arrow_point))
    pygame.draw.line(surface, color, to_int_matrix(arrow_point), to_int_matrix(arrow_part1))
    pygame.draw.line(surface, color, to_int_matrix(arrow_point), to_int_matrix(arrow_part2))


def to_int_matrix(mat):
    return mat.round().astype(int)


def draw_people(person_a, person_b, color1, color2):
    person_radius = 6
    person_a = to_int_matrix(person_a)
    person_b = to_int_matrix(person_b)
    pygame.gfxdraw.filled_circle(surface, *person_a, person_radius, color1)
    pygame.gfxdraw.filled_circle(surface, *person_b, person_radius, color2)


def undraw():
    white = (255, 255, 255)
    draw_people(person_a, person_b, white, white)
    draw_arrow(person_a, a_direction, white)
    draw_arrow(person_b, b_direction, white)
    draw_distance(person_a, person_b, (255, 255, 255))


def draw():
    if len(b_positions) > 2:
        pygame.draw.lines(surface, (0, 255, 0), False, b_positions)
        pygame.draw.lines(surface, (255, 0, 0), False, a_positions)
    draw_arrow(person_a, a_direction, (0, 0, 0))
    draw_arrow(person_b, b_direction, (0, 0, 0))
    draw_people(person_a, person_b, (255, 0, 0), (0, 255, 0))
    draw_distance(person_a, person_b, (0, 0, 0))


pygame.init()
clock = pygame.time.Clock()
fps = 60

surface = pygame.display.set_mode((1000, 500))
surface.fill((255, 255, 255))
font = pygame.font.SysFont("dejavuserif", 24)

person_a = np.array([50, 50])
person_b = np.array([50, 450])
speed = 1
a_direction = np.array([1, 0])
b_positions = []
a_positions = []
tick = 0
label_d = font.render("d", True, (0, 0, 0), (255, 255, 255))
label_d_prime = font.render("d'", True, (0, 0, 0), (255, 255, 255))

pygame.draw.line(surface, (0, 0, 0), (25, 50), (25, 450))
pygame.draw.line(surface, (0, 0, 0), (15, 50), (35, 50))
pygame.draw.line(surface, (0, 0, 0), (15, 450), (35, 450))
draw_letter_at(label_d, np.array([40, 250]))

while person_a[0] < 900:
    person_a, person_b, b_direction = move_guys(person_a, person_b)
    b_positions.append(to_int_matrix(person_b))
    a_positions.append(to_int_matrix(person_a))
    draw()
    pygame.display.update()
    pygame.image.save(surface, "gif_{}.png".format(tick))
    tick += 1
    undraw()

pygame.quit()

images = []
for num in range(tick):
    filename = "gif_{}.png".format(num)
    images.append(imageio.imread(filename))
    os.remove(filename)
output_file = 'gif.gif'
imageio.mimsave(output_file, images, duration=(1. / fps))
