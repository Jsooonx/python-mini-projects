import random
import sys
import pygame

# Basic configs
WIDTH, HEIGHT = 1000, 600
TOP_MARGIN = 80
SIDE_MARGIN = 40
BAR_COUNT = 80
MIN_VALUE = 10
MAX_VALUE = 500
FPS = 60

BACKGROUND = (18, 18, 18)
BAR_COLOR = (220, 220, 220)
ACTIVE_COLOR = (255, 170, 0)
SORTED_COLOR = (0, 200, 120)
TEXT_COLOR = (245, 245, 245)
ACCENT = (90, 170, 255)


class DrawInfo:
    def __init__(self, width, height, values):
        self.width = width
        self.height = height
        self.values = values
        self.min_val = min(values)
        self.max_val = max(values)
        self.block_width = round((width - SIDE_MARGIN * 2) / len(values))
        self.block_height = (height - TOP_MARGIN - 40) / (self.max_val - self.min_val)
        self.start_x = SIDE_MARGIN
        self.font = pygame.font.SysFont("fonts/Inter-Regular.otf", 30)
        self.small_font = pygame.font.SysFont("fonts/Inter-Regular.otf", 22)

    def set_values(self, values):
        self.values = values
        self.min_val = min(values)
        self.max_val = max(values)
        self.block_width = round((self.width - SIDE_MARGIN * 2) / len(values))
        max_range = max(1, self.max_val - self.min_val)
        self.block_height = (self.height - TOP_MARGIN - 40) / max_range


def generate_values(count):
    return [random.randint(MIN_VALUE, MAX_VALUE) for _ in range(count)]


def draw(draw_info, algo_name, ascending, comparisons, swaps, highlight=None, sorted_indices=None):
    screen = pygame.display.get_surface()
    screen.fill(BACKGROUND)

    title = draw_info.font.render(f"Sorting Visualizer - {algo_name}", True, TEXT_COLOR)
    screen.blit(title, (SIDE_MARGIN, 15))

    controls = draw_info.small_font.render(
        "R = reset | SPACE = start/pause | A = ascending | D = descending | B = bubble | I = insertion | ESC = quit",
        True,
        TEXT_COLOR,
    )
    screen.blit(controls, (SIDE_MARGIN, 45))

    stats = draw_info.small_font.render(
        f"Order: {'Ascending' if ascending else 'Descending'}   Comparisons: {comparisons}   Swaps/Shifts: {swaps}",
        True,
        ACCENT,
    )
    screen.blit(stats, (SIDE_MARGIN, 68))

    draw_bars(draw_info, highlight or {}, sorted_indices or set())
    pygame.display.update()


def draw_bars(draw_info, highlight, sorted_indices):
    screen = pygame.display.get_surface()
    values = draw_info.values

    for i, value in enumerate(values):
        x = draw_info.start_x + i * draw_info.block_width
        bar_height = (value - draw_info.min_val) * draw_info.block_height
        y = draw_info.height - bar_height

        color = BAR_COLOR
        if i in sorted_indices:
            color = SORTED_COLOR
        elif i in highlight:
            color = highlight[i]

        pygame.draw.rect(
            screen,
            color,
            (x, y, max(1, draw_info.block_width - 1), bar_height),
        )


def bubble_sort(draw_info, ascending=True):
    values = draw_info.values
    n = len(values)
    comparisons = 0
    swaps = 0

    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            comparisons += 1

            draw(
                draw_info,
                "Bubble Sort",
                ascending,
                comparisons,
                swaps,
                highlight={i: ACTIVE_COLOR, i + 1: ACCENT},
                sorted_indices=set(range(end + 1, n)),
            )
            yield comparisons, swaps

            should_swap = (values[i] > values[i + 1] and ascending) or (
                values[i] < values[i + 1] and not ascending
            )

            if should_swap:
                values[i], values[i + 1] = values[i + 1], values[i]
                swaps += 1
                swapped = True

                draw(
                    draw_info,
                    "Bubble Sort",
                    ascending,
                    comparisons,
                    swaps,
                    highlight={i: ACTIVE_COLOR, i + 1: ACTIVE_COLOR},
                    sorted_indices=set(range(end + 1, n)),
                )
                yield comparisons, swaps

        if not swapped:
            break

    draw(
        draw_info,
        "Bubble Sort",
        ascending,
        comparisons,
        swaps,
        sorted_indices=set(range(n)),
    )
    yield comparisons, swaps


def insertion_sort(draw_info, ascending=True):
    values = draw_info.values
    comparisons = 0
    swaps = 0

    for i in range(1, len(values)):
        current = values[i]
        j = i

        while j > 0:
            comparisons += 1

            should_shift = (values[j - 1] > current and ascending) or (
                values[j - 1] < current and not ascending
            )

            draw(
                draw_info,
                "Insertion Sort",
                ascending,
                comparisons,
                swaps,
                highlight={j: ACTIVE_COLOR, j - 1: ACCENT},
                sorted_indices=set(range(i)) if i > 0 else set(),
            )
            yield comparisons, swaps

            if should_shift:
                values[j] = values[j - 1]
                j -= 1
                swaps += 1
            else:
                break

        values[j] = current

    draw(
        draw_info,
        "Insertion Sort",
        ascending,
        comparisons,
        swaps,
        sorted_indices=set(range(len(values))),
    )
    yield comparisons, swaps


def main():
    pygame.init()
    pygame.display.set_caption("Sorting Visualizer")
    pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    values = generate_values(BAR_COUNT)
    draw_info = DrawInfo(WIDTH, HEIGHT, values)

    sorting = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_name = "Bubble Sort"
    sorting_generator = None
    comparisons = 0
    swaps = 0

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r:
                    values = generate_values(BAR_COUNT)
                    draw_info.set_values(values)
                    sorting = False
                    comparisons = 0
                    swaps = 0

                elif event.key == pygame.K_SPACE:
                    if not sorting:
                        sorting = True
                        sorting_generator = sorting_algorithm(draw_info, ascending)
                    else:
                        sorting = False

                elif event.key == pygame.K_a and not sorting:
                    ascending = True

                elif event.key == pygame.K_d and not sorting:
                    ascending = False

                elif event.key == pygame.K_b and not sorting:
                    sorting_algorithm = bubble_sort
                    sorting_name = "Bubble Sort"

                elif event.key == pygame.K_i and not sorting:
                    sorting_algorithm = insertion_sort
                    sorting_name = "Insertion Sort"

        if sorting and sorting_generator is not None:
            try:
                comparisons, swaps = next(sorting_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_name, ascending, comparisons, swaps)

    pygame.quit()


if __name__ == "__main__":
    main()
