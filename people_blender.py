# Author: Berin
import click
from PIL import Image, ImageDraw
from pathlib import Path
from random import randrange, choice
from statistics import mean
from tqdm import tqdm

PEOPLE = list(Path('./people-select').iterdir())

def get_person_image(path=None):
    path = path or choice(PEOPLE)
    img = Image.open(path.absolute())
    return img

WIDTH = 1024
HEIGHT = 1024

final_image = Image.new('RGB', (WIDTH, HEIGHT))


def blend_images_in_grid(cell_size=128):
    prev_person = get_person_image()
    for y in tqdm(range(0, HEIGHT, cell_size)):
        for x in range(0, WIDTH, cell_size):
            # x, y are used to pick the cell's upper-left corner position
            person = get_person_image()

            for sx in range(x, x + cell_size):
                for sy in range(y, y + cell_size):
                    r, g, b = person.getpixel((sx, sy))
                    pr, pg, pb = prev_person.getpixel((sx, sy))

                    r, g, b = (r + pr) // 2, (g + pg) // 2, (b + pb) // 2
                    final_image.putpixel((sx, sy), (r, g, b))

            prev_person.close()
            prev_person = person

    person.close()


def merge_faces(start, end, output='out.png'):
    print(f"Merging {end - start} faces...")
    people_set = PEOPLE[start:end]
    total = len(people_set)
    people = [get_person_image(p) for p in people_set]

    for sy in tqdm(range(0, HEIGHT)):
        for sx in range(0, WIDTH):

            all_r = 0
            all_g = 0
            all_b = 0
            for person in people:
                r, g, b = person.getpixel((sx, sy))
                all_r += r
                all_g += g
                all_b += b

            r, g, b = all_r // total, all_g // total, all_b // total
            final_image.putpixel((sx, sy), (r, g, b))

    for p in people:
        p.close()

    final_image.save(output)
    final_image.close()


if __name__ == '__main__':
    offset = 100
    for i, start in enumerate(range(0, len(PEOPLE) - 1, offset)):
        final_image = Image.new('RGB', (WIDTH, HEIGHT))
        out = f'out{i+1:02}.png'
        print(f'Will save image in {out}...')
        merge_faces(start, start + offset, out)
