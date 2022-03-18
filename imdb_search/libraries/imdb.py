import re
import time
import os 
import shutil

from openpyxl import load_workbook
from pathlib import Path

from RPA.Browser.Selenium import Selenium
from robot.libraries.BuiltIn import BuiltIn

from Communicate import RunItem
from RunItems import get_runitem
from Constants import COMPLETED, ERROR
from BotLogger import BotLogger


browser_lib = Selenium()
builtin = BuiltIn()
bot_log = BotLogger()
runitem = RunItem()

URL = 'https://www.imdb.com/'
FILE_NAME = "imdb.xlsx"

def open_browser(url):
    # use headless=True so robot work without opening browser, removi maximize argument
    # maximize help robot to open browser in full screen
    browser_lib.open_available_browser(url, maximized=True)

def movie_info_locator():
    """
        collection of locators like rating, storyline, tagline, genres
        return dictionary values
    """
    locators = {
        'rating': f'//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]',
        'storyline': f'//div[@data-testid="storyline-plot-summary"]/div/div',
        'tagline': f'//li[@data-testid="storyline-taglines"]/div/div/ul/li',
        'genres': f'//li[@data-testid="storyline-genres"]/div/ul/li'
    }
    return locators

def search_movie(name):
    movie_name = name
    search_field = 'id:suggestion-search'
    search_button = 'id:suggestion-search-button'
    browser_lib.input_text(search_field, movie_name)
    browser_lib.click_button(search_button)
    time.sleep(0.5)

def filter_movie():
    browser_lib.wait_until_page_contains_element("//div[@id='main']")
    
    # wait for movie list div or search result div 
    browser_lib.wait_until_page_contains_element('class:findFilterList')
    browser_lib.click_element('//*[@id="sidebar"]/div[3]/ul/ul/li[1]/a')
    browser_lib.wait_until_page_contains_element('//div[@class="article"]')
    
def get_req_movie_info():

    # call locator function and values are assigned to respective variables
    rating_locator, storyline_locator, tagline_locator, genres_locator_main = movie_info_locator().values()
    rating = browser_lib.get_text(rating_locator)

    # create genres list if the movies have more genres ie. ['Adventure', 'Drama', 'SciFi']
    genres_count = browser_lib.get_element_count(genres_locator_main)
    genres_list = [browser_lib.get_text(f'{genres_locator_main}[{i}]') for i in range(1, genres_count + 1)] 
    genres = ', '.join(genres_list)

    # checks whether the movie have taglines. some movie contains taglines, some not
    try:
        tagline_text = browser_lib.get_text(tagline_locator)
    except:
        tagline_text = 'Taglines Not Found'

    # capture storyline of the respective movie
    storyline_text = browser_lib.get_text(storyline_locator)

    return [{
        'Ratings': f'{rating}',
        'Storyline': f'{storyline_text}', 
        'Tagline': f'{tagline_text}', 
        'Genres': f'{genres}',
    }]

def get_movie_list():
    # some part of filtering movie is coded here 
    no_result = browser_lib.get_text('//h1[@class="findHeader"]')
    exact_title = browser_lib.is_element_visible('//div[@class="findToggleExact"]/a')

    # if robot catch no result found or no any exact title match filter 
    # it will return not found
    msg_condition = 'No results found for' in no_result or exact_title == False
    if msg_condition:
        return [{
            'Ratings': 'Not Found',
            'Storyline': 'Not Found',
            'Tagline':'Not Found',
            'Genres':'Not Found'
        }]

    # click to exact title match if element is visible
    browser_lib.click_element('//*[@id="main"]/div/div[2]/div/a')

    browser_lib.wait_until_page_contains_element('class:findSection')
    movie_rows = browser_lib.get_element_count('//*[@id="main"]/div/div[2]/table/tbody/tr')
    movie_lists = []

    # need optimization if possible 
    # when list of movies is shown after filtering we filter non year movie 
    # then take url of movie having year present in it
    for i in range(1, movie_rows+1):
        movie_table_locator = f'//*[@id="main"]/div/div[2]/table/tbody/tr[{i}]/td[2]'
        movie_year_text = browser_lib.get_text(movie_table_locator)
        movie_year = re.search(r'(\d+)', movie_year_text) or None
        movie_url = browser_lib.get_element_attribute(f'{movie_table_locator}/a', attribute='href')
        if movie_year != None:
            movie_lists.append([f'{movie_year.group()}', f'{movie_url}'])
        continue
    latest_movie = sorted(movie_lists)[-1][1]
    browser_lib.go_to(f'{latest_movie}')
    movie_infos = get_req_movie_info()
    return movie_infos

def read_write_excel():
    try:
        initial_time = builtin.get_time()
        current_dir = os.getcwd()
        file_name = os.path.join(current_dir, 'excel_file', FILE_NAME)
        wb = load_workbook(file_name)
        sheet = wb.worksheets[0]

        # read movie column which is 'A' column
        # read ratings, storyline, tagline and genres columns
        movies_col, rating_col, storyline_col, tagline_col, genres_col = sheet['A'], sheet['B'], sheet['C'], sheet['D'], sheet['E']

        for mov_ind in range(1, len(movies_col)-1):
            start_time = builtin.get_time()
            movie_name = movies_col[mov_ind].value

            if movie_name is None:
                continue

            bot_log.logger.info(f'{movie_name}: Search Started')
            search_movie(f"{movie_name.lower()}")
            filter_movie()

            movie_info = get_movie_list()

            # write the captured info into excel file
            rating_col[mov_ind].value = movie_info[0]['Ratings']
            storyline_col[mov_ind].value = movie_info[0]['Storyline']
            tagline_col[mov_ind].value = movie_info[0]['Tagline']
            genres_col[mov_ind].value = movie_info[0]['Genres']
            
            bot_log.logger.info(f'{movie_name}: Searched and Wrote Into Excel Row')
            final_time = builtin.get_time()
            imdb_log = bot_log.get_log_contents()
            runitem_val = get_runitem(
                    start_time, COMPLETED,
                    {'Search': 'Searched'},
                    final_time,
                    log_text=imdb_log
                )
            builtin.log_to_console(runitem_val) # comment this part when working with control room
            # runitem.create_run_items(runitem_val) # uncomment this part when working with control room
            bot_log.clear_logs()
            
        
        # save and close workbook here
        builtin.log_to_console('File saving and closing')
        wb.save(file_name)
        wb.close()
    except Exception as e:
        final_time = builtin.get_time()
        runitem_val = get_runitem(
                    initial_time, COMPLETED,
                    {'Search': 'Error occured'},
                    final_time,
                    log_text=e
                )
        builtin.log_to_console(runitem_val) # comment this part when working with control room
        # runitem.create_run_items(runitem_val) # uncomment this part when working with control room
        bot_log.clear_logs()
           
def copy_excel_to_output():
    current_dir = os.getcwd()
    file_name = os.path.join(current_dir, 'excel_file', FILE_NAME)
    output_path = os.path.join(current_dir, 'output')
    if Path(file_name).exists():
        pass

    # checks if output named directory exist
    if Path(output_path).exists():
        # if exist we create path where the copied file will be named output_imdb.xlsx
        destination = os.path.join(output_path, 'output_imdb.xlsx')

        # copy file into output folder
        shutil.copy(file_name, destination)
    else:
        builtin.log_to_console('Output folder is not created')    

def imdb():
    open_browser(URL)
    read_write_excel()
    copy_excel_to_output()

