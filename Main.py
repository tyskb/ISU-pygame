import pygame, math, random
from Button_class import Button
from item_class import Item, ItemsManager, PlayerInventory

pygame.init()
clock = pygame.time.Clock()
FPS = 60
run = True

#Screen size
sc_width = 1280
sc_length = 720
screen = pygame.display.set_mode((sc_width, sc_length))

#Title and Icon
pygame.display.set_caption("Game")
icon = pygame.image.load("pygame/images/financial-profit.png")
pygame.display.set_icon(icon)

#define fonts
title = pygame.font.SysFont("freesanbold.ttf", 36)
font = pygame.font.SysFont("freesanbold.ttf", 24)
s_font = pygame.font.SysFont("freesanbold.ttf", 18)

#define colours
TEXT_COL = (255, 255, 255)

#text
def draw_text(text, font, TEXT_COL, x, y):
    img = font.render(text, True, TEXT_COL)
    screen.blit(img, (x, y))

#bg images
background = pygame.image.load("pygame/images/city.png").convert()
background = pygame.transform.scale(background, (1823, 720))
bg_width = background.get_width()
game_bg = pygame.image.load("pygame/images/game.png")
game_bg = pygame.transform.scale(game_bg, (1280, 720))


#items img
nft = pygame.image.load("pygame/images/art.png")
bitcoin = pygame.image.load("pygame/images/bitcoin.png")
bubble_tea = pygame.image.load("pygame/images/bubble-tea.png")
gpu = pygame.image.load("pygame/images/graphic-card.png")
ps5 = pygame.image.load("pygame/images/play.png")
car = pygame.image.load("pygame/images/racing-car.png")
shoes = pygame.image.load("pygame/images/shoes.png")
watch = pygame.image.load("pygame/images/wristwatch.png")
nft = pygame.transform.scale(nft, (100, 100))
bitcoin = pygame.transform.scale(bitcoin, (100, 100))
bubble_tea = pygame.transform.scale(bubble_tea, (100, 100))
gpu = pygame.transform.scale(gpu, (100, 100))
ps5 = pygame.transform.scale(ps5, (100, 100))
car = pygame.transform.scale(car, (100, 100))
shoes = pygame.transform.scale(shoes, (100, 100))
watch = pygame.transform.scale(watch, (100, 100))
num_button = pygame.image.load("pygame/images/num_button.webp")
num_button = pygame.transform.scale(num_button, (50, 50))


#define game variables
tiles = math.ceil(sc_width / bg_width)+1
    #add an extra one as buffer (let the image to load)
items_manager = ItemsManager()

    
def generate_player_stats():
    """
    This function takes the name of the player and generates stats, inculding: age, luck, parnethood, and startup capital.
    It would return a  dictionary that contians those data.
    """
    # Player stats
    parenthood = random.randrange(1, 11)
    luck = random.randrange(-10, 11) * parenthood
    age = random.randrange(18, 41)
    startup_capital = random.randrange(100, 50000)

    if luck * parenthood > 1:
        startup_capital += luck * parenthood

    player_stats = {
        "Age": age,
        "Parenthood": parenthood,
        "Luck": luck,
        "Startup capital": startup_capital
    }

    return player_stats

#generate and save the player stats 
player_stats = generate_player_stats()

def display_player_stats(stats):
    player_stats = (
        f"Player Stats:             "
        f"Age: {stats['Age']}       "
        f"Luck: {stats['Luck']}     "
        f"Startup Capital: ${stats['Startup capital']}"
    )
    return(player_stats)

def calculate_total_price(items, quantities):
    total_price = 0
    for item, quantity in zip(items, quantities):
        total_price += item.price * quantity
    return total_price

def draw_inventory(inventory_display, font, x, y):
    for i, (item, quantity) in enumerate(inventory_display.items()):
        inventory_text = f"{item.name}: {quantity}"
        draw_text(inventory_text, font, TEXT_COL, x, y + i * 30)

#game Loop
def game_menu():

    run = True
    scroll = 0

    while run:

        clock.tick(FPS)

        #draw scrolling backgrond
        for i in range (0, tiles):
            screen.blit(background, (i * bg_width + scroll, 0))
                #The x and y location (Top left)
                
        #scroll background
        scroll -= 2

        #reset scroll (so it won't stop after 2 image)
        if abs(scroll) > bg_width:
            scroll = 0
            
        draw_text("> Press ENTER to start", title, TEXT_COL, 800, 550)
        draw_text("> Press ESC to quit", title, TEXT_COL, 800, 600)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    stats_display()
                elif event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()

player_stats = generate_player_stats()

def stats_display():

    run = True
    global player_stats
    show_stats = display_player_stats(player_stats)
    

    #scrolling text
    snip = font.render("", True, "white")
    counter = 0
    speed = 3
    done = False
    message = "> Press enter to continue"

    while run:

        screen.fill("black")
        clock.tick(FPS)

        if counter < speed * len(show_stats):
            counter += 1
        elif counter >= speed * len(show_stats):
            done = True

        snip = font.render(show_stats[0:counter//speed], True, "white")
        screen.blit(snip, (50, 250))

        pygame.display.update()

        snip = font.render(message[0:counter//speed], True, "white")
        screen.blit(snip, (950, 650))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play(show_stats, items_manager)
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
    pygame.quit()

#small item img
s_nft = pygame.transform.scale(nft, (50, 50))
s_bitcoin = pygame.transform.scale(bitcoin, (50, 50))
s_bubble_tea = pygame.transform.scale(bubble_tea, (50, 50))
s_gpu = pygame.transform.scale(gpu, (50, 50))
s_ps5 = pygame.transform.scale(ps5, (50, 50))
s_car = pygame.transform.scale(car, (50, 50))
s_shoes = pygame.transform.scale(shoes, (50, 50))
s_watch = pygame.transform.scale(watch, (50, 50))
s_num_button = pygame.transform.scale(num_button, (30, 30))

def play(show_stats, items_manager):

    run = True
    global player_stats
    player_inventory = PlayerInventory(max_size=150, initial_money=player_stats["Startup capital"])
    message = "> Press enter to proceed to the next year"

    # buttons
    buy_button = Button(num_button, (1150, 50), "Buy", font, "black", "green", "green")
    sell_button = Button(num_button, (870, 690), "Sell", font, "black", "red", "red")
    buttons = [
        Button(num_button, (150, 220), "0", font, "black", "green", "red"),
        Button(num_button, (300, 370), "0", font, "black", "green", "red"),
        Button(num_button, (450, 220), "0", font, "black", "green", "red"),
        Button(num_button, (600, 370), "0", font, "black", "green", "red"),
        Button(num_button, (750, 220), "0", font, "black", "green", "red"),
        Button(num_button, (900, 370), "0", font, "black", "green", "red"),
        Button(num_button, (1050, 220), "0", font, "black", "green", "red"),
        Button(num_button, (1200, 370), "0", font, "black", "green", "red"),
    ]
    s_buttons = [
        Button(s_num_button, (425, 540), "0", font, "black", "green", "red"),
        Button(s_num_button, (550, 540), "0", font, "black", "green", "red"),
        Button(s_num_button, (675, 540), "0", font, "black", "green", "red"),
        Button(s_num_button, (800, 540), "0", font, "black", "green", "red"),
        Button(s_num_button, (425, 670), "0", font, "black", "green", "red"),
        Button(s_num_button, (550, 670), "0", font, "black", "green", "red"),
        Button(s_num_button, (675, 670), "0", font, "black", "green", "red"),
        Button(s_num_button, (800, 670), "0", font, "black", "green", "red"),
    ]


    while run:

        screen.fill("black")

        screen.blit(game_bg, (0, 0))
        draw_text(show_stats, font, TEXT_COL, 50, 420)
        draw_text(f"Balance: {player_inventory.get_money()}", font, TEXT_COL, 600, 420)
        draw_text("Inventory:", font, TEXT_COL, 900, 420)

        mouse_pos = pygame.mouse.get_pos()
        left_click, _, right_click = pygame.mouse.get_pressed()
        

        # display market
        prices = items_manager.display_prices()
        for i, price in enumerate(prices):
            draw_text(price, font, TEXT_COL, 50, 450 + i * 30)

        inventory_display = player_inventory.get_inventory()
        draw_inventory(player_inventory.get_inventory(), font, 950, 450)
        draw_text(message, s_font, TEXT_COL, 970, 690)

        # items img
        screen.blit(nft, (100, 100))
        screen.blit(bitcoin, (250, 250))
        screen.blit(bubble_tea, (400, 100))
        screen.blit(gpu, (550, 250))
        screen.blit(ps5, (700, 100))
        screen.blit(car, (850, 250))
        screen.blit(shoes, (1000, 100))
        screen.blit(watch, (1150, 250))

        #small item img
        screen.blit(s_nft, (400, 470))
        screen.blit(s_bitcoin, (525, 470))
        screen.blit(s_bubble_tea, (650, 470))
        screen.blit(s_gpu, (775, 470))
        screen.blit(s_ps5, (400, 600))
        screen.blit(s_car, (525, 600))
        screen.blit(s_shoes, (650, 600))
        screen.blit(s_watch, (775, 600))

        for button in buttons:
            button.changeColor(mouse_pos, left_click, right_click)
            button.update(screen)

            change_amount = button.check_click(mouse_pos, left_click, right_click)
            if change_amount == 1:
                button.increment_value()
            elif change_amount == -1:
                button.decrement_value()

        for button in s_buttons:
            button.changeColor(mouse_pos, left_click, right_click)
            button.update(screen)

            change_amount = button.check_click(mouse_pos, left_click, right_click)
            if change_amount == 1:
                button.increment_value()
            elif change_amount == -1:
                button.decrement_value()

        buy_button.changeColor(mouse_pos, left_click, right_click)
        buy_button.update(screen)
        sell_button.changeColor(mouse_pos, left_click, right_click)
        sell_button.update(screen)
        
        #check if the buy button is clicked
        if buy_button.rect.collidepoint(mouse_pos) and left_click:
            items_to_buy = items_manager.items
            quantities = [button.get_value() for button in buttons]

            #calculate the total price
            total_price = calculate_total_price(items_to_buy, quantities)

            #check if the player has enough money to buy the items
            if player_inventory.get_money() >= total_price:
                for item, quantity in zip(items_to_buy, quantities):
                    player_inventory.buy_item(item, quantity)

                #update the balance display
                draw_text(f"Balance: {player_inventory.get_money()}", font, TEXT_COL, 600, 420)
                #reset num and price
                for button in buttons:
                    button.text_input = "0"
                total_price = 0
            else:
                #display a message if the player doesn't have enough money
                draw_text("Not enough money!", font, (255, 0, 0), 600, 450)

        # Check if the Sell button is clicked
        if sell_button.rect.collidepoint(mouse_pos) and left_click:
            items_to_sell = items_manager.items
            quantities = [button.get_value() for button in s_buttons]

            # Calculate the total selling price
            total_price = calculate_total_price(items_to_sell, quantities)

            # Sell the items and update the balance display
            sell_result, message1 = player_inventory.sell_items(items_to_sell, quantities)
            if sell_result:
                draw_text(f"Balance: {player_inventory.get_money()}", font, TEXT_COL, 600, 420)
                # Reset numbers on s_buttons
                for button in s_buttons:
                    button.text_input = "0"
            else:
                # Display a message if the player doesn't have enough items to sell
                draw_text(message1, font, (255, 0, 0), 600, 450)

        if player_stats["Age"] >= 75:
                if player_inventory.get_money() < 1000000000:
                    game_over()
                else:
                    win()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                        # Increase player's age by one
                        player_stats["Age"] += 1
                        # Change item prices randomly
                        items_manager.randomly_change_prices(num_items_to_change=3)  # You can adjust the number of items to change
                        # Update show_stats to reflect the changes
                        show_stats = display_player_stats(player_stats)
                        # Draw updated stats and prices
                        draw_text(show_stats, font, TEXT_COL, 50, 420)
                        prices = items_manager.display_prices()
                        for i, price in enumerate(prices):
                            draw_text(price, font, TEXT_COL, 50, 450 + i * 30)
            if event.type == pygame.QUIT:
                    run = False

        pygame.display.update()

    pygame.quit()

def game_over():
    run = True
    while run:
        screen.fill("black")
        message = "Game Over!"
        draw_text(message, title, TEXT_COL, 500, 350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()


def win():
    run = True
    while run:
        screen.fill("black")
        message = "You Win!"
        draw_text(message, title, TEXT_COL, 500, 350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()
    pygame.quit()

game_menu()
