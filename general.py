import pygame
import random
import math
import time
import tracemalloc #? to track memory usage

pygame.init() # needed to run the pygame library

class draw_info:
    black = 0, 0, 0
    white = 255, 255, 255
    red = 255, 0, 0
    green = 0, 255, 0
    blue = 0, 0, 255
    yellow = 255, 255, 0
    purple = 128, 0, 128
    brown = 165, 42, 42
    bg_color = white

    # we need differing colors to enhance visibility
    gradients = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    font = pygame.font.SysFont('comicsans', 20) # displaying instructions onto screen
    large_font = pygame.font.SysFont('comicsans', 30) # for large text
    side_pad = 100 # total padding on the sides of the window
    top_pad = 150 # total padding on the top and bottom of window to show controls

    def __init__(self, width, height, lst) -> None:
        # screen width and height
        self.width = width 
        self.height = height
        
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Sorting Algorithm Visualizer')
        self.set_list(lst)
        
    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.side_pad) / len(lst))
        self.block_height_scale = math.floor((self.height - self.top_pad) / (self.max_val - self.min_val)) # accounting for the range of values present
        self.draw_x = self.side_pad // 2 # x-coordinate of the drawer

# important to clear the screen after each animation - it's the convention. Gets rid of overlays
def refill(draw_info, algo_name, ascending):
    # initially a white window
    draw_info.window.fill(draw_info.bg_color)

    title = draw_info.large_font.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.blue)  # title of the window, Ascending if ascending, else Descending
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width() / 2, 5))

    # for controls
    controls = draw_info.font.render('R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending', 1, draw_info.black) # instructions for user
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width() / 2, 40))

    # for sorting algorithm choice
    in_place = draw_info.font.render('I - Insertion Sort | B - Bubble Sort | S - Selection Sort', 1, draw_info.black)
    draw_info.window.blit(in_place, (draw_info.width/2 - in_place.get_width() / 2, 65))

    # for divide-and-conquer
    divide_n_conquer = draw_info.font.render('M - Merge Sort | Q - Quick Sort', 1, draw_info.black)
    draw_info.window.blit(divide_n_conquer, (draw_info.width/2 - divide_n_conquer.get_width() / 2, 90))

    # extra algorithms - I know, I'm a genius
    extra_algs = draw_info.font.render(
        'X - Radix Sort | H - Shell Sort | P - Heap Sort', 1, draw_info.black)
    draw_info.window.blit(
        extra_algs, (draw_info.width/2 - extra_algs.get_width() / 2, 115))

    draw_list(draw_info)
    pygame.display.update()

# drawing each and every bar

# dictionary for accessing colors
def draw_list(draw_info, color_positions={}, clear_bg=False, lst=None):
    if lst == None:
        lst = draw_info.lst

    if clear_bg: # inefficient to re-render controls on screen; only redraw the list after every pass...
        clear_rect = (draw_info.side_pad//2, draw_info.top_pad, draw_info.width - draw_info.side_pad, draw_info.height - draw_info.top_pad)
        pygame.draw.rect(draw_info.window, draw_info.bg_color, clear_rect) # actually drawing it

    for i, val in enumerate(lst): # returns tuples for each item in the form (index, value)
        x = draw_info.draw_x + i * draw_info.block_width # x co-ord for each item; changes according to its index
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height_scale # we needed the offset because, by convention, rectangles are drawn from their top-left edge

        # we subtracted the min_val to account for negative values within the list

        color = draw_info.gradients[i % 3] # alternating between the 3 shades of gray

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height)) # rect object: Rect(left, top, width, height)

    if clear_bg:
        pygame.display.update() # render the drawing of white rectangle

# starting list
def generate_starting_lst(n, min_val, max_val):
    lst = []
    for _ in range(n):
        lst.append(random.randint(min_val, max_val))
    return lst

# bubble sort
def bubble_sort(draw_info, ascending=True, lst=None): # by default, we sort in ascending order
    if lst == None:
        lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst) - 1 - i): # not considering the last item, since in every pass, the last item is always in place

            if (lst[j] > lst[j+1] and ascending) or (lst[j] < lst[j+1] and ascending == False):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.green, j+1 : draw_info.red}, True) # green and red used to show which bars are being compared
                yield True # returns generator object, used to draw each step. Can stop function at any time and resume - pause functionality

    return lst


# insertion sort
def insertion_sort(draw_info, ascending=True, lst=None):
    if lst == None:
        lst = draw_info.lst

    n = len(lst)
    for i in range(1, n):
        current_value = lst[i]
        free_index = i

        while free_index > 0 and ((lst[free_index - 1] > current_value and ascending) or (lst[free_index - 1] < current_value and not ascending)):
            lst[free_index] = lst[free_index - 1]
            free_index -= 1
            cp = {x: draw_info.blue for x in range(i)}
            cp[i] = draw_info.red
            cp[free_index] = draw_info.green
            draw_list(draw_info, cp, clear_bg=True)
            yield True

        lst[free_index] = current_value

    return lst

# selection sort
def selection_sort(draw_info, ascending=True, lst=None):
    if lst == None:
        lst = draw_info.lst

    n = len(lst)
    for i in range(n):
        min_index = i

        for j in range(i+1, n):
            if (lst[j] < lst[min_index] and ascending) or (lst[j] > lst[min_index] and ascending == False):
                min_index = j

        lst[i], lst[min_index] = lst[min_index], lst[i]
        draw_list(draw_info, {i:draw_info.red, min_index:draw_info.green}, True)
        yield True
    return lst

# merge sort here:
def merge_sort(draw_info, ascending=True, lst=None):
    if lst == None:
        lst = draw_info.lst
    yield from merge_sort_helper(draw_info, lst, 0, len(lst)-1, ascending)

def merge_sort_helper(draw_info, lst, start, end, ascending):
    if start < end:
        mid = (start + end) // 2
        yield from merge_sort_helper(draw_info, lst, start, mid, ascending)
        yield from merge_sort_helper(draw_info, lst, mid+1, end, ascending)
        yield from merge(draw_info, lst, start, mid, end, ascending)
    yield lst

def merge(draw_info, lst, start, mid, end, ascending):
    left = lst[start:mid+1]
    right = lst[mid+1:end+1]
    i, j, k = 0, 0, start
    while i < len(left) and j < len(right):
        if (left[i] <= right[j] and ascending) or (left[i] > right[j] and not ascending):
            lst[k] = left[i]
            i += 1
        else:
            lst[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        lst[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        lst[k] = right[j]
        j += 1
        k += 1
    color_positions = {x: draw_info.green for x in range(start, end)}
    color_positions[end] = draw_info.red
    yield draw_list(draw_info, color_positions, True, lst)

# quick sort
def quick_sort(draw_info, ascending=True, lst=None):
    if lst==None:
        lst = draw_info.lst
    yield from quick_sort_helper(draw_info, lst, 0, len(lst)-1, ascending) # recursive algorithm, so we need a helper function

def partition(draw_info, lst, low, high,ascending):
    pivot = lst[high]
    i = low - 1

    # basic quicksort alg here:
    for j in range(low, high):
        if (lst[j] <= pivot and ascending) or (lst[j] > pivot and not ascending):
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
        color_positions = {
            # which sub-list are we looking at?
            x: draw_info.blue for x in range(low, high+1)
        }
        color_positions[i] = draw_info.green
        color_positions[j] = draw_info.red
        draw_list(draw_info, color_positions, True, lst)
        time.sleep(0.15)

    lst[i+1], lst[high] = lst[high], lst[i+1]
    time.sleep(0.5)
    return i+1

def quick_sort_helper(draw_info, lst, low, high, ascending):
    if low < high:
        pivot_index = partition(draw_info, lst, low, high, ascending)
        yield True # to show animations - otherwise, the thing moves too quickly to see anything meaningful
        yield from quick_sort_helper(draw_info, lst, low, pivot_index-1, ascending) # delegation to left sub-array
        yield from quick_sort_helper(draw_info, lst, pivot_index+1, high, ascending) # delegation to right sub-array

# radix sort
def radix_sort(draw_info, ascending=True, lst=None):
    if lst == None:
        lst = draw_info.lst
    n = len(lst)

    # get the max value
    max_digs = len(str(max(lst)))

    x = 0
    while x < max_digs:
        bins = [[] for _ in range(10)]
        for i in range(n):
            index = (lst[i]//10**x) % 10
            bins[index].append(lst[i])
        # descending order check
        if ascending==False:
            bins.reverse() 
        i = 0
        for bin in bins:
            for item in bin:
                lst[i] = item
                i += 1
            # we visualize the current bin
            cp={k:draw_info.blue for k in range(i - len(bin), i)}
            draw_list(draw_info, cp, lst=lst, clear_bg=True)
            yield True
            time.sleep(0.2)
        x += 1
    return lst

# shell sort
def shell_sort(draw_info, ascending=True, lst=None):
    if lst==None:
        lst = draw_info.lst

    # similar to insertion sort, except that it uses logarithmic intervals i.e. half, quarter, eighth etc.
    n = len(lst)
    interval = n//2
    while interval > 0:
        for i in range(interval, n):
            current_item = lst[i]
            j = i
            while j >= interval and ((lst[j - interval] > current_item and ascending) or (lst[j - interval] < current_item and not ascending)):
                lst[j] = lst[j - interval]
                j -= interval
            lst[j] = current_item
            draw_list(draw_info, {j: draw_info.red, i: draw_info.green}, clear_bg=True)
            yield True

        interval //= 2
    return lst

# heap sort
def heap_sort(draw_info, ascending=True, lst=None):
    if lst is None:
        lst = draw_info.lst
    n = len(lst)

    # Build max heap
    for i in range(n // 2, -1, -1): # decreasing the size constantly to account for the last element in the heap being sorted
        yield from heapify(draw_info, lst, n, i, ascending)

    # Sort the heap
    for i in range(n - 1, 0, -1):
        # Swap the first and last elements
        lst[i], lst[0] = lst[0], lst[i]

        # Visualize the swap
        cp = {i: draw_info.brown, 0: draw_info.purple}
        draw_list(draw_info, cp)
        yield True

        # Heapify the remaining elements
        yield from heapify(draw_info, lst, i, 0, ascending)

    return lst

# Conversion into heaps
def heapify(draw_info, arr, n, i, ascending):
    # Find the largest or smallest element among the root and its children
    if ascending:
        largest_or_smallest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[i] < arr[l]:
            largest_or_smallest = l

        if r < n and arr[largest_or_smallest] < arr[r]:
            largest_or_smallest = r
    else:
        largest_or_smallest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[i] > arr[l]:
            largest_or_smallest = l

        if r < n and arr[largest_or_smallest] > arr[r]:
            largest_or_smallest = r

    # Visualize the heap
    heap_cp = {j: draw_info.blue for j in range(n)}
    heap_cp[i] = draw_info.yellow
    draw_list(draw_info, heap_cp, True)
    yield True

    # If root is not largest/smallest, swap with largest/smallest and continue heapifying
    if largest_or_smallest != i:
        arr[i], arr[largest_or_smallest] = arr[largest_or_smallest], arr[i]

        # Visualize the swap
        cp = {i: draw_info.green, largest_or_smallest: draw_info.red}
        draw_list(draw_info, cp)
        yield True

        yield from heapify(draw_info, arr, n, largest_or_smallest, ascending)

# pygame event loop
def main():
    run = True # flag
    clock = pygame.time.Clock() # regulates speed of loop in fps

    # random_lst variables; easier to modify list now
    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_lst(n, min_val, max_val)
    # instantiating draw_info class to create a display
    d_i = draw_info(1000, 800, lst)
    sorting = False # flag for sorting algorithm; like play/pause
    ascending = True # indicates order of sorting

    sorting_algorithm = bubble_sort # which algorithm will load?
    sorting_algo_name = 'Bubble Sort'
    sorting_algorithm_generator = None

    # * main loop here
    while run:
        clock.tick(10) #!fps

        if sorting: # if on play
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            refill(d_i, sorting_algo_name, ascending)

        # constantly refreshing screen
        pygame.display.update()

        # event listener
        for event in pygame.event.get():
            # exiting program by clicking on the red cross button
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r: # press r to reset the system
                lst = generate_starting_lst(n, min_val, max_val)
                d_i.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(d_i, ascending) # yield returns a generator which is stored here
            # N.B. only change the order when the system is paused
            elif event.key == pygame.K_a and sorting == False:
                ascending = True
            elif event.key == pygame.K_d and sorting == False:
                ascending = False
            
            # for the sorting algorithms
            elif event.key == pygame.K_b and sorting == False:
                sorting_algorithm = bubble_sort
                sorting_algo_name = 'Bubble Sort'
            elif event.key == pygame.K_i and sorting == False:
                sorting_algorithm = insertion_sort
                sorting_algo_name = 'Insertion Sort'
            elif event.key == pygame.K_s and sorting == False:
                sorting_algorithm = selection_sort
                sorting_algo_name = 'Selection Sort'
            elif event.key == pygame.K_m and sorting == False:
                sorting_algorithm = merge_sort
                sorting_algo_name = 'Merge Sort'
            elif event.key == pygame.K_q and sorting == False:
                sorting_algorithm = quick_sort
                sorting_algo_name = 'Quick Sort'
            elif event.key == pygame.K_x and sorting == False:
                sorting_algorithm = radix_sort
                sorting_algo_name = 'Radix Sort'
            elif event.key == pygame.K_h and sorting == False:
                sorting_algorithm = shell_sort
                sorting_algo_name = 'Shell Sort'
            elif event.key == pygame.K_p and sorting == False:
                sorting_algorithm = heap_sort
                sorting_algo_name = 'Heap Sort'

    pygame.quit()

tracemalloc.start() # tracing memory usage

# running the main code
if __name__ == "__main__":
    main()

# displaying the memory
memory_used = tracemalloc.get_traced_memory()
# current vs peak
print(
    f'Current: {round((memory_used[0]/2**20), 2)}MB, Peak: {round((memory_used[1]/2**20), 2)}MB')

# stopping the library
tracemalloc.stop()

# massive inspiration received from this YouTube video - https://youtu.be/twRidO-_vqQ
# I hope you enjoyed looking at this project!