import pygame


# detect if body is in chunk 

def check_collision_rect_circle(rect, circle_center, circle_radius):
    circle_x, circle_y = circle_center
    closest_x = max(rect.left, min(circle_x, rect.right))
    closest_y = max(rect.top, min(circle_y, rect.bottom))
    distance_squared = (circle_x - closest_x) ** 2 + (circle_y - closest_y) ** 2
    return distance_squared < (circle_radius ** 2)

# returns list of chunks in the quadrant in which the body is present


# try to find an alternative (too many chunks are returned)
def find_candidate_chunks(chunks_dict, circle_center, circle_radius, screen_center):
    
    circle_x, circle_y = circle_center
    screen_center_x, screen_center_y = screen_center

    candidate_quadrant_keys = []
    
    circle_rect = pygame.Rect(circle_x - circle_radius, circle_y - circle_radius,
                              circle_radius * 2, circle_radius * 2)

    if circle_rect.colliderect(pygame.Rect(0, 0, screen_center_x, screen_center_y)):
        candidate_quadrant_keys.append('I')
    if circle_rect.colliderect(pygame.Rect(screen_center_x, 0, screen_center_x, screen_center_y)):
        candidate_quadrant_keys.append('II')
    if circle_rect.colliderect(pygame.Rect(screen_center_x, screen_center_y, screen_center_x, screen_center_y)):
        candidate_quadrant_keys.append('III')
    if circle_rect.colliderect(pygame.Rect(0, screen_center_y, screen_center_x, screen_center_y)):
        candidate_quadrant_keys.append('IV')

    candidate_chunks = []
    for quadrant_key in set(candidate_quadrant_keys):
        candidate_chunks.extend(chunks_dict[quadrant_key])

    return candidate_chunks